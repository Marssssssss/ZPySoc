def bitCount(x):
    x = (x & 0x55555555) + (x >> 1 & 0x55555555)
    x = (x & 0x33333333) + (x >> 2 & 0x33333333)
    x = (x & 0x0f0f0f0f) + (x >> 4 & 0x0f0f0f0f)
    x = (x & 0x00ff00ff) + (x >> 8 & 0x00ff00ff)
    return x + (x >> 16) & 0xffff


a = int(raw_input())
print bitCount(a)

