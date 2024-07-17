from constants import stopCode
import helper
from PIL import Image

def encodeText(imageAddress, saveAddress, text):
    # Open image in RGBA format in a list and copy the list for the encoded image
    image = Image.open(imageAddress)
    rgbaImage = image.convert("RGBA")
    pixels = list(rgbaImage.getdata())
    newImagePixels = pixels.copy()

    # Change text to be encoded into its Ascii form
    text += stopCode
    textBits = ""
    for char in text:
        textBits += format(ord(char), '07b')

    # Modify original images RGB values bits with the message
    for pixelIndex, pixel in enumerate(pixels):
        # If there is more to be encoded, continue, otherwise, stop
        if not textBits:
            break
        # Create new arrays of pixels to change values
        newRGB = [[i for i in format(pixel[0], '08b')], [i for i in format(pixel[1], '08b')], [i for i in format(pixel[2], '08b')], pixel[3]]
        # For every pixel loop over all 3 rgb channels, changing all 8 values if the alpha channel is 0, and 3 if the alpha is more than 0
        for channel in range(3):
            if pixel[3] > 0:
                for i in range(3):
                    if textBits:
                        newRGB[channel][-i-1] = textBits[0]
                        textBits = textBits[1:]
            else:
                for i in range(8):
                    if textBits:
                        newRGB[channel][-i-1] = textBits[0]
                        textBits = textBits[1:]
        
        # Replace original pixel with encoded one
        newPixel = (helper.binListToInt(newRGB[0]), helper.binListToInt(newRGB[1]), helper.binListToInt(newRGB[2]), pixel[3])
        newImagePixels[pixelIndex] = newPixel

    # Save new encoded image
    newImage = Image.new("RGBA", rgbaImage.size)
    newImage.putdata(newImagePixels)
    newImage.save(saveAddress)



def decodeText(encodedImageAddress):
    # Open image in RGBA format in a list
    image = Image.open(encodedImageAddress)
    rgbaImage = image.convert("RGBA")
    pixels = list(rgbaImage.getdata())

    # Variables to keep track of message and bits
    message = ""
    bits = ""

    for pixel in pixels:
        binPixel = [[i for i in format(pixel[0], '08b')], [i for i in format(pixel[1], '08b')], [i for i in format(pixel[2], '08b')], pixel[3]]
        if helper.checkForStopCode(message):
            print(message[:-len(stopCode)])
            return message[:-len(stopCode)]
        
        for channel in range(3):
            if pixel[3] > 0:
                for i in range(3):
                    bits += binPixel[channel][-i-1]
                    if len(bits) == 7:
                        message += helper.binStringToChar(bits)
                        bits = ""
                        if helper.checkForStopCode(message):
                            print(message[:-len(stopCode)])
                            return message[:-len(stopCode)]
            else:
                for i in range(8):
                    bits += binPixel[channel][-i-1]
                    if len(bits) == 7:
                        message += helper.binStringToChar(bits)
                        bits = ""
                        if helper.checkForStopCode(message):
                            print(message[:-len(stopCode)])
                            return message[:-len(stopCode)]

        
        


            


def main():
    encodeText("utils/sample.png", "utils/encodedText.png", "The big bad man thought he could see this message but he can't")
    decodeText("utils/encodedText.png")
    


if __name__ == "__main__":
    main()