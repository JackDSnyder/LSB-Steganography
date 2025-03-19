from .constants import stopCode, defaultPassword
from PIL import Image
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import hashlib
from io import BytesIO

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
    return [[i for i in format(pixel[0], '08b')], 
            [i for i in format(pixel[1], '08b')], 
            [i for i in format(pixel[2], '08b')]]

# Returns whether the stopcode is in a string
def checkForStopCode(str1: str) -> bool:
    return stopCode in str1

# Pad a hidden image to fit the dimensions of the original image
def padImage(originalImageIO, hiddenImageIO):
    # Open both images
    originalImage = Image.open(originalImageIO)
    hiddenImage = Image.open(hiddenImageIO)

    # Get dimensions
    originalWidth, originalHeight = originalImage.size
    hiddenWidth, hiddenHeight = hiddenImage.size

    # Create a new image with the same dimensions as the original
    paddedImage = Image.new('RGBA', (originalWidth, originalHeight), (0, 0, 0, 0))

    # Paste the hidden image in the top-left corner
    paddedImage.paste(hiddenImage, (0, 0))

    return paddedImage



##################################################################
# Helper functions for encrypting and decrypting images and text #
##################################################################

##################################
# Text Encryption and Decryption #
##################################

# Returns a byte object representing the SHA-256 hash of the password
def deriveTextKey(password: str) -> bytes:
    # Create a hash of the password to use as a key for encryption
    if not password:
        password = defaultPassword
    return hashlib.sha256(password.encode()).digest()

def encryptMessage(message: str, password: str) -> bytes:
    key = deriveTextKey(password)
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    encryptedMessage = cipher.encrypt(pad(message.encode(), AES.block_size))
    return iv + encryptedMessage

def decryptMessage(encryptedMessage: bytes, password: str) -> str:
    key = deriveTextKey(password)
    iv = encryptedMessage[:AES.block_size]

    if isinstance(iv, str):
        iv = iv.encode()

    cipher = AES.new(key, AES.MODE_CBC, iv)

    try:
        decryptedMessage = unpad(cipher.decrypt(encryptedMessage[AES.block_size:]), AES.block_size)
        return decryptedMessage.decode()
    except:
        return "Incorrect passcode."


###################################
# Image Encryption and Decryption #
###################################

def deriveImageKey(password):
    # Create a hash of the password to use as a key for shuffling
    if not password:
        password = defaultPassword
    return int.from_bytes(hashlib.sha256(password.encode()).digest()[:4], byteorder='big')

def shufflePixels(pixels, key):
    # Create a copy of the pixels array to avoid modifying the original
    shuffled = pixels.copy()
    
    # Use the key to generate a deterministic but random-looking sequence
    np.random.seed(key)
    
    # Get the shape of the array
    height, width = pixels.shape[:2]
    
    # Create a list of all pixel indices
    indices = np.arange(height * width)
    
    # Shuffle the indices
    np.random.shuffle(indices)
    
    # Reshape the indices back to 2D
    indices = indices.reshape(height, width)
    
    # Apply the shuffle to each channel
    for i in range(pixels.shape[2]):
        shuffled[:, :, i] = pixels[:, :, i].flatten()[indices].reshape(height, width)
    
    return shuffled

def unshufflePixels(pixels, key):
    # Create a copy of the pixels array to avoid modifying the original
    unshuffled = pixels.copy()
    
    # Use the key to generate the same sequence as in shufflePixels
    np.random.seed(key)
    
    # Get the shape of the array
    height, width = pixels.shape[:2]
    
    # Create a list of all pixel indices
    indices = np.arange(height * width)
    
    # Shuffle the indices
    np.random.shuffle(indices)
    
    # Create the inverse permutation
    inverse_indices = np.zeros_like(indices)
    inverse_indices[indices] = np.arange(len(indices))
    
    # Reshape the inverse indices back to 2D
    inverse_indices = inverse_indices.reshape(height, width)
    
    # Apply the inverse shuffle to each channel
    for i in range(pixels.shape[2]):
        unshuffled[:, :, i] = pixels[:, :, i].flatten()[inverse_indices].reshape(height, width)
    
    return unshuffled
