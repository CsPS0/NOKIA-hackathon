import math

def min_drops(n, h):
    d = 1
    while True:
        total_floors = 0
        for i in range(1, n + 1):
            total_floors += math.comb(d, i)
        if total_floors >= h:
            return d
        d += 1

print(min_drops(1, 100))
print(min_drops(2, 100))
print(min_drops(3, 100))
