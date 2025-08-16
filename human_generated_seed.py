#!/usr/bin/env python
import math
import cmath

def is_prime(n):
    """Check if n is a prime number."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def human_generated_seed(limit):
    """Generate A201804 sequence up to a computed limit."""
    # Compute epoch as per the original code
    h = int(limit)
    epoch = 90 * h * h - 12 * h + 1
    max_n = epoch  # Upper bound for n

    # Initialize amplitude map (zero-indexed list)
    amplitude_map = [0] * (max_n + 1)

    # Operators for k=11 from Table 8 (Page 25)
    operators = [
        (90, 120, 34, 7, 53),
        (90, 132, 48, 19, 29),
        (90, 120, 38, 17, 43),
        (90, 90, 11, 13, 77),
        (90, 78, -1, 11, 91),
        (90, 108, 32, 31, 41),
        (90, 90, 17, 23, 67),
        (90, 72, 14, 49, 59),
        (90, 60, 4, 37, 83),
        (90, 60, 8, 47, 73),
        (90, 48, 6, 61, 71),
        (90, 12, 0, 79, 89)
    ]

    # Mark composites using operators
    for a, l, m, p, q in operators:
        for x in range(1, int((max_n / 90) ** 0.5) + 2):
            n = a * x * x - l * x + m
            if 0 <= n <= max_n:
                amplitude_map[n] += 1
                # Mark multiples of p and q
                px = p + 90 * (x - 1)
                qx = q + 90 * (x - 1)
                for t in range(1, (max_n - n) // px + 1):
                    if n + t * px <= max_n:
                        amplitude_map[n + t * px] += 1
                for t in range(1, (max_n - n) // qx + 1):
                    if n + t * qx <= max_n:
                        amplitude_map[n + t * qx] += 1

    # Identify holes (primes, amplitude = 0)
    holes = [n for n in range(max_n + 1) if amplitude_map[n] == 0]
    primes = [90 * n + 11 for n in holes]
    composites = [n for n in range(max_n + 1) if amplitude_map[n] >= 1]

    return holes, primes, composites, amplitude_map

# Example usage
limit = input("Enter a number for limit (will be used to compute epoch): ")
holes, primes, composites, amplitude_map = human_generated_seed(limit)
print(f"Holes (n where amplitude = 0): {holes}")
print(f"Primes (90n + 11): {primes}")
print(f"Composites (n where amplitude >= 1): {composites[:10]}...")  # Truncate for brevity
print(f"Total energy (sum of amplitudes): {sum(amplitude_map)}")
print(f"This is the number of holes (sum of 0's): {len(holes)}")