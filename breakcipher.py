from mersenneTwister import extract_number, seed_mt
from server import generate_token


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

# STILL NEED TO IMPLEMENT
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
lshifttc = temp ^ ((temp << t) & c)
lshiftsb = temp ^ ((temp << s) & b)
val1 = [int(x) for x in list('{0:032b}'.format(rhsift))]
val2sb = [int(x) for x in list('{0:032b}'.format(lshiftsb))]
val2tc = [int(x) for x in list('{0:032b}'.format(lshifttc))]
# print("Inital: " + str([int(i) for i in list('{:032b}'.format(100))]))
# print(temp1)
print(temp)
# print(val)
print(rhsift)
# print(val1)
print()
# print("inital: " + str([int(i) for i in list('{:032b}'.format(temp ^ (temp >> l)))]))
rUndo = (undoRight(int(rhsift), l))
print("rUndo: " + str(rUndo))
print()

print(temp)
# print(val)
print(lshiftsb)
# print(val2sb)
print()
lUndosb = undoLeft(lshiftsb, s, b)
print("lUndosb: " + str(lUndosb))
print()

print(temp)
# print(val)
print(lshifttc)
# print(val2tc)
print()
lUndotc = undoLeft(lshifttc, t, c)
print("lUndotc: " + str(lUndotc))
print()

print("unmix")

seed_mt(12345)
extractVal = extract_number()

print("unmixed val: " + str(unmix(extractVal)))
