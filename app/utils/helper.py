from .constants import stopCode, defaultPassword
from PIL import Image
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

import hashlib

##############################################################
# Helper functions for encoding and decoding images and text #
##############################################################

# Evaluates and return a list of 0's and 1's
def binListToInt(binList: list) -> int:
    binString = ''.join(binList)
    return int(binString, 2)

# Evaluates binary and returns the associated ASCII character
def binStringToChar(binString: str) -> str:
    binString = ''.join(binString)
    return chr(int(binString, 2))

# Returns a string of the 8-bit binary version of each characters ASCII number
def messageToAscii(message: str) -> str:
    message = message[2:-1]
    message += stopCode
    textBits = ""
    for char in message:
        textBits += format(ord(char), '08b')
    return textBits


# Converts an integer into a lists of 0's and 1's that represent the integer in binary
def intToListOfBits(num: int) -> list:
    return [i for i in format(num, "08b")]

# Converts a pixels RGB data into binary lists
def pixelToBinLists(pixel: list) -> list:
    return [intToListOfBits(pixel[0]),
            intToListOfBits(pixel[1]),
            intToListOfBits(pixel[2])]

# Returns whether the stopcode is in a string
def checkForStopCode(str1: str) -> bool:
    return stopCode in str1

# Pad a hidden image to fit the dimensions of the original image
def padImage(originalImagePath: str, hiddenImagePath: str) -> Image:
    originalImage = Image.open(originalImagePath)
    originalWidth, originalHeight = originalImage.size
    hiddenImage = Image.open(hiddenImagePath)

    # Create a black image with the dimensions of the original image
    newImage = Image.new('RGB', (originalWidth, originalHeight), (0, 0, 0, 0))
    # Paste the hidden image onto the new image
    newImage.paste(hiddenImage, (0, 0))

    # Return the new image
    return newImage



##################################################################
# Helper functions for encrypting and decrypting images and text #
##################################################################

##################################
# Text Encryption and Decryption #
##################################

# Returns a byte object representing the SHA-256 hash of the password
def deriveTextKey(password: str) -> bytes:
    # .encode() first encodes the password into bytes
    # Then .sha256() returns the SHA-256 hash object of the encoded password bytes
    # Lastly, .digest() retrieves the hash value from the hash object as a bytes object
    return hashlib.sha256(password.encode()).digest()

def encryptMessage(message: str, password: str) -> bytes:
    key = deriveTextKey(password)

    # AES.new() creates a cipher object is an instance of an encryption algorithm that can encrypt and decrypt
    # CBC is Cipher Block Chaining mode which takes each 16 byte data block from the AES algorithm and chains them together by XORing them together
    cipher = AES.new(key, AES.MODE_CBC)

    # An iv (initialization vector) is a pseudo-random value that ensures that the same text encrypted multiple times with the same key
    # will produce different cyphertexts each time, introducing randomness in the encryption process adding another layer of security
    iv = cipher.iv

    # First the message is converted to bytes using encode, then pad() pads the encoded message to fit in 16byte block sizes to work with the AES algorithm
    # Lastly, .encrypt() uses our cipher object to encrypt the padded message
    encryptedMessage = cipher.encrypt(pad(message.encode(), AES.block_size))

    # Concatenates the iv and encrypted message because the iv is needed for deryption. Returns a bytes object containing both thte message and iv
    return iv + encryptedMessage

def decryptMessage(encryptedMessage: bytes, password: str) -> str:
    key = deriveTextKey(password)

    # Extracts the iv from the encrypted message
    iv = encryptedMessage[:AES.block_size]

    if isinstance(iv, str):
        iv = iv.encode()

    # Creates a cypher object with the iv for decryption
    cipher = AES.new(key, AES.MODE_CBC, iv)

    try:
        # First, the iv is sliced out of the encrypted message
        # Second, the message is decrypted using the cypher containing the iv
        # Lastly, we unpad the message since it was padded to encrypt the message
        decryptedMessage = unpad(cipher.decrypt(encryptedMessage[AES.block_size:]), AES.block_size)
        # The decrypted message is in bytes so it is decoded and then returned back as a string
        return decryptedMessage.decode()
    except:
        return "Incorrect passcode."


###################################
# Image Encryption and Decryption #
###################################

def deriveImageKey(password: str) -> int:
    # First, the password is encoded into bytes, then uses the bytes to compute the SHA-256 hash
    # Next, the hash is is converted to a string of hexadecimal digits.
    # Lastly, the hexadecimal string is evaluated as an integer and returned
    hashInt =  int(hashlib.sha256(password.encode()).hexdigest(), 16)
    return hashInt % (2**32)

def shufflePixels(image: np.ndarray, key: int) -> np.ndarray:
    np.random.seed(key)

    # Reshapes the image, -1 is a placeholder to have the size of the dimension
    # image.shape[2] is 4 because each pixels values are stored in RGBA format
    flatImage = image.reshape(-1, image.shape[2])

    # The image is shuffled randomly using random seeded previously by the key
    np.random.shuffle(flatImage)

    # The image is reshaped and returned
    return flatImage.reshape(image.shape)

def unshufflePixels(image: np.ndarray, key:int) -> np.ndarray:
    np.random.seed(key)

    # Reshapes the image just as shufflePixels does
    flatImage = image.reshape(-1, image.shape[2])

    # Creates an array of indices ranging from 0 to the amount of pixels-1
    indices = np.arange(flatImage.shape[0])

    # Uses the seeded random to shuffle the indices
    np.random.shuffle(indices)

    # Creates an array with the same shape as the flat image to store the unshuffled pixels
    originalImage = np.empty_like(flatImage)

    # Assigns the shuffled pixels back to their original positions
    originalImage[indices] = flatImage

    # Reshapes the array back to its original shape
    return originalImage.reshape(image.shape)
