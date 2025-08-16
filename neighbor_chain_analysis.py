import math
import numpy as np
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt
from collections import defaultdict

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

def compute_chain_neighbors(n_max, operators, k):
    """
    Compute neighbor probabilities for chain-specific and global transitions.
    
    Args:
        n_max (int): Maximum address to consider.
        operators (dict): Dictionary of operators for residue class k.
        k (int): Residue class (e.g., 7).
    
    Returns:
        results (dict): Composite, chain, and operator-specific metrics.
        hole_results (dict): Hole metrics.
        stats (dict): Statistical comparison results.
    """
    x_max = int(math.sqrt(n_max / 90)) + 2
    all_marked = set()
    operator_chains = defaultdict(list)
    operator_addresses = defaultdict(set)
    
    # Generate chains for each operator
    for a, l, m, p in operators[k]:
        op = (a, l, m, p)
        for x in range(1, x_max):
            n = a * x**2 - l * x + m
            if 0 <= n <= n_max:
                chain = [n]
                p_x = p + 90 * (x - 1) if p != 0 else 0
                if p_x > 0:
                    n_prime = n + p_x
                    while n_prime <= n_max:
                        chain.append(n_prime)
                        n_prime += p_x
                operator_chains[op].append(chain)
                operator_addresses[op].update(chain)
                all_marked.update(chain)
    
    # Compute holes and possibly prime addresses
    holes = set(range(n_max + 1)) - all_marked
    possibly_prime = {}
    for op, addrs in operator_addresses.items():
        possibly_prime[op] = sorted(set(range(n_max + 1)) - addrs - {0})
    
    # Global transition matrices (mod 7 for compatibility)
    mod7_trans_composite = np.zeros((7, 7))
    mod7_trans_holes = np.zeros((7, 7))
    
    # Specific address transitions
    specific_trans_composite = defaultdict(int)
    specific_trans_holes = defaultdict(int)
    small_n = [1, 4, 7, 8, 11, 14, 18, 21, 25, 28, 98]  # Expanded to include chain addresses
    
    # Composite global transitions
    sorted_composites = sorted(all_marked)
    for i in range(len(sorted_composites) - 1):
        n, n_next = sorted_composites[i], sorted_composites[i + 1]
        mod7, mod7_next = n % 7, n_next % 7
        mod7_trans_composite[mod7, mod7_next] += 1
        if n in small_n and n_next in small_n:
            specific_trans_composite[(n, n_next)] += 1
    
    # Hole transitions
    sorted_holes = sorted(holes)
    for i in range(len(sorted_holes) - 1):
        n, n_next = sorted_holes[i], sorted_holes[i + 1]
        mod7, mod7_next = n % 7, n_next % 7
        mod7_trans_holes[mod7, mod7_next] += 1
        if n in small_n and n_next in small_n:
            specific_trans_holes[(n, n_next)] += 1
    
    # Chain-specific transitions (all addresses)
    chain_trans = {}
    chain_mod_px_trans = {}
    for op, chains in operator_chains.items():
        chain_specific_trans = defaultdict(int)
        mod_px_trans = defaultdict(lambda: np.zeros((max([p + 90*(x-1) for x, chain in enumerate(chains, 1)]), max([p + 90*(x-1) for x, chain in enumerate(chains, 1)]))))
        for x, chain in enumerate(chains, 1):
            p_x = p + 90 * (x - 1) if p != 0 else 0
            if p_x == 0:
                continue
            for i in range(len(chain) - 1):
                n, n_next = chain[i], chain[i + 1]
                chain_specific_trans[(n, n_next)] += 1
                mod_px_trans[p_x][n % p_x, n_next % p_x] += 1
        chain_trans[op] = chain_specific_trans
        chain_mod_px_trans[op] = mod_px_trans
    
    # Normalize global transition matrices
    mod7_prob_composite = mod7_trans_composite / mod7_trans_composite.sum(axis=1, keepdims=True)
    mod7_prob_holes = mod7_trans_holes / mod7_trans_holes.sum(axis=1, keepdims=True)
    mod7_prob_composite = np.nan_to_num(mod7_prob_composite, nan=0.0)
    mod7_prob_holes = np.nan_to_num(mod7_prob_holes, nan=0.0)
    
    # Normalize specific transitions
    total_specific_composite = sum(specific_trans_composite.values())
    total_specific_holes = sum(specific_trans_holes.values())
    specific_prob_composite = {k: v / total_specific_composite if total_specific_composite > 0 else 0 for k, v in specific_trans_composite.items()}
    specific_prob_holes = {k: v / total_specific_holes if total_specific_holes > 0 else 0 for k, v in specific_trans_holes.items()}
    
    # Normalize chain-specific transitions
    chain_prob = {}
    chain_mod_px_prob = {}
    for op, trans in chain_trans.items():
        total = sum(trans.values())
        chain_prob[op] = {k: v / total if total > 0 else 0 for k, v in trans.items()}
    for op, mod_px_trans in chain_mod_px_trans.items():
        chain_mod_px_prob[op] = {}
        for p_x, trans_matrix in mod_px_trans.items():
            prob_matrix = trans_matrix / trans_matrix.sum(axis=1, keepdims=True)
            prob_matrix = np.nan_to_num(prob_matrix, nan=0.0)
            chain_mod_px_prob[op][p_x] = prob_matrix
    
    # Chi-square test for mod 7 transitions
    stats = {}
    try:
        chi2, p, _, _ = chi2_contingency(mod7_trans_composite + 1)  # Smoothing
        stats['chi_square_mod7'] = {'chi2': chi2, 'p_value': p}
    except:
        stats['chi_square_mod7'] = {'chi2': np.nan, 'p_value': np.nan}
    
    # Plot mod 7 transition matrices
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(mod7_prob_composite, cmap='viridis', interpolation='nearest')
    plt.title('Composite Mod 7 Transition Probabilities')
    plt.xlabel('Next n mod 7')
    plt.ylabel('Current n mod 7')
    plt.colorbar()
    
    plt.subplot(1, 2, 2)
    plt.imshow(mod7_prob_holes, cmap='viridis', interpolation='nearest')
    plt.title('Hole Mod 7 Transition Probabilities')
    plt.xlabel('Next n mod 7')
    plt.ylabel('Current n mod 7')
    plt.colorbar()
    plt.tight_layout()
    plt.savefig('mod7_chain_probabilities.png')
    plt.close()
    
    return {
        'composite': {
            'mod7_prob': mod7_prob_composite,
            'specific_prob': specific_prob_composite,
            'addresses': sorted_composites
        },
        'chains': chain_prob,
        'chain_mod_px': chain_mod_px_prob,
        'operators': operator_addresses,
        'possibly_prime': possibly_prime,
        'holes': {
            'mod7_prob': mod7_prob_holes,
            'specific_prob': specific_prob_holes,
            'addresses': sorted_holes
        },
        'stats': stats
    }

