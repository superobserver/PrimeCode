#!/usr/bin/env python
import cmath
import numpy
import sys
numpy.set_printoptions(threshold=sys.maxsize)

# Get limit for the range to be sieved
limit = int(input("limit value here: "))
limit = int(limit)

# Calculate epoch
h = limit
epoch = 90 * (h * h) - 12 * h + 1
print("The epoch range is", epoch)
limit = epoch
base10 = (limit * 90) + 11
print("This is the base-10 limit:", base10)

# Calculate range for iterations
a = 90
b = -300
c = 250 - limit
d = (b**2) - (4 * a * c)
sol1 = (-b - cmath.sqrt(d)) / (2 * a)
sol2 = (-b + cmath.sqrt(d)) / (2 * a)
print('The solutions are {0} and {1}'.format(sol1, sol2))
new_limit = int(sol2.real)

# Initialize arrays
A201804 = numpy.zeros(int(limit + 10), dtype=int)
oplist = []  # Tracks number of zeros per iteration
forbidden_values = []  # To store indices where A201804 remains 0
marks_per_operator = [numpy.zeros(int(limit + 10), dtype=int) for _ in range(12)]  # Separate array for each operator

# Composite generating function
def drLD(x, l, m, z, o, listvar, op_index):
    y = 90 * (x * x) - l * x + m
    if 0 <= y < len(listvar):
        listvar[y] += 1
        marks_per_operator[op_index][y] += 1
    p = z + (90 * (x - 1))
    q = o + (90 * (x - 1))
    for n in range(1, int(((limit - y) / p) + 1)):
        idx = int(y + p * n)
        if 0 <= idx < len(listvar):
            listvar[idx] += 1
            marks_per_operator[op_index][idx] += 1
    for n in range(1, int(((limit - y) / q) + 1)):
        idx = int(y + q * n)
        if 0 <= idx < len(listvar):
            listvar[idx] += 1
            marks_per_operator[op_index][idx] += 1
    numzero = (listvar == 0).sum()
    oplist.append(numzero)

# Apply cancellation operators
operator_params = [
    (120, 34, 7, 53),   # Operator 1
    (132, 48, 19, 29),  # Operator 2
    (120, 38, 17, 43),  # Operator 3
    (90, 11, 13, 77),   # Operator 4
    (78, -1, 11, 91),   # Operator 5
    (108, 32, 31, 41),  # Operator 6
    (90, 17, 23, 67),   # Operator 7
    (72, 14, 49, 59),   # Operator 8
    (60, 4, 37, 83),    # Operator 9
    (60, 8, 47, 73),    # Operator 10
    (48, 6, 61, 71),    # Operator 11
    (12, 0, 79, 89)     # Operator 12
]

for x in range(1, new_limit):
    for idx, (l, m, z, o) in enumerate(operator_params):
        drLD(x, l, m, z, o, A201804, idx)

# Trim buffer
A201804 = A201804[:-10]
for i in range(12):
    marks_per_operator[i] = marks_per_operator[i][:-10]

# Identify forbidden values
forbidden_values = [k for k in range(len(A201804)) if A201804[k] == 0]
print("Forbidden values (k where 90k + 11 are prime):", forbidden_values)
print("Number of forbidden values:", len(forbidden_values))

# Calculate density of marks
marks = len(A201804) - (A201804 == 0).sum()
density = marks / len(A201804)
print("Total marks:", marks)
print("Density of marks:", density)

# Analyze marks per operator
for i, (l, m, z, o) in enumerate(operator_params):
    total_marks = marks_per_operator[i].sum()
    print(f"Operator {i+1} (z={z}, o={o}): Total marks = {total_marks}")

# Analyze cancellation frequencies for the first operator as an example
def analyze_frequencies(op_index, z, o):
    frequencies = {}
    for x in range(1, new_limit):
        y = 90 * (x * x) - operator_params[op_index][0] * x + operator_params[op_index][1]
        p = z + (90 * (x - 1))
        q = o + (90 * (x - 1))
        if 0 <= y < limit:
            frequencies[y] = frequencies.get(y, 0) + 1
        for n in range(1, int(((limit - y) / p) + 1)):
            idx = int(y + p * n)
            if 0 <= idx < limit:
                frequencies[idx] = frequencies.get(idx, 0) + 1
        for n in range(1, int(((limit - y) / q) + 1)):
            idx = int(y + q * n)
            if 0 <= idx < limit:
                frequencies[idx] = frequencies.get(idx, 0) + 1
    return frequencies

# Example: Analyze frequencies for the first operator
freqs = analyze_frequencies(0, 7, 53)
print("Mark frequencies for Operator 1 (z=7, o=53):", dict(sorted(freqs.items())[:20]))  # Print first 20 for brevity