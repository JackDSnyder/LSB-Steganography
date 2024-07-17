from constants import endDecode
from helper import binListToInt
from PIL import Image

def encodeText(imageAddress, text):
    # Open image in RGBA format and add to create a list of each pixels value
    image = Image.open(imageAddress)
    rgbaImage = image.convert("RGBA")
    pixels = list(rgbaImage.getdata())
    newImagePixels = pixels.copy()

    # Change text to be encoded into its Ascii form
    text += endDecode
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
        newPixel = (binListToInt(newRGB[0]), binListToInt(newRGB[1]), binListToInt(newRGB[2]), pixel[3])
        print(newPixel)
        newImagePixels[pixelIndex] = newPixel

    # Save new encoded image
    newImage = Image.new("RGBA", rgbaImage.size)
    newImage.putdata(newImagePixels)
    newImage.save("utils/encodedImage.png")

            


def main():
    encodeText("utils/Sample.png", "Test")
    


if __name__ == "__main__":
    main()