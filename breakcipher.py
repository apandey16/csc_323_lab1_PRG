import os
import MT19937
import requests
import re
import base64


w, n, m, r = 32, 624, 397, 31
a = 0x9908b0df
u, d = 11, 0xffffffff
s, b = 7, 0x9d2c5680
t, c = 15, 0xefc60000
l = 18
f = 1812433253

# the las l bits are the least significant bits 
# kind of reconstructing the last l bits at a time

def undoRight(value, shift):
    value = [int(x) for x in list('{0:032b}'.format(value))]
    retVal = value

    offset = 0 

    while offset < w:
        curMath = []
        chunk = [0] * offset + [1] * shift + [0] * (w - shift -offset)
        for num in range(w):
            curMath.append(value[num] & chunk[num])

        curMath = ([0] * shift) + curMath
        curMath = curMath[:w]

        for digitIdx in range(len(curMath)):
            retVal[digitIdx] = retVal[digitIdx] ^ curMath[digitIdx]

        offset += shift

    retValNum = int(bin(int(''.join(map(str, retVal)), 2)) , 2)
    return retValNum

def undoLeft(value, shift, andedVal):
    explodedAnd = [int(x) for x in list('{0:032b}'.format(andedVal))]
    value = [int(x) for x in list('{0:032b}'.format(value))]
    retVal = value

    offset = 0 

    while offset < w:
        curMath = []
        chunk = [0] * (w - shift - offset) + [1] * shift + [0] * offset
        for num in range(w):
            curMath.append(value[num] & chunk[num])

        curMath += [0] * shift
        curMath = curMath[-w:]

        for digitIdx in range(len(curMath)):
            retVal[digitIdx] = retVal[digitIdx] ^ (curMath[digitIdx] & explodedAnd[digitIdx])

        offset += shift

    retValNum = int(bin(int(''.join(map(str, retVal)), 2)) , 2)
    return retValNum


# y = y ^ ((y >> u) & d)
# y = y ^ ((y << s) & b)
# y = y ^ ((y << t) & c)
# y = y ^ (y >> l)
def unmix(input):
    y = undoRight(input, l)
    y = undoLeft(y, t, c)
    y = undoLeft(y, s, b)
    y = undoRight(y, u)  # don't need to pass in d becuae it just ensures it is a 32 bit number
    return y

def resetAdminPassword():
    registerPayload = {"user" : "user", "password" : "password"}
    regesterURL = 'http://0.0.0.0:8080/register'
    resetPasswordUrl = 'http://0.0.0.0:8080/forgot'
    resetPayload = {"user" : "user"}

    requests.post(regesterURL, data=registerPayload)

    encodedResetToken = []
    for i in range(78):
        reset = requests.post(resetPasswordUrl, resetPayload)
        match = (re.search(r'/?token=.*<', reset.text))
        encodedResetToken.append(match.group(0)[6:-27])

    decodedTokens = []
    for item in encodedResetToken:
        decodedTokens.append(str(base64.b64decode(item))[2:-1].split(':'))

    state = []
    for item in decodedTokens:
        for num in item:
            state.append(int(unmix(int(num))))

    seed = os.urandom(4)
    mt = MT19937.MT19937(seed)
    mt.MT = state

    adminResetPayload = {"user" : "admin"}
    resetFormUrl = 'http://0.0.0.0:8080/reset?token='

    requests.post(resetPasswordUrl, data=adminResetPayload)
    
    generatedToken = str(mt.extract_number())
    for i in range(7):
        generatedToken += ":" + str(mt.extract_number())
    generatedToken = str(base64.b64encode(generatedToken.encode('utf-8')))[2:-1]
    resetFormUrl += generatedToken

    newPassword = {"password": "pass"}
    requests.post(resetFormUrl, data=newPassword)

    newAdminLogin = {"username": "admin", "password": "pass"}
    loginURL = 'http://0.0.0.0:8080/'
    r = requests.post(loginURL, data=newAdminLogin)
    return r.text
    

retTok = resetAdminPassword()
print(retTok)