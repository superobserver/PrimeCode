#!/usr/bin/env python
import time

# User input for start value and total range
start = int(input("Enter the start value: "))
total_range = int(input("Enter the total range (depth of the list, e.g., 1000): "))
limit = start + total_range

# Initialize amplitude map
amplitude_map = [0] * total_range

# Digital root and last digit check
def is_valid(num):
    dr = num
    while dr > 9:
        dr = sum(int(d) for d in str(dr))
    ld = num % 10
    return dr in [1, 2, 4, 5, 7, 8] and ld in [1, 3, 7, 9]

# Function for generating composites
def drLD(x, l, m, z, o, amp_map, start_val, lim):
    y = 90 * (x * x) - l * x + m
    if start_val <= y < lim:
        amp_map[y - start_val] += 1
    p = z + (90 * (x - 1))
    newp_start = int((start_val - y) / p)
    newp_lim = int(((lim - y) / p) + 1)
    for n in range(newp_start, newp_lim):
        new_y = y + (p * n)
        if start_val <= new_y < lim and is_valid(90 * new_y + 11):
            amp_map[new_y - start_val] += 1
    q = o + (90 * (x - 1))
    newq_start = int((start_val) / q)
    newq_lim = int(((lim) / q) + 1)
    for n in range(newq_start, newq_lim):
        new2_y = y + (q * n)
        if start_val <= new2_y < lim and is_valid(90 * new2_y + 11):
            amp_map[new2_y - start_val] += 1

# Pairs for k=11 (A201804)
pairs = [
    (7, 53, 4), (19, 29, 6), (17, 43, 8), (13, 77, 11), (11, 91, 11),
    (31, 41, 14), (23, 67, 17), (49, 59, 32), (37, 83, 34), (47, 73, 38),
    (61, 71, 48), (79, 89, 78)
]

# Mark composites and measure time
start_time = time.time()
for x in range(1, 1000):  # Arbitrary upper limit for x, adjust as needed
    for p, q, n_0 in pairs:
        l, m = (120, 34) if (p == 7 and q == 53) else (132, 48) if (p == 19 and q == 29) else (120, 38) if (p == 17 and q == 43) else (90, 11) if (p == 13 and q == 77) else (78, -1) if (p == 11 and q == 91) else (108, 32) if (p == 31 and q == 41) else (90, 17) if (p == 23 and q == 67) else (72, 14) if (p == 49 and q == 59) else (60, 4) if (p == 37 and q == 83) else (60, 8) if (p == 47 and q == 73) else (48, 6) if (p == 61 and q == 71) else (12, 0)
        drLD(x, l, m, p, q, amplitude_map, start, limit)
end_time = time.time()
execution_time = end_time - start_time

print("Amplitude map:", amplitude_map)
print("The total energy to produce this list:", sum(amplitude_map))
A201804c = [i for i, x in enumerate(amplitude_map) if x == 0]
newA = [(i + start) for i in A201804c]
print("This is the number of A201804 amplitude_map:", len(newA), "between", start, "and", limit)
A201804b = [(i * 90) + 11 for i in newA]
print("This is the last 50 terms base-10 expression of A201804 (see A142317):", A201804b[-50:])
base10lim = (limit * 90) + 11
operators = 1000 * 12  # Adjust based on actual x limit
print("This is the number of LOCATION OPERATORS:", operators)
print("This is the number of operations:", sum(amplitude_map))
print("This is the limit in base-10:", base10lim)
print("This is the ratio of base10limit to OPERATORS:", base10lim / operators)
print("This is the square root of the base10limit:", math.sqrt(base10lim))
print("This is the ratio of the sq.rt. to the OPERATORS:", math.sqrt(base10lim) / operators)
print("This is the ratio sqrt(lim) to ACTUAL list ops:", math.sqrt(base10lim) / sum(amplitude_map))
newdict = Counter(amplitude_map)
bigOmega = dict(newdict)
print("This is the distribution of composite types:", bigOmega)
print("Execution time:", execution_time, "seconds")