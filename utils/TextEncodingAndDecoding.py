from constants import endDecode
from PIL import Image

def encodeText(imageAddress, text):
    # Open image in RGBA format and add to create a list of each pixels value
    image = Image.open(imageAddress)
    rgbaImage = image.convert("RGBA")
    pixels = list(rgbaImage.getdata())

    # Change text to be encoded into its Ascii form
    textBits = ""
    text += endDecode
    for character in text:
        textBits += str(bin(ord(character)))[2:]

    # Modify original images RGB values bits with the message
    modifiedPixels = []
    for pixel in pixels:
        if textBits:
            alphaChannel = pixel[3]
            modifiedPixelArray = [0,0,0,pixel[3]]
            for valIndex in range(3):
                if textBits:
                    newVal = ""
                    # Convert pixel to binary and change bits depending on alpha channel value

                    # If alpha is 0, change all rgb bits
                    if alphaChannel == 0:
                        for i in range(8):
                            if textBits:
                                newVal += textBits[0]
                                textBits = textBits[1:]
                            else:
                                newVal += "0"
                    # else only change the least significant bits
                    else:
                        original = str(bin(ord(pixel[valIndex])))[2:]
                        for i in range(3):
                            if textBits:
                                original[-i-1] = textBits[0]
                                textBits = textBits[1:]

                modifiedPixelArray[valIndex] = int(newVal, 2)

        # If there was information to be encoded, append encoded pixel, else, append original pixel
            modifiedPixel = (modifiedPixelArray[0], modifiedPixelArray[1], modifiedPixelArray[2], 1)
            modifiedPixels.append(modifiedPixel)
        else:
            modifiedPixels.append(pixel)
    
    modified_image = Image.new("RGBA", rgbaImage.size)
    modified_image.putdata(modifiedPixels)
    modified_image.save("utils/modified_image.png")



def decodeText(imageAddress):
    pass


def main():
    encodeText("utils/Sample.png", "h", 3)


if __name__ == "__main__":
    main()