#!/usr/bin/env python
import cmath
import math
from collections import Counter

# User input for start value and total range
start = input("Enter the start value: ")
start = int(start)
total_range = int(input("Enter the total range (depth of the list, e.g., 1000): "))
limit = start + total_range

# List of TRUE to depth of search space
primes = [0] * (limit - start)

# Get RANGE for number of iterations through functions
# Constants for QUADRATIC
a = 90
b = -300
c = 250 - limit

# Calculate the discriminant
d = (b ** 2) - (4 * a * c)

# Find two solutions
sol1 = (-b - cmath.sqrt(d)) / (2 * a)
sol2 = (-b + cmath.sqrt(d)) / (2 * a)
print('The solutions are {0} and {1}'.format(sol1, sol2))

# The integer REAL part of this value is the limit for RANGE
new_limit = sol2.real

s = 0

# Function for generating composites
def drLD(x, l, m, z, o):
    global s
    s = s + 1
    y = 90 * (x * x) - l * x + m
    if start <= y < limit:
        primes[y - start] = primes[y - start] + 1
        print("added y", y)

    p = z + (90 * (x - 1))
    newp_start = int((start - y) / p)
    newp_lim = int(((limit - y) / p) + 1)
    if int(new_limit) / x < 1.3:
        newp_start = newp_start - 1
    for n in range(newp_start, newp_lim):
        s = s + 1
        new_y = y + (p * n)
        print(new_y, n, x, z)
        if start <= new_y < limit:
            primes[new_y - start] = primes[new_y - start] + 1
            print("TAKEN OUT OF THE P LIST", new_y, n, x, z, newp_start, newp_lim)

    q = o + (90 * (x - 1))
    newq_start = int((start) / q)
    newq_lim = int(((limit) / q) + 1)
    if int(new_limit) / x < 1.3:
        newq_start = newq_start - 1
    for n in range(newq_start, newq_lim):
        new2_y = y + (q * n)
        print(new2_y, n, x, o)
        s = s + 1
        if start <= new2_y < limit:
            primes[new2_y - start] = primes[new2_y - start] + 1
            print("TAKEN OUT OF THE Q LIST", new2_y, n, x, o, newq_start, newq_lim)

# Apply composite generating functions up to the calculated new_limit
for x in range(1, int(new_limit) + 1):
    # 11
    drLD(x, 78, -1, 11, 91)   # 11,91 @11, 203 5    564
    drLD(x, 120, 34, 7, 53)   # 7,53  @4,  154 1    831
    drLD(x, 132, 48, 19, 29)  # 19,29 @6,  144 2    371
    drLD(x, 120, 38, 17, 43)  # 17,43 @8,  158 3    403
    drLD(x, 90, 11, 13, 77)   # 13,77 @11, 191 4    493
    drLD(x, 108, 32, 31, 41)  # 31,41 @14, 176 6    262
    drLD(x, 90, 17, 23, 67)   # 23,67 @17, 197 7    320
    drLD(x, 72, 14, 49, 59)   # 49,59 @32, 230 8    192
    drLD(x, 60, 4, 37, 83)    # 37,83 @34, 244 9    229
    drLD(x, 60, 8, 47, 73)    # 47,73 @38, 248 10   195
    drLD(x, 48, 6, 61, 71)    # 61,71 @48, 270 11   165
    drLD(x, 12, 0, 79, 89)    # 79,89 @78, 336 12   139

# primes.remove(primes[0])  # Delete the first element as it is not coded/operated on
print("Amplitude map:", primes)
print("The total number of operations on the list:", sum(primes))
A201804c = [i for i, x in enumerate(primes) if x == 0]
newA = [(i + start) for i in A201804c]

print("This is the number of A201804 primes:", len(newA), "between", start, "and", limit)
A201804b = [(i * 90) + 11 for i in newA]

print("This is the last 50 terms base-10 expression of A201804 (see A142317):", A201804b[-50:])