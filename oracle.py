import base64
from encodeAndDecode import base64Encode
import random
import time
from mersenneTwister import seed_mt, extract_number

def oracle():
    time.sleep(random.randint(5, 60))

    curTime = int(time.time())
    print("seed start time: " + str(curTime))
    seed_mt(curTime)
    time.sleep(random.randint(5, 60))

    mtNum = extract_number()

    retVal = base64Encode(str(mtNum))

    return retVal

def findTime(retVal):
    startTime = int(time.time())
    testTime = startTime
    extractedVal = None

    while extractedVal != retVal:
        seed_mt(testTime)
        encodedRetVal = base64Encode(str(extract_number()))
        extractedVal = base64.b64decode(encodedRetVal).decode('utf-8')
        testTime -= 1

    return testTime + 1

def main():
    encodedRetVal = oracle()
    decodedRetVal = base64.b64decode(encodedRetVal).decode('utf-8')
    # print(decodedRetVal)

    print("found time: " + str(findTime(decodedRetVal)))

if __name__ == '__main__':
    main()