# Execute the analysis
n_max = 10000
k = 7
results = compute_chain_neighbors(n_max, operators, k)

# Print results
print("\nComposite Mod 7 Transition Probabilities:")
for i in range(7):
    for j in range(7):
        if results['composite']['mod7_prob'][i, j] > 0:
            print(f"  P(n mod 7 = {j} | n mod 7 = {i}) = {results['composite']['mod7_prob'][i, j]:.4f}")

print("\nHole Mod 7 Transition Probabilities:")
for i in range(7):
    for j in range(7):
        if results['holes']['mod7_prob'][i, j] > 0:
            print(f"  P(n mod 7 = {j} | n mod 7 = {i}) = {results['holes']['mod7_prob'][i, j]:.4f}")

print("\nComposite Specific Address Transitions:")
for (n, n_next), prob in results['composite']['specific_prob'].items():
    print(f"  P({n} to {n_next}) = {prob:.4f}")

print("\nHole Specific Address Transitions:")
for (n, n_next), prob in results['holes']['specific_prob'].items():
    print(f"  P({n} to {n_next}) = {prob:.4f}")

print("\nOperator (90, 82, -1, 7) Chain Transitions:")
op_7 = (90, 82, -1, 7)
for (n, n_next), prob in results['chains'][op_7].items():
    print(f"  P({n} to {n_next}) = {prob:.4f}")
