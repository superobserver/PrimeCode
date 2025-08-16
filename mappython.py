#!/usr/bin/env python
import cmath
import math
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Get user input for limit
limit = int(input("Enter number (h): "))
h = limit
epoch = 90 * (h * h) - 12 * h + 1
limit = epoch
print(f"Epoch: {limit}")

# Calculate x_max using the quadratic formula
a, b, c = 90, -300, 250 - limit
d = (b**2) - (4 * a * c)
sol1 = (-b - cmath.sqrt(d)) / (2 * a)
sol2 = (-b + cmath.sqrt(d)) / (2 * a)
new_limit = sol2
print(f"x_max: {new_limit.real}")

# Initialize array for A224854
A224854 = [0] * int(limit + 100)  # Buffer to avoid index errors

# Composite generating function
def drLD(x, l, m, z, listvar, primitive):
    y = 90 * (x * x) - l * x + m
    if y < len(listvar):
        listvar[y] += 1
    p = z + (90 * (x - 1))
    for n in range(1, int(((limit - y) / p) + 1)):
        idx = y + (p * n)
        if idx < len(listvar):
            listvar[idx] += 1

# Apply the sieve operators for A224854
for x in range(1, int(new_limit.real)):
    # Operators for 90n + 11
    for l, m, z in [
        (120, 34, 7), (120, 34, 53), (132, 48, 19), (132, 48, 29),
        (120, 38, 17), (120, 38, 43), (90, 11, 13), (90, 11, 77),
        (78, -1, 11), (78, -1, 91), (108, 32, 31), (108, 32, 41),
        (90, 17, 23), (90, 17, 67), (72, 14, 49), (72, 14, 59),
        (60, 4, 37), (60, 4, 83), (60, 8, 47), (60, 8, 73),
        (48, 6, 61), (48, 6, 71), (12, 0, 79), (12, 0, 89)
    ]:
        drLD(x, l, m, z, A224854, 11)

    # Operators for 90n + 13
    for l, m, z in [
        (76, -1, 13), (76, -1, 91), (94, 18, 19), (94, 18, 67),
        (94, 24, 37), (94, 24, 49), (76, 11, 31), (76, 11, 73),
        (86, 6, 11), (86, 6, 83), (104, 29, 29), (104, 29, 47),
        (86, 14, 23), (86, 14, 71), (86, 20, 41), (86, 20, 53),
        (104, 25, 17), (104, 25, 59), (14, 0, 77), (14, 0, 89),
        (94, 10, 7), (94, 10, 79), (76, 15, 43), (76, 15, 61)
    ]:
        drLD(x, l, m, z, A224854, 13)

# Trim buffer and process data
A224854 = A224854[:-100]
twin_prime_n = [i for i, x in enumerate(A224854) if x == 0]
print(f"Number of twin primes: {len(twin_prime_n)}")

# Find maximum number of markings
max_markings = max(A224854)
print(f"Maximum number of markings: {max_markings}")

# Analyze neighbor markings
neighbor_markings_left = Counter()
neighbor_markings_right = Counter()
for n in twin_prime_n:
    # Left neighbor (n-1), skip if n=0
    if n > 0:
        left_mark = A224854[n - 1]
        neighbor_markings_left[left_mark] += 1
    # Right neighbor (n+1), skip if n is at the end
    if n < limit - 1:
        right_mark = A224854[n + 1]
        neighbor_markings_right[right_mark] += 1

# Total twin primes with valid neighbors
total_left = sum(neighbor_markings_left.values())  # Excludes n=0
total_right = sum(neighbor_markings_right.values())  # All have right neighbor unless at end

# Compute probabilities for all marking values
classes = range(max_markings + 1)
prob_left = [neighbor_markings_left.get(i, 0) / total_left if total_left > 0 else 0 for i in classes]
prob_right = [neighbor_markings_right.get(i, 0) / total_right if total_right > 0 else 0 for i in classes]
prob_avg = [(pl + pr) / 2 for pl, pr in zip(prob_left, prob_right)]  # Average of left and right

# Verify sum of probabilities
prob_sum = sum(prob_avg)
print(f"Sum of probabilities: {prob_sum:.4f}")

# Bar graph visualization
plt.figure(figsize=(15, 6))
plt.bar(classes, prob_avg, color='lightcoral', edgecolor='black', width=0.8)
plt.xlabel('Number of Markings of Neighbor')
plt.ylabel('Probability')
plt.title(f'Probability of Neighbor Markings for Twin Primes in A224854 (n = 0 to {limit - 1})')
plt.xticks(np.arange(0, max_markings + 1, step=max(1, max_markings // 20)))  # Adjust ticks for readability
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add text annotation
plt.figtext(0.5, -0.15, f'Bar graph showing the probability that a twin prime n (A224854[n] = 0) '
                        f'has a neighbor (n-1 or n+1) with 0 to {max_markings} markings, up to n = {limit - 1}. '
                        'Probabilities are averaged over left and right neighbors. '
                        f'Total twin primes: {len(twin_prime_n)}.',
            ha='center', fontsize=10, wrap=True)

# Adjust layout
plt.tight_layout()
plt.subplots_adjust(bottom=0.2)
plt.show()

# Print probabilities
print("\nProbabilities of neighbor markings (averaged left and right):")
for i, prob in enumerate(prob_avg):
    if prob > 0:  # Only print non-zero probabilities for brevity
        print(f"Markings = {i}: {prob:.4f}")