#!/usr/bin/env python
import math
from collections import defaultdict
import numpy as np

def is_valid(num):
    """Check DR and LD constraints."""
    dr = sum(int(d) for d in str(num)) % 9
    ld = num % 10
    return dr in [1, 2, 4, 5, 7, 8] and ld in [1, 3, 7, 9]

def compute_overlaps_and_variance(h, silo_width=1000):
    """Compute operator overlaps, amplitude variance, and energy for A201804."""
    # Compute epoch
    n_max = 90 * h * h - 12 * h + 1

    # Initialize maps
    amplitude_map = [0] * (n_max + 1)
    operator_hits = [[] for _ in range(n_max + 1)]  # Track operator IDs
    frequency_overlaps = defaultdict(lambda: defaultdict(int))  # Track overlaps per prime

    # Operators for k=11 (Table 8, Page 25) with extended primes for epoch
    base_operators = [
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

    # Extend operators for higher epochs (e.g., 7 -> 97, 11 -> 101)
    operators = []
    max_x = int((n_max / 90) ** 0.5) + 2
    for a, l, m, p, q, op_id in base_operators:
        operators.append((a, l, m, p, q, op_id))
        for i in range(1, max_x):
            new_p = p + 90 * i
            new_q = q + 90 * i
            new_m = m  # Simplified; m may need adjustment per document
            if is_valid(new_p) and is_valid(new_q):
                operators.append((a, l, new_m, new_p, new_q, op_id + 100 * i))

    # Mark composites and track overlaps
    for a, l, m, p, q, op_id in operators:
        for x in range(1, max_x):
            n = a * x * x - l * x + m
            if 0 <= n <= n_max and is_valid(90 * n + 11):
                amplitude_map[n] += 1
                operator_hits[n].append(op_id)
                frequency_overlaps[p][n] += 1
                frequency_overlaps[q][n] += 1
                px = p + 90 * (x - 1)
                qx = q + 90 * (x - 1)
                for t in range(1, (n_max - n) // px + 1):
                    next_n = n + t * px
                    if next_n <= n_max and is_valid(90 * next_n + 11):
                        amplitude_map[next_n] += 1
                        operator_hits[next_n].append(op_id)
                        frequency_overlaps[p][next_n] += 1
                for t in range(1, (n_max - n) // qx + 1):
                    next_n = n + t * qx
                    if next_n <= n_max and is_valid(90 * next_n + 11):
                        amplitude_map[next_n] += 1
                        operator_hits[next_n].append(op_id)
                        frequency_overlaps[q][next_n] += 1

    # Compute holes and primes
    holes = [n for n in range(n_max + 1) if amplitude_map[n] == 0]
    primes = [90 * n + 11 for n in holes]

    # Compute amplitude variance across silos
    silo_amplitudes = []
    for start in range(0, n_max + 1, silo_width):
        end = min(start + silo_width - 1, n_max)
        silo = amplitude_map[start:end + 1]
        silo_amplitudes.append(np.var(silo) if silo else 0)

    # Sum of reciprocals of prime frequencies
    frequency_primes = set()
    for _, _, _, p, q, _ in operators:
        frequency_primes.add(p)
        frequency_primes.add(q)
    reciprocal_sum = sum(1.0 / p for p in frequency_primes if p != 0)

    # Zero-to-amplitude ratio
    zero_count = len(holes)
    total_amplitude = sum(amplitude_map)
    zero_to_amplitude_ratio = zero_count / total_amplitude if total_amplitude > 0 else 0

    # Overlap tree for each frequency (e.g., p=7)
    overlap_trees = {}
    for p in frequency_primes:
        overlap_trees[p] = {}
        for n in range(n_max + 1):
            if frequency_overlaps[p][n] > 0:
                overlap_trees[p][n] = [op_id for op_id in operator_hits[n] if n in frequency_overlaps[p]]

    return {
        "n_max": n_max,
        "holes": len(holes),
        "primes": primes[:10],
        "total_energy": total_amplitude,
        "zero_to_amplitude_ratio": zero_to_amplitude_ratio,
        "reciprocal_sum": reciprocal_sum,
        "silo_variances": silo_amplitudes[:10],  # Limit for brevity
        "overlap_trees": {p: list(overlap_trees[p].items())[:5] for p in list(overlap_trees.keys())[:3]},  # Sample for p=7, etc.
        "overlaps": sum(1 for n in range(n_max + 1) if amplitude_map[n] > 1),
        "overlap_details": [(n, amplitude_map[n], operator_hits[n]) for n in range(n_max + 1) if amplitude_map[n] > 1][:5]
    }

# Example usage
h = int(input("Enter h for epoch (e.g., 2 for n_max=337): "))
result = compute_overlaps_and_variance(h)
print(f"Epoch n_max: {result['n_max']}")
print(f"Number of holes: {result['holes']}")
print(f"Primes (90n + 11): {result['primes']}...")
print(f"Total energy: {result['total_energy']}")
print(f"Zero-to-amplitude ratio: {result['zero_to_amplitude_ratio']:.6f}")
print(f"Sum of reciprocals of prime frequencies: {result['reciprocal_sum']:.6f}")
print(f"Silo variances (first 10): {result['silo_variances']}")
print(f"Number of overlaps: {result['overlaps']}")
print(f"Overlap details (n, amplitude, operator IDs): {result['overlap_details']}")
print(f"Overlap trees (sample for 3 primes): {result['overlap_trees']}")