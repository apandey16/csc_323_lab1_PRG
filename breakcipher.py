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

def undoRight(value, shift):
    value = [int(x) for x in list('{0:032b}'.format(value))]
    y_shifted = [0] * shift
    retVal = []
    print(value)

    # value.reverse()

    valueChunked = []

    offset = 0
    while offset < w:
        valueChunked.append(value[offset:shift + offset])
        offset += shift
    print(valueChunked)


    loopOffset = 0
    for item in valueChunked:
        for digit in range(len(item)):
            discoveredElement = item[digit] ^ y_shifted[digit + loopOffset]
            retVal.append(discoveredElement)
        loopOffset += shift 
        y_shifted += retVal
    
    # retVal.reverse()
    print(retVal)

    return retVal

    # i = 0
    # while i < w:
    #     mask = '0' * i + '1' * shift + '0' * (w - shift - i)
    #     mask = int(mask[:w], 2)
    #     section = retVal & mask

    #     retVal = retVal ^ (section >> shift)

    #     i += shift

    # return retVal

def deconstructedValues(mixedValue, size):
    y_shifted = [0] * size
    og_y = []
    
    mixedValue = [int(d) for d in str(mixedValue)]
    mixedValue.reverse()

    mixedValueChunked = []
    # do it in chucks
    chunk = 0
    while chunk < len(mixedValue):
        mixedValueChunked.append(mixedValue[chunk:chunk + size])
        chunk += size
    print(mixedValueChunked) 
    # mixedValueChunked.reverse()

    offset = 0
    for block in mixedValueChunked:
        # block.reverse()
        for element in range(len(block)):
            discoveredElement = block[element] ^ y_shifted[element + offset]
            og_y.append(discoveredElement)
        offset += size
        y_shifted += og_y
    
    og_y.reverse()

    return og_y

def unmix(y):
    # print(y)
    # y_bits = [int(i) for i in list('{:032b}'.format(y))]
    # print(y_bits)


    print("found:  " + "".join(str(deconstructedValues(y, l))))
    
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
    # print(retTokens)
    
    for tok in retTokens:
        unmixedTokens.append(unmix(int.from_bytes(tok, 'big')))
    
    return unmixedTokens

# temp1 = 100
# print(type(temp1))
temp = 123456789
val = [int(x) for x in list('{0:032b}'.format(temp))]
# print(temp1)
rhsift = temp ^ (temp >> l)
val1 = [int(x) for x in list('{0:032b}'.format(rhsift))]
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
# unmix(rhsift)

# unmix(temp ^ (temp >> l))
# seed_mt(1234)
# unmix(extract_number())
# print(tokens())