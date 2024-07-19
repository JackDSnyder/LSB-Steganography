from constants import stopCode
from PIL import Image

def binListToInt(binList):
    binString = ''.join(binList)
    return int(binString, 2)

def binStringToChar(binString):
    binString = ''.join(binString)
    return chr(int(binString, 2))

def checkForStopCode(str1):
    return stopCode in str1

def indexInHidden(index: int, originalImage: Image, hiddenImage: Image):
    originalDimensions = originalImage.size
    hiddenDimensions = hiddenImage.size
    yIndex = index // originalDimensions[0]
    xIndex = index % originalDimensions[0]
    return xIndex < hiddenDimensions[0] and yIndex < hiddenDimensions[1]

def originalIndexToHiddenIndex(originalIndex: int, originalImage: Image, hiddenImage: Image):
    originalDimensions = originalImage.size
    hiddenDimensions = hiddenImage.size
    
    originalY = originalIndex // originalDimensions[0]
    orignalX = originalIndex % originalDimensions[0]
    
    return orignalX + originalY * hiddenDimensions[0]
