import numpy as np

# 24 primitive pairs from Table 1
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
    
    # Pair k with all 24 primitives (and handle squares)
    for z1, dr1, ld1 in PRIMITIVES:
        for z2, dr2, ld2 in PRIMITIVES:
            # Include squared terms if z1 = z2 = k
            if z1 == z2 and z1 != k:
                continue  # Skip non-k squares unless z1 = k
            
            # First n value
            d = z1 * z2
            n1 = d // 90
            p1 = 90 * n1 + k
            if p1 % 90 != z1 and p1 % 90 != z2:
                continue
            
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
    
    # Limit to 14 operators if needed
    return operators[:14] if len(operators) > 14 else operators

# Generate operators for all k
all_operators = {k: derive_operators(k) for k in K}

# Output operators in requested format
for k in K:
    print(f"\nOperators for k={k}:")
    for l, m, z1, z2 in all_operators[k]:
        print(f"⟨{l}, {m}, {z1}, {z2}⟩")

# Example comparison for k=29 with known values
known_operators_29 = [(60, -1, 29, 91), (150, 62, 11, 19), (96, 25, 37, 47), (24, 1, 73, 83),
                      (144, 57, 13, 23), (90, 20, 31, 59), (90, 22, 41, 49), (36, 3, 67, 77),
                      (156, 67, 7, 17), (84, 19, 43, 53), (30, 0, 61, 89), (30, 2, 71, 79)]
print(f"\nComparison for k=29:")
print("Known operators:")
for l, m, z1, z2 in known_operators_29:
    print(f"⟨{l}, {m}, {z1}, {z2}⟩")
print("Derived operators:")
for l, m, z1, z2 in all_operators[29]:
    print(f"⟨{l}, {m}, {z1}, {z2}⟩")