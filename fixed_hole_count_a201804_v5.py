#!/usr/bin/env python
import math
from collections import defaultdict
import numpy as np

def drLD(x, l, m, z, listvar):
    """Composite generating function for A201804."""
    y = 90 * (x * x) - l * x + m
    if 0 <= y < len(listvar):
        listvar[y] += 1
    p = z + 90 * (x - 1)
    for n in range(1, int(((len(listvar) - 1 - y) / p) + 1)):
        next_y = y + p * n
        if 0 <= next_y < len(listvar):
            listvar[next_y] += 1

def compute_overlaps_and_variance(h, silo_width=1000, validate_n=1000):
    """Compute operator overlaps, amplitude variance, and energy for A201804."""
    # Compute epoch
    n_max = 90 * h * h - 12 * h + 1

    # Initialize amplitude map
    amplitude_map = [0] * (n_max + 1)
    operator_hits = [[] for _ in range(n_max + 1)]
    frequency_overlaps = defaultdict(lambda: defaultdict(int))
    operator_indices = defaultdict(list)  # Independent lists for each operator

    # Operators for k=11 (Table 8, Page 25)
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

    # Extend operators
    operators = []
    max_x = int((n_max / 90) ** 0.5) + 2
    max_prime = int(math.sqrt(90 * n_max)) + 1
    for a, l, m, p, q, op_id in base_operators:
        operators.append((a, l, m, p, q, op_id))
        i = 1
        while True:
            new_p = p + 90 * i
            new_q = q + 90 * i
            if new_p > max_prime or new_q > max_prime:
                break
            operators.append((a, l, m, new_p, new_q, op_id + 100 * i))
            i += 1

    # Mark composites and track independent lists
    for a, l, m, p, q, op_id in operators:
        indices = []
        for x in range(1, max_x):
            n = a * x * x - l * x + m
            if 0 <= n <= n_max:
                indices.append(n)
                amplitude_map[n] += 1
                operator_hits[n].append(op_id)
                frequency_overlaps[p][n] += 1
                frequency_overlaps[q][n] += 1
            px = p + 90 * (x - 1)
            qx = q + 90 * (x - 1)
            for t in range(1, int((n_max - n) / px) + 1):
                next_n = n + t * px
                if 0 <= next_n <= n_max:
                    indices.append(next_n)
                    amplitude_map[next_n] += 1
                    operator_hits[next_n].append(op_id)
                    frequency_overlaps[p][next_n] += 1
            for t in range(1, int((n_max - n) / qx) + 1):
                next_n = n + t * qx
                if 0 <= next_n <= n_max:
                    indices.append(next_n)
                    amplitude_map[next_n] += 1
                    operator_hits[next_n].append(op_id)
                    frequency_overlaps[q][next_n] += 1
        operator_indices[op_id] = sorted(list(set(indices)))

    # Compute holes (zeros in amplitude map)
    holes = [n for n in range(n_max + 1) if amplitude_map[n] == 0]
    primes = [90 * n + 11 for n in holes]

    # Validation against original output
    validation_amplitudes = [
        (4, 31), (6, 31), (8, 31), (11, 63), (14, 31)
    ]
    validation_result = {
        "matches": True,
        "mismatches": []
    }
    for n, expected_amp in validation_amplitudes:
        if n <= validate_n and amplitude_map[n] != expected_amp:
            validation_result["matches"] = False
            validation_result["mismatches"].append((n, amplitude_map[n], expected_amp))

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

    # Overlap tree
    overlap_trees = {}
    for p in frequency_primes:
        overlap_trees[p] = {}
        for n in range(n_max + 1):
            if frequency_overlaps[p][n] > 0:
                overlap_trees[p][n] = [op_id for op_id in operator_hits[n]]

    return {
        "n_max": n_max,
        "holes": len(holes),
        "primes": primes[:10],
        "total_energy": total_amplitude,
        "zero_to_amplitude_ratio": zero_to_amplitude_ratio,
        "reciprocal_sum": reciprocal_sum,
        "silo_variances": silo_amplitudes[:10],
        "overlaps": sum(1 for n in range(n_max + 1) if amplitude_map[n] > 1),
        "overlap_details": [(n, amplitude_map[n], operator_hits[n]) for n in range(n_max + 1) if amplitude_map[n] > 1][:5],
        "overlap_trees": {p: list(overlap_trees[p].items())[:5] for p in list(overlap_trees.keys())[:3]},
        "validation": validation_result,
        "operator_indices": {op_id: indices[:10] for op_id, indices in operator_indices.items()}
    }

# Run for h=30
h = 30
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
print(f"Validation result: {result['validation']}")
print(f"Operator indices (first 10 for each operator): {result['operator_indices']}")
