from mersenneTwister import extract_number, seed_mt
from server import generate_token


w, n, m, r = 32, 624, 397, 31
a = 0x9908b0df
u, d = 11, 0xffffffff
s, b = 7, 0x9d2c5680
t, c = 15, 0xefc60000
l = 18
f = 1812433253


# y = y ^ ((y >> u) & d)
# y = y ^ ((y << s) & b)
# y = y ^ ((y << t) & c)
# y = y ^ (y >> l)

# the las l bits are the least significant bits 
# kind of reconstructing the last l bits at a time

def undoRight(value, shift, anded=None):
    value = [int(x) for x in list('{0:032b}'.format(value))]
    y_shifted = [0] * shift
    retVal = []

    valueChunked = []

    offset = 0
    while offset < w:
        valueChunked.append(value[offset:shift + offset])
        offset += shift
        
    loopOffset = 0
    for item in valueChunked:
        for digit in range(len(item)):
            discoveredElement = item[digit] ^ y_shifted[digit + loopOffset]
            retVal.append(discoveredElement)
        loopOffset += shift 
        y_shifted += retVal
        
    if anded is not None:
        andedInts = [int(x) for x in list('{0:032b}'.format(anded))]
        for idx in range(len(andedInts)):
            retVal[idx] = andedInts[idx] & retVal[idx]
    return retVal

def undoLeft(value, shift):
    value = [int(x) for x in list('{0:032b}'.format(value))]
    y_shifted = [0] * shift
    retVal = []

    valueChunked = []

    offset = 0
    while offset < w:
        valueChunked.append(value[-shift:])
        value = value[:-shift]
        offset += shift

    loopOffset = 0
    for chunk in valueChunked:
        tempRetVal = []
        for digit in range(len(chunk)):
            if len(chunk) == shift:
                discoveredElement = chunk[digit] ^ y_shifted[digit + loopOffset]
            else:
                discoveredElement = chunk[digit] ^ y_shifted[len(y_shifted) - len(chunk) + digit]
            tempRetVal = tempRetVal + [discoveredElement]
        retVal = tempRetVal + retVal
        y_shifted = y_shifted + tempRetVal
        loopOffset += shift


    return retVal

def unmix(y):
    y = y ^ (y << l)
    y = y ^ ((y << t) & c)
    y = y ^ ((y << s) & b)
    y = y ^ ((y >> u) & d)
    return y

def tokens():
    # request token from server via API
    retTokens = []
    unmixedTokens = []
    for i in range(78):
        retTokens.append(generate_token())
    
    for tok in retTokens:
        unmixedTokens.append(unmix(int.from_bytes(tok, 'big')))
    
    return unmixedTokens

temp = 1276448053
val = [int(x) for x in list('{0:032b}'.format(temp))]
# print(temp1)
rhsift = temp ^ ((temp >> l))
lshift = temp ^ ((temp << s) & 0xFFFFFFFF)
val1 = [int(x) for x in list('{0:032b}'.format(rhsift))]
val2 = [int(x) for x in list('{0:032b}'.format(lshift))]
# print("Inital: " + str([int(i) for i in list('{:032b}'.format(100))]))
# print(temp1)
print(temp)
print(val)
print(rhsift)
print(val1)
print()
# print("inital: " + str([int(i) for i in list('{:032b}'.format(temp ^ (temp >> l)))]))
rUndo = (undoRight(int(rhsift), l))
print("rUndo: " + str(rUndo))
print()

print(temp)
print(val)
print(lshift)
print(val2)
print()
lUndo = undoLeft(int(lshift), s)
print("lUndo: " + str(lUndo))
print()

# unmix(rhsift)

# unmix(temp ^ (temp >> l))
# seed_mt(1234)
# unmix(extract_number())
# print(tokens())