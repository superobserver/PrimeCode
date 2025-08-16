import numpy as np
from scipy import optimize

# 24 primitive pairs
PRIMITIVES = [
    (91, 1, 1), (73, 1, 3), (37, 1, 7), (19, 1, 9),
    (11, 2, 1), (83, 2, 3), (47, 2, 7), (29, 2, 9),
    (31, 4, 1), (13, 4, 3), (67, 4, 7), (49, 4, 9),
    (41, 5, 1), (23, 5, 3), (77, 5, 7), (59, 5, 9),
    (61, 7, 1), (43, 7, 3), (7, 7, 7), (79, 7, 9),
    (71, 8, 1), (53, 8, 3), (17, 8, 7), (89, 8, 9)
]  # (z, DR, LD)

K = [1, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59, 61, 67, 71, 73, 77, 79, 83, 89]

def digital_root(n):
    return n if n < 10 else digital_root(sum(int(d) for d in str(n)))

def derive_operators(k):
    operators = []
    k_dr = digital_root(k)
    k_ld = k % 10
    for z1, dr1, ld1 in PRIMITIVES:
        for z2, dr2, ld2 in PRIMITIVES:
            if z1 == z2 and z1 != k:
                continue  # Skip non-k squares unless z1 = k
            # First n value
            d = z1 * z2
            n1 = d // 90
            p1 = 90 * n1 + k
            if p1 % 90 != z1 and p1 % 90 != z2:
                continue  # Must match z1 or z2 initially
            
            # Second n value
            x = 2 if z1 != z2 else 1  # Adjust x for squared terms
            z1_next = z1 + 90 * (x - 1)
            z2_next = z2 + 90 * (x - 1)
            d_next = z1_next * z2_next
            n2 = d_next // 90
            p2 = 90 * n2 + k
            if p2 % 90 != z1 and p2 % 90 != z2:
                continue
            
            # Solve for l, m
            # n1 = 90 - l + m (x=1)
            # n2 = 90x^2 - lx + m
            if z1 == z2:  # Squared term
                l = (90 * x**2 - n2 + 90 - n1) / (x - 1)
                m = n1 - 90 + l
            else:
                l = (90 * 4 - n2 + 90 - n1) / 3  # x=2
                m = n1 - 90 + l
            
            if not l.is_integer() or not m.is_integer():
                continue
            l, m = int(l), int(m)
            
            # Verify DR and LD preservation for composites
            valid = True
            for x_test in range(1, 3):
                n_test = 90 * x_test**2 - l * x_test + m
                if n_test >= 0:
                    p_test = 90 * n_test + k
                    if digital_root(p_test) != k_dr or p_test % 10 != k_ld:
                        valid = False
                        break
            if valid:
                operators.append((l, m, z1, z2))
    
    return operators[:14] if len(operators) > 14 else operators  # Limit to 14 if squares included

# Generate and validate operators
all_operators = {k: derive_operators(k) for k in K}
for k in all_operators:
    print(f"Operators for k={k}: {[(l, m, z1, z2) for l, m, z1, z2 in all_operators[k]]}")

# Compare with known operators (example for k=29)
known_operators_29 = [(60, -1, 29, 91), (150, 62, 11, 19), (96, 25, 37, 47), (24, 1, 73, 83),
                      (144, 57, 13, 23), (90, 20, 31, 59), (90, 22, 41, 49), (36, 3, 67, 77),
                      (156, 67, 7, 17), (84, 19, 43, 53), (30, 0, 61, 89), (30, 2, 71, 79)]
derived_operators_29 = all_operators[29]
print("\nComparison for k=29:")
print(f"Known: {[(l, m, z1, z2) for l, m, z1, z2 in known_operators_29]}")
print(f"Derived: {[(l, m, z1, z2) for l, m, z1, z2 in derived_operators_29]}")

# Generate holes
def is_composite_address(n, k, operators, n_max):
    p = 90 * n + k
    for l, m, z1, z2 in operators:
        a, b, c = 90, -l, m - n
        discriminant = b**2 - 4 * a * c
        if discriminant >= 0:
            x = (-b + np.sqrt(discriminant)) / (2 * a)
            if x > 0 and x == int(x) and 0 <= 90 * int(x)**2 - l * int(x) + m <= n_max:
                if p % 90 == z1 or p % 90 == z2:
                    return True
    return False

def generate_holes(n_max, k):
    holes = []
    for n in range(n_max + 1):
        if not is_composite_address(n, k, all_operators[k], n_max):
            prime = 90 * n + k
            holes.append(prime)
    return holes

n_max = 1000  # Test with smaller n_max first
all_holes = {k: generate_holes(n_max, k) for k in K}
for k in all_holes:
    print(f"Generated {len(all_holes[k])} holes for k={k}")

# Compute zeta sum and zeros
def zeta_k_approx(s, primes):
    return sum(p**(-s) for p in primes)

def zeta_sum_approx(s, all_holes):
    return (15/4) * sum(zeta_k_approx(s, all_holes[k]) for k in K)

def find_sum_zeros(t_range=(0, 30), num_points=1000):
    t_values = np.linspace(t_range[0], t_range[1], num_points)
    zeros = []
    for i in range(len(t_values) - 1):
        s1 = 0.5 + t_values[i] * 1j
        s2 = 0.5 + t_values[i + 1] * 1j
        z1 = zeta_sum_approx(s1, all_holes)
        z2 = zeta_sum_approx(s2, all_holes)
        if (z1.real * z2.real < 0) and (z1.imag * z2.imag < 0):
            def objective(t):
                s = 0.5 + t * 1j
                z = zeta_sum_approx(s, all_holes)
                return [z.real, z.imag]
            t_zero = optimize.root(objective, (t_values[i] + t_values[i + 1]) / 2).x[0]
            if 0 <= t_zero <= 30:
                zeros.append(0.5 + t_zero * 1j)
    return zeros

zeros_sum = find_sum_zeros()
print(f"Zeros of scaled sum: {[f'{z.real:.1f} + {z.imag:.4f}i' for z in zeros_sum]}")