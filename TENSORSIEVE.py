#!/usr/bin/env python
import numpy as np

# User input for n_max
n_max = int(input("Enter upper limit (n_max): "))
k = 11

# Operators for k=11 from Table 3 (Section 3.1): [a, l, m, p, q]
operators_k11 = [
    [120, 106, 34, 7, 53],  # z=1
    [132, 108, 48, 19, 29], # z=2
    [120, 98, 38, 17, 43],  # z=3
    [90, 79, 11, 13, 77],   # z=4
    [78, 79, -1, 11, 91],  # z=5
    [108, 86, 32, 31, 41],  # z=6
    [90, 73, 17, 23, 67],   # z=7
    [72, 58, 14, 49, 59],   # z=8
    [60, 56, 4, 37, 83],    # z=9
    [60, 52, 8, 47, 73],    # z=10
    [48, 42, 6, 61, 71],    # z=11
    [12, 12, 0, 79, 89]     # z=12
]

print(f"Processing n_max: {n_max}")

def generate_marking_map(n_max, k, operators):
    # Initialize amplitude array (0 for holes, >=1 for composites)
    marked = np.zeros(n_max + 1, dtype=np.int32)
    
    # Process each operator
    for a, l, m, p, q in operators:
        # Generate x values up to sqrt(n_max / 90) + 2
        x = np.arange(1, int(np.sqrt(n_max / 90)) + 2)
        # Quadratic operator: n = a*x^2 - l*x + m
        n = a * x**2 - l * x + m
        # Filter valid n within range [0, n_max]
        valid_n = n[(n >= 0) & (n <= n_max)]
        
        # Mark base composites
        marked[valid_n] += 1
        
        # Generate periodic multiples for p and q
        for period in [p, q]:
            # Maximum i for each valid_n to stay within n_max
            i_max = (n_max - valid_n) // period + 1
            # Use the largest i_max to ensure coverage
            i = np.arange(np.max(i_max))
            # Compute all multiples at once
            multiples = valid_n[:, None] + period * i[None, :]
            # Flatten and filter within range
            valid_multiples = multiples[(multiples <= n_max)].ravel()
            # Mark periodic composites
            marked[valid_multiples] += 1
    
    # Holes are where amplitude = 0
    holes = np.where(marked == 0)[0]
    # Primes are 90n + k
    primes = 90 * holes + k
    return holes, primes, marked

# Execute the sieve
holes, primes, amplitudes = generate_marking_map(n_max, k, operators_k11)

# Print results
print("Holes (n):", holes.tolist())
print("Primes (90n + k):", primes.tolist())
print("Number of holes:", len(holes))
# Optional: Print amplitudes (uncomment if needed, might be large)
# print("Amplitudes:", amplitudes.tolist())