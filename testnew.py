import math


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def dr_ld_check(n):
    dr = n % 9 if n % 9 != 0 else 9
    ld = n % 10
    return dr in [1, 2, 4, 5, 7, 8] and ld in [1, 3, 7, 9]

operators_7 = [
    (90, 82, -1, 7), (90, 118, 37, 19), (90, 82, 17, 37), (90, 28, 2, 73),
    (90, 152, 64, 11), (90, 98, 25, 29), (90, 62, 9, 47), (90, 8, 0, 83),
    (90, 118, 35, 13), (90, 82, 15, 31), (90, 98, 23, 23), (90, 62, 7, 41),
    (90, 82, -1, 91), (90, 118, 37, 43), (90, 82, 17, 61), (90, 28, 2, 79),
    (90, 152, 64, 17), (90, 98, 25, 53), (90, 62, 9, 71), (90, 8, 0, 89),
    (90, 118, 35, 49), (90, 82, 15, 67), (90, 98, 23, 59), (90, 62, 7, 77)
]

n_max = 100
amplitude = [0] * (n_max + 1)
for a, l, m, p in operators_7:
    x_max = int(math.sqrt(n_max / a)) + 2
    marked_primes = set()
    for x in range(1, x_max):
        n = a * x**2 - l * x + m
        if 0 <= n <= n_max:
            p_base = 90 * n + 7
            if is_prime(p) and p * p == p_base and p not in marked_primes:
                amplitude[n] += 1
                marked_primes.add(p)
            elif not (is_prime(p) and p * p == p_base):
                amplitude[n] += 1
            p_x = p + 90 * (x - 1)
            for i in range(1, (n_max - n) // p_x + 1):
                n_new = n + i * p_x
                if n_new <= n_max:
                    amplitude[n_new] += 1

holes = [(90 * n + 7, "Prime" if is_prime(90 * n + 7) else f"Composite (Factors: {factorize(90 * n + 7)})") for n in range(n_max + 1) if amplitude[n] == 0]
print("Last 10 Holes for k = 7:")
for p, status in holes[-10:]:
    print(f"  {p}: {status}")
    for q in [n for n, a in enumerate(amplitude) if a > 0][:10]:  # Sample basis set
        diff = (p - 7) // 90 - q
        if diff >= 0 and dr_ld_check(diff):
            print(f"    Check n - q = {diff}: Eligible but not canceled elsewhere")

# Adjust prior script from "Last 1000 Terms" section
n_max = 23900001
limit = 2.15e9
amplitude = mark_composites(n_max, operators, coprime_24)
last_holes = get_last_holes(n_max, amplitude, coprime_24, limit, 1000)
for k in coprime_24:
    print(f"\nk = {k} (Last 5 of 1000):")
    for i, (p, status) in enumerate(last_holes[k][:5]):
        print(f"  {i+1}. {p}: {status}")