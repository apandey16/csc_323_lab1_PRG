import base64 
import binascii

encryptionType = "utf-8"
#'ascii'/'utf-8'
handler = "replace"
#'ignore'/'replace'

def base64Encode(input: str) -> bytes:
    stringBytes = input.encode(encryptionType, handler)
    return base64.b64encode(stringBytes)
    # encodedBytes = base64.b64encode(stringBytes)
    # return encodedBytes.decode(encryptionType,handler)

def base64Decode(input):
    encodedBytes = input.encode(encryptionType,handler)
    return base64.b64decode(encodedBytes)
    # stringBytes = base64.b64decode(encodedBytes)
    # return stringBytes.decode(encryptionType,handler)

def convertToHex(binary: bytes) -> str:
    return str(binary.hex())

def convertToBytes(hexStr: str) -> bytes:
    hexStr = ''.join(c for c in hexStr if c in '0123456789ABCDEFabcdef')

    if len(hexStr) % 2 != 0:
        hexStr = '0' + hexStr
    return binascii.unhexlify(hexStr)
