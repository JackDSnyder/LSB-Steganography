from .constants import stopCode, defaultPassword
from . import helper

from PIL import Image
import numpy as np
from io import BytesIO

def encodeText(originalImageIO, text, outputIO, password):
    if not password:
        password = defaultPassword

    # Encrypt the text first
    encrypted_text = helper.encryptMessage(text, password)
    
    # Convert encrypted text to binary
    textBinary = ''
    for byte in encrypted_text:
        textBinary += format(byte, '08b')
    textBinary += '00000000'  # Add null terminator

    # Open the original image
    originalImage = Image.open(originalImageIO)
    rgbaOriginalImage = originalImage.convert("RGBA")
    originalWidth, originalHeight = rgbaOriginalImage.size

    # Convert image to numpy array
    originalImagePixels = np.array(rgbaOriginalImage.getdata(), dtype=np.uint8).reshape((originalHeight, originalWidth, 4))
    newImagePixels = originalImagePixels.copy()

    # Encode text in the image
    textIndex = 0
    for pixelRow in range(originalHeight):
        for pixelCol in range(originalWidth):
            if textIndex >= len(textBinary):
                break

            originalPixel = originalImagePixels[pixelRow, pixelCol]
            newRGB = helper.pixelToBinLists(originalPixel)

            # Modify the least significant bits with text data
            for channel in range(3):
                if textIndex < len(textBinary):
                    newRGB[channel][-1] = textBinary[textIndex]
                    textIndex += 1

            # Replace original pixel with encoded one
            newPixel = (helper.binListToInt(newRGB[0]), 
                        helper.binListToInt(newRGB[1]), 
                        helper.binListToInt(newRGB[2]), originalPixel[3])
            newImagePixels[pixelRow, pixelCol] = newPixel

    # Save the encoded image
    newImage = Image.fromarray(newImagePixels.astype('uint8'), 'RGBA')
    newImage.save(outputIO, format='PNG')
    return True

def decodeText(encodedImageIO, password):
    if not password:
        password = defaultPassword

    # Open the encoded image
    encodedImage = Image.open(encodedImageIO)
    rgbaEncodedImage = encodedImage.convert("RGBA")
    imageWidth, imageHeight = rgbaEncodedImage.size

    # Convert image to numpy array
    encodedImagePixels = np.array(rgbaEncodedImage.getdata(), dtype=np.uint8).reshape((imageHeight, imageWidth, 4))

    # Extract binary data
    binaryData = ''
    for pixel in encodedImagePixels.reshape(-1, 4):
        for channel in range(3):
            binaryData += format(pixel[channel], '08b')[-1]
            if len(binaryData) % 8 == 0:
                char = chr(int(binaryData[-8:], 2))
                if char == '\0':  # Null terminator
                    # Convert binary data to bytes
                    encrypted_bytes = bytes()
                    for i in range(0, len(binaryData)-8, 8):
                        byte = int(binaryData[i:i+8], 2)
                        encrypted_bytes += bytes([byte])
                    
                    try:
                        # Decrypt the text
                        decrypted_text = helper.decryptMessage(encrypted_bytes, password)
                        if decrypted_text == "Incorrect passcode.":
                            return "Error: Incorrect password. Please try again."
                        return decrypted_text
                    except Exception as e:
                        print(f"Decryption error: {str(e)}")
                        return "Error: Failed to decrypt message. Please check your password."

    return ''  # Return empty string if no null terminator found
