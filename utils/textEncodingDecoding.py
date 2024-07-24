from constants import stopCode, defaultPassword
import helper

from PIL import Image

def encodeText(imageAddress, saveAddress, text, password):
    if not password:
        password = defaultPassword
        
    # Open image in RGBA format in a list and copy the encoded image
    image = Image.open(imageAddress)
    rgbaImage = image.convert("RGBA")
    pixels = list(rgbaImage.getdata())
    newImagePixels = pixels.copy()

    # Change text to be encoded into its Ascii form
    encryptedText = helper.encryptMessage(text, password)
    textBits = helper.messageToAscii(str(encryptedText))

    # Modify original images RGB values' bits with the message
    for pixelIndex, pixel in enumerate(pixels):
        # If there is more to be encoded, continue, otherwise, stop
        if not textBits:
            break
        # Create new arrays of pixels to change values
        newRGB = helper.pixelToBinLists(pixel)

        # For every pixel loop over all 3 rgb channels, 
        # changing all 8 values if the alpha channel is 0, and 3 if the alpha is more than 0
        for channel in range(3):
            if pixel[3] > 0:
                for i in range(2):
                    if textBits:
                        newRGB[channel][-i-1] = textBits[0]
                        textBits = textBits[1:]
            else:
                for i in range(8):
                    if textBits:
                        newRGB[channel][-i-1] = textBits[0]
                        textBits = textBits[1:]
        
        # Replace original pixel with encoded one
        newPixel = (helper.binListToInt(newRGB[0]), 
                    helper.binListToInt(newRGB[1]), 
                    helper.binListToInt(newRGB[2]), pixel[3])
        newImagePixels[pixelIndex] = newPixel

    # Save new encoded image
    newImage = Image.new("RGBA", rgbaImage.size)
    newImage.putdata(newImagePixels)
    newImage.save(saveAddress)



def decodeText(encodedImageAddress, password):
    if not password:
        password = defaultPassword

    # Open image in RGBA format in a list
    image = Image.open(encodedImageAddress)
    rgbaImage = image.convert("RGBA")
    pixels = list(rgbaImage.getdata())

    # Variables to keep track of message and bits
    message = ""
    bits = ""

    for pixel in pixels:
        binPixel = [helper.intToListOfBits(pixel[0]), 
                    helper.intToListOfBits(pixel[1]), 
                    helper.intToListOfBits(pixel[2]), pixel[3]]
        
        for channel in range(3):
            if pixel[3] > 0:
                for i in range(2):
                    bits += binPixel[channel][-i-1]
                    if len(bits) == 8:
                        message += helper.binStringToChar(bits)
                        bits = ""
                        if helper.checkForStopCode(message):
                            message = message[:-len(stopCode)]
                            byteData = message.encode('latin1').decode('unicode_escape').encode('latin1')
                            return helper.decryptMessage(byteData, password)
                            
            else:
                for i in range(8):
                    bits += binPixel[channel][-i-1]
                    if len(bits) == 8:
                        message += helper.binStringToChar(bits)
                        bits = ""
                        if helper.checkForStopCode(message):
                            message = message[:-len(stopCode)]
                            byteData = message.encode('latin1').decode('unicode_escape').encode('latin1')
                            return helper.decryptMessage(byteData, password)

        
        


def main():
    encodeText("utils/sample.png", "utils/encodedText.png", 
               "The big bad man thought he could see this message but he can't", "python")
    print(decodeText("utils/encodedText.png", "python"))
    


if __name__ == "__main__":
    main()
