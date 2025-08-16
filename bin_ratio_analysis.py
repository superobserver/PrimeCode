import math
import numpy as np
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt
from collections import defaultdict

def digital_root(x):
    """Compute the digital root of x (x mod 9, or 9 if x mod 9 == 0)."""
    return x % 9 if x % 9 != 0 else 9

def sum_digital_root(n):
    """Compute the sum digital root of n (sum of digits mod 9)."""
    return digital_root(sum(int(d) for d in str(n)))

def leading_digital_root(n):
    """Compute the leading digital root of n (first digit mod 9)."""
    return digital_root(int(str(n)[0]))

def gcd(a, b):
    """Compute the greatest common divisor of a and b."""
    while b:
        a, b = b, a % b
    return a

# Operators for k = 7
operators = {
    7: [
        (90, 82, -1, 7), (90, 82, -1, 91), (90, 118, 37, 19), (90, 118, 37, 43),
        (90, 82, 17, 37), (90, 82, 17, 61), (90, 28, 2, 73), (90, 28, 2, 79),
        (90, 152, 64, 11), (90, 152, 64, 17), (90, 98, 25, 29), (90, 98, 25, 53),
        (90, 62, 9, 47), (90, 62, 9, 71), (90, 8, 0, 83), (90, 8, 0, 89),
        (90, 118, 35, 13), (90, 118, 35, 49), (90, 82, 15, 31), (90, 82, 15, 67),
        (90, 98, 23, 23), (90, 98, 23, 59), (90, 62, 7, 41), (90, 62, 7, 77)
    ]
}

def compute_neighbor_probabilities(n_max, operators, k):
    """
    Compute neighbor probabilities for LDR and SDR transitions for composites and holes.
    
    Args:
        n_max (int): Maximum address to consider.
        operators (dict): Dictionary of operators for residue class k.
        k (int): Residue class (e.g., 7).
    
    Returns:
        results (dict): Composite and operator-specific metrics.
        hole_results (dict): Hole metrics.
        stats (dict): Statistical comparison results.
    """
    x_max = int(math.sqrt(n_max / 90)) + 2
    all_marked = set()
    operator_addresses = defaultdict(set)
    
    # Generate composite addresses
    for idx, (a, l, m, p) in enumerate(operators[k]):
        marked = set()
        for x in range(1, x_max):
            n = a * x**2 - l * x + m
            if 0 <= n <= n_max:
                marked.add(n)
                p_x = p + 90 * (x - 1) if p != 0 else 0
                if p_x > 0:
                    for n_prime in range(n, n_max + 1, p_x):
                        if 0 <= n_prime <= n_max:
                            marked.add(n_prime)
        operator_addresses[(a, l, m, p)] = marked
        all_marked.update(marked)
    
    # Compute holes
    holes = set(range(n_max + 1)) - all_marked
    
    # Transition matrices (LDR and SDR)
    ldr_trans_composite = np.zeros((9, 9))  # Rows: current LDR, Columns: next LDR
    sdr_trans_composite = np.zeros((9, 9))
    ldr_trans_holes = np.zeros((9, 9))
    sdr_trans_holes = np.zeros((9, 9))
    
    # Operator-specific transitions
    operator_trans = {}
    
    # Composite transitions
    sorted_composites = sorted(all_marked)
    for i in range(len(sorted_composites) - 1):
        n, n_next = sorted_composites[i], sorted_composites[i + 1]
        ldr, ldr_next = leading_digital_root(n), leading_digital_root(n_next)
        sdr, sdr_next = sum_digital_root(n), sum_digital_root(n_next)
        ldr_trans_composite[ldr - 1, ldr_next - 1] += 1
        sdr_trans_composite[sdr - 1, sdr_next - 1] += 1
    
    # Hole transitions
    sorted_holes = sorted(holes)
    for i in range(len(sorted_holes) - 1):
        n, n_next = sorted_holes[i], sorted_holes[i + 1]
        ldr, ldr_next = leading_digital_root(n), leading_digital_root(n_next)
        sdr, sdr_next = sum_digital_root(n), sum_digital_root(n_next)
        ldr_trans_holes[ldr - 1, ldr_next - 1] += 1
        sdr_trans_holes[sdr - 1, sdr_next - 1] += 1
    
    # Operator-specific transitions
    for op, addresses in operator_addresses.items():
        sorted_addresses = sorted(addresses)
        ldr_trans_op = np.zeros((9, 9))
        sdr_trans_op = np.zeros((9, 9))
        for i in range(len(sorted_addresses) - 1):
            n, n_next = sorted_addresses[i], sorted_addresses[i + 1]
            ldr, ldr_next = leading_digital_root(n), leading_digital_root(n_next)
            sdr, sdr_next = sum_digital_root(n), sum_digital_root(n_next)
            ldr_trans_op[ldr - 1, ldr_next - 1] += 1
            sdr_trans_op[sdr - 1, sdr_next - 1] += 1
        operator_trans[op] = {'ldr': ldr_trans_op, 'sdr': sdr_trans_op}
    
    # Normalize transition matrices to probabilities
    ldr_prob_composite = ldr_trans_composite / ldr_trans_composite.sum(axis=1, keepdims=True)
    sdr_prob_composite = sdr_trans_composite / sdr_trans_composite.sum(axis=1, keepdims=True)
    ldr_prob_holes = ldr_trans_holes / ldr_trans_holes.sum(axis=1, keepdims=True)
    sdr_prob_holes = sdr_trans_holes / sdr_trans_holes.sum(axis=1, keepdims=True)
    
    # Handle NaNs (rows with no transitions)
    ldr_prob_composite = np.nan_to_num(ldr_prob_composite, nan=0.0)
    sdr_prob_composite = np.nan_to_num(sdr_prob_composite, nan=0.0)
    ldr_prob_holes = np.nan_to_num(ldr_prob_holes, nan=0.0)
    sdr_prob_holes = np.nan_to_num(sdr_prob_holes, nan=0.0)
    
    # Operator-specific probabilities
    operator_prob = {}
    for op in operator_trans:
        ldr_op = operator_trans[op]['ldr']
        sdr_op = operator_trans[op]['sdr']
        ldr_prob_op = ldr_op / ldr_op.sum(axis=1, keepdims=True)
        sdr_prob_op = sdr_op / sdr_op.sum(axis=1, keepdims=True)
        ldr_prob_op = np.nan_to_num(ldr_prob_op, nan=0.0)
        sdr_prob_op = np.nan_to_num(sdr_prob_op, nan=0.0)
        operator_prob[op] = {'ldr': ldr_prob_op, 'sdr': sdr_prob_op}
    
    # Chi-square test for transition matrices
    stats = {}
    try:
        chi2, p, _, _ = chi2_contingency(ldr_trans_composite + 1)  # Smoothing
        stats['chi_square_ldr'] = {'chi2': chi2, 'p_value': p}
    except:
        stats['chi_square_ldr'] = {'chi2': np.nan, 'p_value': np.nan}
    try:
        chi2, p, _, _ = chi2_contingency(sdr_trans_composite + 1)
        stats['chi_square_sdr'] = {'chi2': chi2, 'p_value': p}
    except:
        stats['chi_square_sdr'] = {'chi2': np.nan, 'p_value': np.nan}
    
    # Plot transition matrices
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(ldr_prob_composite, cmap='viridis', interpolation='nearest')
    plt.title('Composite LDR Transition Probabilities')
    plt.xlabel('Next LDR')
    plt.ylabel('Current LDR')
    plt.colorbar()
    
    plt.subplot(1, 2, 2)
    plt.imshow(ldr_prob_holes, cmap='viridis', interpolation='nearest')
    plt.title('Hole LDR Transition Probabilities')
    plt.xlabel('Next LDR')
    plt.ylabel('Current LDR')
    plt.colorbar()
    plt.tight_layout()
    plt.savefig('ldr_transition_probabilities.png')
    plt.close()
    
    return {
        'composite': {
            'ldr_prob': ldr_prob_composite,
            'sdr_prob': sdr_prob_composite,
            'addresses': sorted_composites
        },
        'operators': operator_prob,
        'holes': {
            'ldr_prob': ldr_prob_holes,
            'sdr_prob': sdr_prob_holes,
            'addresses': sorted_holes
        },
        'stats': stats
    }

