from .constants import defaultPassword
from . import helper

from PIL import Image
import numpy as np

def encodeImage(originalImageAddress, hiddenImageAddress, saveAddress, password):
    if not password:
        password = defaultPassword

    # Pad the hidden image to fit the dimensions of the original image and open the original image normally
    hiddenImage = helper.padImage(originalImageAddress, hiddenImageAddress)
    originalImage = Image.open(originalImageAddress)

    # Open both images in RGBA format in a list and copy the encoded image
    rgbaOriginalImage = originalImage.convert("RGBA")
    rgbaHiddenImage = hiddenImage.convert("RGBA")
    hiddenWidth, hiddenHeight = rgbaHiddenImage.size
    originalWidth, originalHeight = rgbaOriginalImage.size

    # Changes the container of the pixel information from a python list to a Numpy array with array elements being 8-bit integers
    # Then reshapes 1d array into a 3d array, with height being the height of the image, same for width, 
    # and 4 represents the 4 channels RGBA for each pixel.
    originalImagePixels = np.array(rgbaOriginalImage.getdata(), dtype=np.uint8).reshape((originalHeight, originalWidth, 4))
    hiddenImagePixels = np.array(rgbaHiddenImage.getdata(), dtype=np.uint8).reshape((hiddenHeight, hiddenWidth, 4))

    # Encrypt image by shuffling pixels
    hashKey = helper.deriveImageKey(password)
    hiddenImagePixels = helper.shufflePixels(hiddenImagePixels, hashKey)
    newImagePixels = originalImagePixels.copy()
    
    # Modify original images RGB values' least significant bits with the hidden images most significant
    for pixelRow in range(originalHeight):
        for pixelCol in range(originalWidth):
            originalPixel = originalImagePixels[pixelRow, pixelCol]
            hiddenPixel = hiddenImagePixels[pixelRow, pixelCol]

            # If the originals alpha channel is 0, copy the RGB of the hidden image
            if originalPixel[3] == 0:
                newImagePixels[pixelRow*originalWidth+pixelCol] = (hiddenPixel[0], 
                                            hiddenPixel[1], 
                                            hiddenPixel[2], 0)

            # If the originals alpha channel isn't 0, proceed normally
            else:
                newRGB = helper.pixelToBinLists(originalPixel)
                hiddenPixelBin = helper.pixelToBinLists(hiddenPixel)               
                
                for channel in range(3):
                    for i in range(3):
                        newRGB[channel][-3+i] = hiddenPixelBin[channel][i]

                # Replace original pixel with encoded one
                newPixel = (helper.binListToInt(newRGB[0]), 
                            helper.binListToInt(newRGB[1]), 
                            helper.binListToInt(newRGB[2]), originalPixel[3])
                newImagePixels[pixelRow, pixelCol] = newPixel

    newImage = Image.fromarray(newImagePixels.astype('uint8'), 'RGBA')
    newImage.save(saveAddress)
            


def decodeImage(encodedImageAddress, saveAddress, password):
    if not password:
        password = defaultPassword

    # Open the encoded image in RGBA format
    encodedImage = Image.open(encodedImageAddress)
    rgbaEncodedImage = encodedImage.convert("RGBA")
    imageWidth, imageHeight = rgbaEncodedImage.size

    # Changes the container of the pixel information from a python list to a Numpy array with array elements being 8-bit integers
    # Then reshapes 1d array into a 3d array, with height being the height of the image, same for width, 
    # and 4 represents the 4 channels RGBA for each pixel.
    encodedImagePixels = np.array(rgbaEncodedImage.getdata(), dtype=np.uint8).reshape((imageHeight, imageWidth, 4))
    decodedImagePixels = encodedImagePixels.copy()

    # Iterate over every pixel, shifting the 3 least significant bits to be the 3 most siginificant bits
    for pixelIndex, pixel in enumerate(encodedImagePixels.reshape(-1,4)):
        newRGB = [[i for i in format(pixel[0], '08b')], 
                    [i for i in format(pixel[1], '08b')], 
                    [i for i in format(pixel[2], '08b')]]
        
        for channel in range(3):
            newRGB[channel][0] = newRGB[channel][-3]
            newRGB[channel][1] = newRGB[channel][-2]
            newRGB[channel][2] = newRGB[channel][-1]
            for i in range(3,8):
               newRGB[channel][i] = '0'

        newPixel = (helper.binListToInt(newRGB[0]), 
                    helper.binListToInt(newRGB[1]), 
                    helper.binListToInt(newRGB[2]), 255)
        decodedImagePixels[pixelIndex // imageWidth, pixelIndex % imageWidth] = newPixel

    # Decrypt image
    hashKey = helper.deriveImageKey(password)
    decodedImagePixels = helper.unshufflePixels(decodedImagePixels, hashKey)

    # Find the bounds of the non-black content
    def is_black_row(row):
        return np.all(row[:, :3] == 0)  # Check if all RGB values are 0

    def is_black_column(col):
        return np.all(col[:, :3] == 0)  # Check if all RGB values are 0

    # Find first and last non-black rows
    first_row = 0
    last_row = imageHeight - 1
    for i in range(imageHeight):
        if not is_black_row(decodedImagePixels[i]):
            first_row = i
            break
    for i in range(imageHeight - 1, -1, -1):
        if not is_black_row(decodedImagePixels[i]):
            last_row = i
            break

    # Find first and last non-black columns
    first_col = 0
    last_col = imageWidth - 1
    for i in range(imageWidth):
        if not is_black_column(decodedImagePixels[:, i]):
            first_col = i
            break
    for i in range(imageWidth - 1, -1, -1):
        if not is_black_column(decodedImagePixels[:, i]):
            last_col = i
            break

    # Crop the image to remove black padding
    decodedImagePixels = decodedImagePixels[first_row:last_row + 1, first_col:last_col + 1]

    # Save new decoded image
    newImage = Image.fromarray(decodedImagePixels.astype('uint8'), 'RGBA')
    newImage.save(saveAddress)

        



