import math
from collections import defaultdict
import numpy as np
from scipy.stats import chi2_contingency

def digital_root(x):
    """Compute the digital root of x (x mod 9, or 9 if x mod 9 == 0)."""
    return x % 9 if x % 9 != 0 else 9

# Use the provided operators for k = 7
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

def per_operator_address_analysis(n_max, operators, k):
    """
    Analyze each operator's addresses for (sum DR, leading DR) pairs and normalized gap
    frequencies in the address space (digits of n).
    
    Args:
        n_max (int): Maximum address to consider.
        operators (dict): Dictionary of operators for residue class k.
        k (int): Residue class (e.g., 7).
    
    Returns:
        operator_results (list): Metrics per operator.
        hole_results (dict): Metrics for hole addresses.
    """
    x_max = int(math.sqrt(n_max / 90)) + 2
    operator_results = []
    all_marked = set()
    
    # Analyze each operator
    for idx, (a, l, m, p) in enumerate(operators[k]):
        marked = set()
        for x in range(1, x_max):
            n = a * x**2 - l * x + m
            if 0 <= n <= n_max:
                marked.add(n)
                all_marked.add(n)
                p_x = p + 90 * (x - 1) if p != 0 else 0
                if p_x > 0:
                    for n_prime in range(n, n_max + 1, p_x):
                        marked.add(n_prime)
                        all_marked.add(n_prime)
        
        pairs = set()
        gap_counts = {i: 0 for i in range(-9, 10)}
        total_gaps = 0
        
        for n in marked:
            digits = list(map(int, str(n)))  # Digits of address n
            gaps = [digits[i+1] - digits[i] for i in range(len(digits)-1)]
            sum_abs_gaps = sum(abs(g) for g in gaps)
            sum_dr = digital_root(sum_abs_gaps) if gaps else 0
            leading_dr = digital_root(sum(digits[:-1])) if len(digits) > 1 else 0
            pairs.add((sum_dr, leading_dr))
            for g in gaps:
                if g in gap_counts:
                    gap_counts[g] += 1
                    total_gaps += 1
        
        gap_norm = {g: count / total_gaps if total_gaps > 0 else 0 for g, count in gap_counts.items()}
        
        operator_results.append({
            'operator': (a, l, m, p),
            'pairs': sorted(pairs),
            'gap_frequencies': gap_norm,
            'num_addresses': len(marked),
            'gap_counts': gap_counts
        })
    
    # Compute hole metrics
    holes = set(range(n_max + 1)) - all_marked
    hole_pairs = set()
    hole_gap_counts = {i: 0 for i in range(-9, 10)}
    hole_total_gaps = 0
    
    for n in holes:
        digits = list(map(int, str(n)))  # Digits of address n
        gaps = [digits[i+1] - digits[i] for i in range(len(digits)-1)]
        sum_abs_gaps = sum(abs(g) for g in gaps)
        sum_dr = digital_root(sum_abs_gaps) if gaps else 0
        leading_dr = digital_root(sum(digits[:-1])) if len(digits) > 1 else 0
        hole_pairs.add((sum_dr, leading_dr))
        for g in gaps:
            if g in hole_gap_counts:
                hole_gap_counts[g] += 1
                hole_total_gaps += 1
    
    hole_gap_norm = {g: count / hole_total_gaps if hole_total_gaps > 0 else 0 for g, count in hole_gap_counts.items()}
    
    # Chi-square tests
    for res in operator_results:
        observed = np.array([[res['gap_counts'][g], hole_gap_counts[g]] for g in range(-9, 10)])
        try:
            chi2, p, _, _ = chi2_contingency(observed)
            res['chi_square'] = {'chi2': chi2, 'p': p}
        except ValueError:
            res['chi_square'] = {'chi2': float('nan'), 'p': float('nan')}
    
    return operator_results, {'pairs': sorted(hole_pairs), 'gap_frequencies': hole_gap_norm}

# Execute the analysis
n_max = 1000
k = 7
operator_results, hole_results = per_operator_address_analysis(n_max, operators, k)

# Print results
for res in operator_results:
    print(f"\nOperator {res['operator']}:")
    print(f"  Number of addresses: {res['num_addresses']}")
    print(f"  (sum DR, leading DR) pairs: {res['pairs']}")
    print(f"  Normalized gap frequencies: {res['gap_frequencies']}")
    print(f"  Chi-square test vs. holes: chi2 = {res['chi_square']['chi2']:.2f}, p = {res['chi_square']['p']:.4f}")
print(f"\nHoles:")
print(f"  (sum DR, leading DR) pairs: {hole_results['pairs']}")
print(f"  Normalized gap frequencies: {hole_results['gap_frequencies']}")