#Mersenne Twister MT 19937
class MT19937:
	def __init__(self, seed):
		self.seed = int.from_bytes(seed, 'big')
		self.w, self.n, self.m, self.r = 32, 624, 397, 31
		self.a = 0x9908b0df
		self.u, self.d = 11, 0xffffffff
		self.s, self.b = 7, 0x9d2c5680
		self.t, self.c = 15, 0xefc60000
		self.l = 18
		self.f = 1812433253
		self.MT = [[] for i in range(self.n)]
		self.idx = self.n + 1
		self.lower_mask = (1 << self.r) - 1 
		self.lower_mask = (1 << self.r) - 1
		self.upper_mask = ~self.lower_mask & ((1 << self.w) - 1)
		self.MT[0] = self.seed
		for i in range(1, self.n):
			self.MT[i] = (self.f * (self.MT[i-1] ^ (self.MT[i-1] >> (self.w-2))) + i) & 0xffffffff
		return

	#Extract a tempered value based on MT[index]
	#calling twist() every n numbers
	def extract_number(self):
		#TODO: Temper and Extract Here
		if self.idx >= self.n:
			self.twist()
		y = self.MT[self.idx]
		y = y ^ ((y >> self.u) & self.d)
		y = y ^ ((y << self.s) & self.b)
		y = y ^ ((y << self.t) & self.c)
		y = y ^ (y >> self.l)
		self.idx += 1
		return y & self.d
		# return 42


	#Generate the next n values from the series x_i 
	def twist(self):
		for i in range(self.n):
			self.x = (self.MT[i] & self.upper_mask) | (self.MT[(i+1) % self.n] & self.lower_mask)
			xA = self.x >> 1
			if (self.x % 2) != 0:
				xA = xA ^ self.a
			self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA
		self.idx = 0
		return

