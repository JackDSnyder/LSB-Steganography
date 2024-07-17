from constants import stopCode

def binListToInt(binList):
    binString = ''.join(binList)
    return int(binString, 2)

def binStringToChar(binString):
    binString = ''.join(binString)
    return chr(int(binString, 2))

def checkForStopCode(str1):
    return stopCode in str1