print("\nOperator (90, 82, -1, 7) Mod p_x Transition Probabilities:")
for p_x, prob_matrix in results['chain_mod_px'][op_7].items():
    print(f"  p_x = {p_x}:")
    for i in range(prob_matrix.shape[0]):
        for j in range(prob_matrix.shape[1]):
            if prob_matrix[i, j] > 0:
                print(f"    P(n mod {p_x} = {j} | n mod {p_x} = {i}) = {prob_matrix[i, j]:.4f}")

print("\nOperator (90, 82, -1, 91) Chain Transitions:")
op_91 = (90, 82, -1, 91)
for (n, n_next), prob in results['chains'][op_91].items():
    print(f"  P({n} to {n_next}) = {prob:.4f}")
print("\nOperator (90, 82, -1, 91) Mod p_x Transition Probabilities:")
for p_x, prob_matrix in results['chain_mod_px'][op_91].items():
    print(f"  p_x = {p_x}:")
    for i in range(prob_matrix.shape[0]):
        for j in range(prob_matrix.shape[1]):
            if prob_matrix[i, j] > 0:
                print(f"    P(n mod {p_x} = {j} | n mod {p_x} = {i}) = {prob_matrix[i, j]:.4f}")

print("\nPossibly Prime Addresses (First 10 for Operator (90, 82, -1, 7)):")
print(results['possibly_prime'][op_7][:10])

print("\nStatistical Tests:")
print(f"  Chi-Square Test (Mod 7): chi2 = {results['stats']['chi_square_mod7']['chi2']:.2f}, p = {results['stats']['chi_square_mod7']['p_value']:.4f}")

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Composite Mod 7 Transition Matrix
composite_matrix = np.array([
    [0.0000, 0.6527, 0.2297, 0.0805, 0.0266, 0.0091, 0.0014],  # From 0
    [0.0032, 0.0000, 0.6588, 0.2296, 0.0762, 0.0247, 0.0075],  # From 1
    [0.0170, 0.0000, 0.0000, 0.6507, 0.2304, 0.0786, 0.0234],  # From 2
    [0.0425, 0.0000, 0.0000, 0.0000, 0.6412, 0.2325, 0.0839],  # From 3
    [0.1172, 0.0000, 0.0000, 0.0000, 0.0000, 0.6462, 0.2366],  # From 4
    [0.3344, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.6656],  # From 5
    [1.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000]   # From 6
])

# Hole Mod 7 Transition Matrix
hole_matrix = np.array([
    [0.0000, 1.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],  # From 0
    [0.0000, 0.0543, 0.3763, 0.2495, 0.1670, 0.0966, 0.0563],  # From 1
    [0.0000, 0.0967, 0.0453, 0.3436, 0.2716, 0.1502, 0.0926],  # From 2
    [0.0000, 0.0903, 0.0719, 0.0472, 0.3532, 0.2772, 0.1602],  # From 3
    [0.0000, 0.1667, 0.0964, 0.0783, 0.0422, 0.3695, 0.2470],  # From 4
    [0.0000, 0.2390, 0.1627, 0.1145, 0.0602, 0.0442, 0.3795],  # From 5
    [0.0000, 0.3674, 0.2359, 0.1608, 0.1273, 0.0752, 0.0334]   # From 6
])

# Plot Heatmaps
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

sns.heatmap(composite_matrix, annot=True, fmt=".4f", cmap="Blues", ax=ax1,
            xticklabels=range(7), yticklabels=range(7))
ax1.set_title("Composite Mod 7 Transition Probabilities")
ax1.set_xlabel("To (n mod 7)")
ax1.set_ylabel("From (n mod 7)")

sns.heatmap(hole_matrix, annot=True, fmt=".4f", cmap="Blues", ax=ax2,
            xticklabels=range(7), yticklabels=range(7))
ax2.set_title("Hole Mod 7 Transition Probabilities")
ax2.set_xlabel("To (n mod 7)")
ax2.set_ylabel("From (n mod 7)")

plt.tight_layout()
plt.show()