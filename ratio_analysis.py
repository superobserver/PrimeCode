import math
import numpy as np
from scipy.stats import ks_2samp, chi2_contingency
import matplotlib.pyplot as plt
from collections import defaultdict

def digital_root(x):
    """Compute the digital root of x (x mod 9, or 9 if x mod 9 == 0)."""
    return x % 9 if x % 9 != 0 else 9

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

def compute_ratios(n_max, operators, k):
    """
    Compute ratios (90n + 7)/n and fractional parts 7/n for composite and hole addresses.
    
    Args:
        n_max (int): Maximum address to consider.
        operators (dict): Dictionary of operators for residue class k.
        k (int): Residue class (e.g., 7).
    
    Returns:
        operator_results (list): Ratio metrics per operator.
        hole_results (dict): Ratio metrics for holes.
        stats (dict): Statistical comparison results.
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
                p_x = p + 90 * (x - 1) if p != 0 else 0
                if p_x > 0:
                    for n_prime in range(n, n_max + 1, p_x):
                        if 0 <= n_prime <= n_max:
                            marked.add(n_prime)
        all_marked.update(marked)
        
        ratios = []
        frac_parts = []
        dr_counts = {i: 0 for i in range(1, 10)}
        for n in marked:
            if n == 0:  # Skip undefined ratio
                continue
            ratio = (90 * n + 7) / n
            frac_part = 7 / n
            ratios.append(ratio)
            frac_parts.append(frac_part)
            dr = digital_root(int(np.floor(ratio)))
            dr_counts[dr] += 1
        
        total_dr = sum(dr_counts.values())
        dr_norm = {dr: count / total_dr if total_dr > 0 else 0 for dr, count in dr_counts.items()}
        
        mean_ratio = np.mean(ratios) if ratios else np.nan
        var_ratio = np.var(ratios) if ratios else np.nan
        mean_frac = np.mean(frac_parts) if frac_parts else np.nan
        var_frac = np.var(frac_parts) if frac_parts else np.nan
        
        operator_results.append({
            'operator': (a, l, m, p),
            'ratios': ratios,
            'frac_parts': frac_parts,
            'dr_frequencies': dr_norm,
            'mean_ratio': mean_ratio,
            'var_ratio': var_ratio,
            'mean_frac': mean_frac,
            'var_frac': var_frac,
            'num_addresses': len(marked)
        })
    
    # Compute hole metrics
    holes = set(range(n_max + 1)) - all_marked
    hole_ratios = []
    hole_frac_parts = []
    hole_dr_counts = {i: 0 for i in range(1, 10)}
    for n in holes:
        if n == 0:  # Skip undefined ratio
            continue
        ratio = (90 * n + 7) / n
        frac_part = 7 / n
        hole_ratios.append(ratio)
        hole_frac_parts.append(frac_part)
        dr = digital_root(int(np.floor(ratio)))
        hole_dr_counts[dr] += 1
    
    total_hole_dr = sum(hole_dr_counts.values())
    hole_dr_norm = {dr: count / total_hole_dr if total_hole_dr > 0 else 0 for dr, count in hole_dr_counts.items()}
    
    hole_mean_ratio = np.mean(hole_ratios) if hole_ratios else np.nan
    hole_var_ratio = np.var(hole_ratios) if hole_ratios else np.nan
    hole_mean_frac = np.mean(hole_frac_parts) if hole_frac_parts else np.nan
    hole_var_frac = np.var(hole_frac_parts) if hole_frac_parts else np.nan
    
    # Statistical comparison
    stats = {}
    # KS test for ratios
    all_composite_ratios = []
    for res in operator_results:
        all_composite_ratios.extend(res['ratios'])
    if all_composite_ratios and hole_ratios:
        ks_stat, ks_p = ks_2samp(all_composite_ratios, hole_ratios)
        stats['ks_test_ratios'] = {'statistic': ks_stat, 'p_value': ks_p}
    
    # KS test for fractional parts
    all_composite_frac = []
    for res in operator_results:
        all_composite_frac.extend(res['frac_parts'])
    if all_composite_frac and hole_frac_parts:
        ks_stat, ks_p = ks_2samp(all_composite_frac, hole_frac_parts)
        stats['ks_test_frac'] = {'statistic': ks_stat, 'p_value': ks_p}
    
    # Chi-square test for digital roots
    composite_dr_counts = {i: 0 for i in range(1, 10)}
    for res in operator_results:
        for dr, count in res['dr_frequencies'].items():
            composite_dr_counts[dr] += count * res['num_addresses']
    observed = np.array([[composite_dr_counts[dr], hole_dr_counts[dr]] for dr in range(1, 10)])
    try:
        chi2, chi2_p, _, _ = chi2_contingency(observed)
        stats['chi_square_dr'] = {'chi2': chi2, 'p_value': chi2_p}
    except ValueError:
        stats['chi_square_dr'] = {'chi2': np.nan, 'p_value': np.nan}
    
    # Plot histograms
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    for res in operator_results:
        if res['ratios']:
            plt.hist(res['ratios'], bins=50, alpha=0.3, label=f'Op {res["operator"]}', density=True)
    plt.hist(hole_ratios, bins=50, alpha=0.5, label='Holes', density=True)
    plt.xlabel('Ratio (90n + 7)/n')
    plt.ylabel('Density')
    plt.title(f'Ratio Distributions (k={k}, n_max={n_max})')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    for res in operator_results:
        if res['frac_parts']:
            plt.hist(res['frac_parts'], bins=50, alpha=0.3, label=f'Op {res["operator"]}', density=True)
    plt.hist(hole_frac_parts, bins=50, alpha=0.5, label='Holes', density=True)
    plt.xlabel('Fractional Part 7/n')
    plt.ylabel('Density')
    plt.title(f'Fractional Part Distributions (k={k}, n_max={n_max})')
    plt.legend()
    plt.tight_layout()
    plt.savefig('ratio_distributions.png')
    plt.close()
    
    return operator_results, {
        'ratios': hole_ratios,
        'frac_parts': hole_frac_parts,
        'dr_frequencies': hole_dr_norm,
        'mean_ratio': hole_mean_ratio,
        'var_ratio': hole_var_ratio,
        'mean_frac': hole_mean_frac,
        'var_frac': hole_var_frac
    }, stats

# Execute the analysis
n_max = 1000
k = 7
operator_results, hole_results, stats = compute_ratios(n_max, operators, k)

# Print results
for res in operator_results:
    print(f"\nOperator {res['operator']}:")
    print(f"  Number of addresses: {res['num_addresses']}")
    print(f"  Mean ratio: {res['mean_ratio']:.4f}")
    print(f"  Variance ratio: {res['var_ratio']:.4f}")
    print(f"  Mean fractional part: {res['mean_frac']:.4f}")
    print(f"  Variance fractional part: {res['var_frac']:.4f}")
    print(f"  Digital root frequencies: {res['dr_frequencies']}")
print(f"\nHoles:")
print(f"  Number of holes: {len(hole_results['ratios'])}")
print(f"  Mean ratio: {hole_results['mean_ratio']:.4f}")
print(f"  Variance ratio: {hole_results['var_ratio']:.4f}")
print(f"  Mean fractional part: {hole_results['mean_frac']:.4f}")
print(f"  Variance fractional part: {hole_results['var_frac']:.4f}")
print(f"  Digital root frequencies: {hole_results['dr_frequencies']}")
print(f"\nStatistical Tests:")
print(f"  KS Test (Ratios): statistic = {stats['ks_test_ratios']['statistic']:.4f}, p = {stats['ks_test_ratios']['p_value']:.4f}")
print(f"  KS Test (Fractional Parts): statistic = {stats['ks_test_frac']['statistic']:.4f}, p = {stats['ks_test_frac']['p_value']:.4f}")
print(f"  Chi-Square Test (DR): chi2 = {stats['chi_square_dr']['chi2']:.2f}, p = {stats['chi_square_dr']['p_value']:.4f}")

def ratio_bin_chi_square(operator_results, hole_results):
    bins = np.linspace(90, 100, 21)  # 20 bins from 90 to 100
    composite_counts, _ = np.histogram([r for res in operator_results for r in res['ratios']], bins=bins)
    hole_counts, _ = np.histogram(hole_results['ratios'], bins=bins)
    observed = np.array([composite_counts, hole_counts])
    try:
        chi2, p, _, _ = chi2_contingency(observed)
        return {'chi2': chi2, 'p_value': p}
    except:
        return {'chi2': np.nan, 'p_value': np.nan}
stats['chi_square_bins'] = ratio_bin_chi_square(operator_results, hole_results)