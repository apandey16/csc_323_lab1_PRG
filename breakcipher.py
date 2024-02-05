from mersenneTwister import extract_number, seed_mt


w, n, m, r = 32, 624, 397, 31
a = 0x9908b0df
u, d = 11, 0xffffffff
s, b = 7, 0x9d2c5680
t, c = 15, 0xefc60000
l = 18
f = 1812433253

def unmix(y):
    y = y & d
    y = y ^ (y >> l)
    y = y ^ ((y << t) & c)
    y = y ^ ((y << s) & b)
    y = y ^ ((y >> u) & d)
    return y

seed_mt(1234)
print(unmix(extract_number()))