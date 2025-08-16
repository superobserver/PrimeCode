import cmath
import math

def mark_composites(n_max, operators):
    """Generate holes (primes) for k=11."""
    marked = [0] * (n_max + 1)
    for a, l, m, p, q in operators:
        for x in range(1, int((n_max / 90) ** 0.5) + 2):
            n = a * x**2 - l * x + m
            if 0 <= n <= n_max:
                marked[n] += 1
                p_x = p + 90 * (x - 1)
                q_x = q + 90 * (x - 1)
                for i in range(1, (n_max - n) // p_x + 1):
                    if n + i * p_x <= n_max:
                        marked[n + i * p_x] += 1
                for i in range(1, (n_max - n) // q_x + 1):
                    if n + i * q_x <= n_max:
                        marked[n + i * q_x] += 1
    return [n for n in range(n_max + 1) if marked[n] == 0]

# Operators for k=11 (Table 8)
operators_k11 = [
    (90, 120, 34, 7, 53), (90, 132, 48, 19, 29), (90, 120, 38, 17, 43),
    (90, 90, 11, 13, 77), (90, 78, -1, 11, 91), (90, 108, 32, 31, 41),
    (90, 90, 17, 23, 67), (90, 72, 14, 49, 59), (90, 60, 4, 37, 83),
    (90, 60, 8, 47, 73), (90, 48, 6, 61, 71), (90, 12, 0, 79, 89)
]

zeta_zeros = {1: 14.134725, 2: 21.022040, 3: 25.010858, 4: 30.424876, 5: 32.935062}

print("Using k=11 (fixed by operators)")
n_max = int(input("Enter n_max (e.g., 20000): "))
print("Known zeta zeros:")
for i, t in zeta_zeros.items():
    print(f"{i}: t = {t}")
choice = input("Enter a number (1-5) to select a zero, 0 for custom t, or a float for direct t: ")

try:
    zero_choice = int(choice)
    if zero_choice == 0:
        t = float(input("Enter custom imaginary part t: "))
    elif zero_choice in zeta_zeros:
        t = zeta_zeros[zero_choice]
    else:
        print("Invalid choice, using default t = 14.134725")
        t = 14.134725
except ValueError:
    t = float(choice)

# Generate holes up to n_max
k = 11
holes = mark_composites(n_max, operators_k11)
print(f"Total holes up to {n_max}: {len(holes)}")
print(f"First few addresses (n): {holes[:5]}")
print(f"Corresponding primes: {[90 * n + k for n in holes[:5]]}")

# Compute zeta_11(s) at intervals
s = 0.5 + t * 1j
interval = 100
zeta_values = {}
for i, n in enumerate(holes):
    if i == 0:
        zeta_k = 0
    term = n ** (-s) if n > 0 else 0
    zeta_k += term
    if (i + 1) % interval == 0 or i == len(holes) - 1:
        n_max_at_interval = holes[i]
        zeta_values[n_max_at_interval] = zeta_k
        print(f"n={n_max_at_interval}, holes so far={i+1}, zeta_11(s)={zeta_k}, |zeta_11(s)|={abs(zeta_k):.6f}")

# Final result
final_zeta = zeta_values[holes[-1]]
print(f"\nFinal s = {s}")
print(f"Final zeta_11(s) up to {n_max} = {final_zeta}")
print(f"Final |zeta_11(s)| = {abs(final_zeta):.6f}")

# Probing around t for final zeta
print("\nProbing final zeta around", t)
t_values = [t - 0.005, t - 0.001, t, t + 0.001, t + 0.005]
for t_probe in t_values:
    s_probe = 0.5 + t_probe * 1j
    zeta_probe = sum(n ** (-s_probe) if n > 0 else 0 for n in holes)
    print(f"t = {t_probe:.6f}, |zeta_11(s)| = {abs(zeta_probe):.6f}")