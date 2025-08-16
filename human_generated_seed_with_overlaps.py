#!/usr/bin/env python
import math

def is_valid(num):
    """Check DR and LD constraints."""
    dr = sum(int(d) for d in str(num)) % 9
    ld = num % 10
    return dr in [1, 2, 4, 5, 7, 8] and ld in [1, 3, 7, 9]

def compute_overlaps(h):
    """Compute operator overlaps for A201804 in an epoch."""
    # Compute epoch
    n_max = 90 * h * h - 12 * h + 1

    # Initialize amplitude map and operator hit tracker
    amplitude_map = [0] * (n_max + 1)
    operator_hits = [[] for _ in range(n_max + 1)]  # Track which operators hit each n

    # Operators for k=11 (Table 8, Page 25)
    operators = [
        (90, 120, 34, 7, 53, 1),
        (90, 132, 48, 19, 29, 2),
        (90, 120, 38, 17, 43, 3),
        (90, 90, 11, 13, 77, 4),
        (90, 78, -1, 11, 91, 5),
        (90, 108, 32, 31, 41, 6),
        (90, 90, 17, 23, 67, 7),
        (90, 72, 14, 49, 59, 8),
        (90, 60, 4, 37, 83, 9),
        (90, 60, 8, 47, 73, 10),
        (90, 48, 6, 61, 71, 11),
        (90, 12, 0, 79, 89, 12)
    ]

    # Mark composites and track operator hits
    for a, l, m, p, q, op_id in operators:
        for x in range(1, int((n_max / 90) ** 0.5) + 2):
            n = a * x * x - l * x + m
            if 0 <= n <= n_max and is_valid(90 * n + 11):
                amplitude_map[n] += 1
                operator_hits[n].append(op_id)
                px = p + 90 * (x - 1)
                qx = q + 90 * (x - 1)
                for t in range(1, (n_max - n) // px + 1):
                    next_n = n + t * px
                    if next_n <= n_max and is_valid(90 * next_n + 11):
                        amplitude_map[next_n] += 1
                        operator_hits[next_n].append(op_id)
                for t in range(1, (n_max - n) // qx + 1):
                    next_n = n + t * qx
                    if next_n <= n_max and is_valid(90 * next_n + 11):
                        amplitude_map[next_n] += 1
                        operator_hits[next_n].append(op_id)

    # Compute overlaps (amplitude > 1)
    overlaps = sum(1 for n in range(n_max + 1) if amplitude_map[n] > 1)
    overlap_details = [(n, amplitude_map[n], operator_hits[n]) for n in range(n_max + 1) if amplitude_map[n] > 1]

    # Holes and primes
    holes = [n for n in range(n_max + 1) if amplitude_map[n] == 0]
    primes = [90 * n + 11 for n in holes]

    return {
        "n_max": n_max,
        "holes": holes,
        "primes": primes,
        "overlaps": overlaps,
        "overlap_details": overlap_details[:10],  # Limit for brevity
        "total_energy": sum(amplitude_map)
    }

# Example usage
h = int(input("Enter h for epoch (e.g., 2 for n_max=337): "))
result = compute_overlaps(h)
print(f"Epoch n_max: {result['n_max']}")
print(f"Holes (n where amplitude = 0): {len(result['holes'])}")
print(f"Primes (90n + 11): {result['primes'][:10]}...")
print(f"Number of overlaps (amplitude > 1): {result['overlaps']}")
print(f"Overlap details (n, amplitude, operator IDs): {result['overlap_details']}")
print(f"Total energy: {result['total_energy']}")
