#!/usr/bin/env python
import time
from collections import Counter

# Configuration
k = 11
n_max = 2191  # Matches paper’s validation
operators = [
    (120, 34, 7, 53),   # z=1: 90x^2-120x+34
    (132, 48, 19, 29),  # z=2
    (120, 38, 17, 43),
    (90, 11, 13, 77),
    (78, -1, 11, 91),
    (108, 32, 31, 41),
    (90, 17, 23, 67),
    (72, 14, 49, 59),
    (60, 4, 37, 83),
    (60, 8, 47, 73),
    (48, 6, 61, 71),
    (12, 0, 79, 89)
]

# Digital root and last digit validation
def is_valid(num):
    dr = num
    while dr > 9:
        dr = sum(int(d) for d in str(dr))
    ld = num % 10
    return dr in [1, 2, 4, 5, 7, 8] and ld in [1, 3, 7, 9]

# Marking function for a single operator
def mark_chain(x, l, m, p, q, n_max):
    marked = set()
    # Quadratic insertion
    n = 90 * (x * x) - l * x + m
    if 0 <= n <= n_max:
        marked.add(n)
    # p_x-chain
    p_x = p + 90 * (x - 1)
    t_max_p = int((n_max - n) / p_x) + 1 if n <= n_max else 0
    for t in range(t_max_p):
        new_n = n + p_x * t
        if 0 <= new_n <= n_max and is_valid(90 * new_n + k):
            marked.add(new_n)
    # q_x-chain
    q_x = q + 90 * (x - 1)
    t_max_q = int((n_max - n) / q_x) + 1 if n <= n_max else 0
    for t in range(t_max_q):
        new_n = n + q_x * t
        if 0 <= new_n <= n_max and is_valid(90 * new_n + k):
            marked.add(new_n)
    return marked

# Simulate de-interlaced operators
start_time = time.time()
local_holes = []
global_amplitude = [0] * (n_max + 1)
x_max = int((n_max / 90) ** 0.5) + 2

for z, (l, m, p, q) in enumerate(operators, 1):
    marked = set()
    for x in range(1, x_max):
        marked.update(mark_chain(x, l, m, p, q, n_max))
    # Local holes: addresses not marked by this operator
    holes = [n for n in range(n_max + 1) if n not in marked]
    local_holes.append((z, holes))
    # Update global amplitude
    for n in marked:
        global_amplitude[n] += 1

# Global holes: addresses with amplitude 0
global_holes = [n for n, amp in enumerate(global_amplitude) if amp == 0]
global_hole_numbers = [90 * n + k for n in global_holes]
gaps = [global_holes[i+1] - global_holes[i] for i in range(len(global_holes)-1)]
dr_counts = Counter(sum(int(d) for d in str(num)) % 9 for num in global_hole_numbers)
ld_counts = Counter(num % 10 for num in global_hole_numbers)

# Analyze chain growth patterns
chain_patterns = []
for z, (l, m, p, q) in enumerate(operators, 1):
    insertions = []
    for x in range(1, min(5, x_max)):  # Limit to first 5 for brevity
        n = 90 * x * x - l * x + m
        if 0 <= n <= n_max:
            insertions.append(n)
    chain_patterns.append((z, p, q, insertions))

# Output
print(f"Number of global holes: {len(global_holes)} (expected 743)")
print(f"First 10 global holes (n): {global_holes[:10]}")
print(f"First 10 global hole numbers (90n+11): {global_hole_numbers[:10]}")
print(f"Global gap statistics: min={min(gaps, default=0)}, max={max(gaps, default=0)}, mean={sum(gaps)/len(gaps) if gaps else 0:.2f}")
print(f"Digital root distribution: {dict(dr_counts)}")
print(f"Last digit distribution: {dict(ld_counts)}")
print("\nLocal holes per operator (first 10 for each):")
for z, holes in local_holes:
    print(f"Operator {z}: {holes[:10]}... ({len(holes)} total)")
print("\nChain growth patterns (first 5 insertions per operator):")
for z, p, q, insertions in chain_patterns:
    print(f"Operator {z} (p={p}, q={q}): {insertions}")
print(f"Execution time: {time.time() - start_time:.2f} seconds")