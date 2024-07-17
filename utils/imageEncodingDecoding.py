import helper
from PIL import Image

def encodeImage(originalImageAddress, hiddenImageAddress, saveAddress):
    # Open both images in RGBA format in a list and copy the encoded image
    originalImage = Image.open(originalImageAddress)
    hiddenImage = Image.open(hiddenImageAddress)
    rgbaOriginalImage = originalImage.convert("RGBA")
    rgbaHiddenImage = hiddenImage.convert("RGBA")
    originalImagePixels = list(rgbaOriginalImage.getdata())
    hiddenImagePixels = list(rgbaHiddenImage.getdata())
    newImagePixels = originalImagePixels.copy()
    counter1 = 0
    counter2 = 0

    # Get image size differences for encoding
    widthDifference = originalImage.size[0] - hiddenImage.size[0]
    
    # Modify original images RGB values' least significant bits with the hidden images most significant
    rowIndex = 0
    for pixelIndex in range(len(originalImagePixels)):
        if pixelIndex % originalImage.size[0] == 0:
            rowIndex += 1
        originalPixel = originalImagePixels[pixelIndex]

        # If the index is not in the hidden image, set the 2 lsb of each value to 00 for all pixel
        if pixelIndex - (rowIndex * widthDifference) >= hiddenImage.size[0]:
            counter2 += 1
            newRGB = [[i for i in format(originalPixel[0], '08b')], 
                          [i for i in format(originalPixel[1], '08b')], 
                          [i for i in format(originalPixel[2], '08b')]]
                
            for channel in range(3):
                for i in range(2):
                    newRGB[channel][-i-1] = "0"

            # Replace original pixel with encoded one
            newPixel = (helper.binListToInt(newRGB[0]), 
                        helper.binListToInt(newRGB[1]), 
                        helper.binListToInt(newRGB[2]), originalPixel[3])
            newImagePixels[pixelIndex] = newPixel

        else:
            counter1 += 1
            hiddenPixel = hiddenImagePixels[pixelIndex]
            # If the originals alpha channel is 0, copy the RGB of the hidden image
            if originalPixel[3] == 0:
                newImagePixels[pixelIndex] = (hiddenPixel[0], 
                                            hiddenPixel[1], 
                                            hiddenPixel[2], 0)

            # If the originals alpha channel is !0, proceed normally
            else:
                newRGB = [[i for i in format(originalPixel[0], '08b')], 
                          [i for i in format(originalPixel[1], '08b')], 
                          [i for i in format(originalPixel[2], '08b')]]
                
                hiddenPixelBin = [[i for i in format(hiddenPixel[0], '08b')], 
                          [i for i in format(hiddenPixel[1], '08b')], 
                          [i for i in format(hiddenPixel[2], '08b')]]
                
                
                for channel in range(3):
                    for i in range(3):
                        newRGB[channel][-i-1] = hiddenPixelBin[channel][i]

                # Replace original pixel with encoded one
                newPixel = (helper.binListToInt(newRGB[0]), 
                            helper.binListToInt(newRGB[1]), 
                            helper.binListToInt(newRGB[2]), originalPixel[3])
                newImagePixels[pixelIndex] = newPixel

    # Save new encoded image
    print(f'encoder in-range pixels: {counter1}')
    print(f'encoder out of range pixels: {counter2}')
    newImage = Image.new("RGBA", rgbaOriginalImage.size)
    newImage.putdata(newImagePixels)
    newImage.save(saveAddress)
            




def decodeImage(encodedImageAddress, saveAddress):
    # Open the encoded image in RGBA format
    encodedImage = Image.open(encodedImageAddress)
    rgbaEncodedImage = encodedImage.convert("RGBA")
    encodedImagePixels = list(rgbaEncodedImage.getdata())
    decodedImagePixels = encodedImagePixels.copy()
    counter1 = 0
    counter2 = 0

    for pixelIndex, pixel in enumerate(encodedImagePixels):
        newRGB = [[i for i in format(pixel[0], '08b')], 
                    [i for i in format(pixel[1], '08b')], 
                    [i for i in format(pixel[2], '08b')], pixel[3]]
        if helper.binListToInt(newRGB[0][-2:]) != 0 or helper.binListToInt(newRGB[1][-2:]) != 0 or helper.binListToInt(newRGB[2][-2:]) != 0:
            counter1 += 1
        for channel in range(3):
            newRGB[channel][0] = newRGB[channel][-3]
            newRGB[channel][1] = newRGB[channel][-2]
            newRGB[channel][2] = newRGB[channel][-1]
            for i in range(3,8):
               newRGB[channel][i] = '0'
        
        if helper.binListToInt(newRGB[0]) != 0 or helper.binListToInt(newRGB[1]) != 0 or helper.binListToInt(newRGB[2]) != 0:
            counter2 += 1

        newPixel = (helper.binListToInt(newRGB[0]), 
                    helper.binListToInt(newRGB[1]), 
                    helper.binListToInt(newRGB[2]), 255)
        decodedImagePixels[pixelIndex] = newPixel

    # Save new encoded image
    print(f'decoder before change non-black pixels: {counter1}')
    print(f'decoder non-black pixels: {counter2}')
    newImage = Image.new("RGBA", rgbaEncodedImage.size)
    newImage.putdata(decodedImagePixels)
    newImage.save(saveAddress)

        

def main():
    encodeImage("utils/sample.png", "utils/sample2.png", "utils/encodedImage.png")
    decodeImage("utils/encodedImage.png", "utils/decodedImage.png")
    


if __name__ == "__main__":
    main()