# Execute the analysis
n_max = 10000
k = 7
results = compute_neighbor_probabilities(n_max, operators, k)

# Print results
print("\nComposite LDR Transition Probabilities:")
for i in range(9):
    for j in range(9):
        if results['composite']['ldr_prob'][i, j] > 0:
            print(f"  P(LDR={j+1} | LDR={i+1}) = {results['composite']['ldr_prob'][i, j]:.4f}")

print("\nHole LDR Transition Probabilities:")
for i in range(9):
    for j in range(9):
        if results['holes']['ldr_prob'][i, j] > 0:
            print(f"  P(LDR={j+1} | LDR={i+1}) = {results['holes']['ldr_prob'][i, j]:.4f}")

print("\nOperator (90, 82, -1, 91) LDR Transition Probabilities:")
op_91 = (90, 82, -1, 91)
for i in range(9):
    for j in range(9):
        if results['operators'][op_91]['ldr'][i, j] > 0:
            print(f"  P(LDR={j+1} | LDR={i+1}) = {results['operators'][op_91]['ldr'][i, j]:.4f}")

print("\nOperator (90, 82, 17, 37) LDR Transition Probabilities:")
op_37 = (90, 82, 17, 37)
for i in range(9):
    for j in range(9):
        if results['operators'][op_37]['ldr'][i, j] > 0:
            print(f"  P(LDR={j+1} | LDR={i+1}) = {results['operators'][op_37]['ldr'][i, j]:.4f}")

print("\nStatistical Tests:")
print(f"  Chi-Square Test (LDR): chi2 = {results['stats']['chi_square_ldr']['chi2']:.2f}, p = {results['stats']['chi_square_ldr']['p_value']:.4f}")
print(f"  Chi-Square Test (SDR): chi2 = {results['stats']['chi_square_sdr']['chi2']:.2f}, p = {results['stats']['chi_square_sdr']['p_value']:.4f}")