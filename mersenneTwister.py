# # # References: 
# # # https://en.wikipedia.org/wiki/Mersenne_Twister#Pseudocode
# # # https://www.cryptologie.net/article/331/how-does-the-mersennes-twister-work/ 
# # # https://cplusplus.com/reference/random/mt19937/ 

# coefficients for MT19937
w, n, m, r = 32, 624, 397, 31
a = 0x9908b0df
u, d = 11, 0xffffffff
s, b = 7, 0x9d2c5680
t, c = 15, 0xefc60000
l = 18
f = 1812433253

MT = [[] for i in range(n)]
idx = n + 1
lower_mask = (1 << r) - 1 
lower_mask = (1 << r) - 1
upper_mask = ~lower_mask & ((1 << w) - 1)

def seed_mt(seed):
    global idx
    
    idx = n
    
    MT[0] = seed
    for i in range(1, n):
        MT[i] = (f * (MT[i-1] ^ (MT[i-1] >> (w-2))) + i) & 0xffffffff

def extract_number():
    global idx

    if idx >= n:
        if idx > n:
            raise Exception("Generator was never seeded")
        twist()

    y = MT[idx]
    y = y ^ ((y >> u) & d)
    y = y ^ ((y << s) & b)
    y = y ^ ((y << t) & c)
    y = y ^ (y >> l)

    idx += 1
    return y & 0xffffffff

def twist():
    global idx
    for i in range(n):
        x = (MT[i] & upper_mask) | (MT[(i+1) % n] & lower_mask)
        xA = x >> 1
        if (x % 2) != 0:
            xA = xA ^ a
        MT[i] = MT[(i + m) % n] ^ xA
    idx = 0


if __name__ == '__main__':
    seed_mt(1234)
    print(extract_number())
    seed_mt(0)
    print(extract_number())
    seed_mt(100000)
    print(extract_number())