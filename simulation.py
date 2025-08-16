import math
import matplotlib.pyplot as plt

# Approximate Li(N)
def li(n):
    return n / math.log(n)  # Simplified, accurate for large N

# Known prime counts for validation
known_pi = {100: 25, 1000: 168, 10000: 1229, 100000: 9592, 1000000: 78498}

# Primes for k = 11 (A201804 subset)
def is_prime(n):
    if n < 2: return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0: return False
    return True

# Full sieve simulation (simplified operators)
def full_sieve(N, k=11):
    n_max = (N - k) // 90
    marked = set()
    operators = [(120, 34, 7, 13), (60, 11, 11, 19), (80, 17, 17, 23), (100, 29, 29, 31)]  # Subset for demo
    for l, m, z, o in operators:
        x_max = int(math.sqrt(N / 90)) + 1
        for x in range(1, x_max + 1):
            n = 90 * x**2 - l * x + m
            if 0 <= n <= n_max and 90 * n + k == (z + 90 * (x - 1)) * (o + 90 * (x - 1)):
                marked.add(n)
    primes = [n for n in range(n_max + 1) if n not in marked and is_prime(90 * n + k)]
    return len(primes), n_max + 1 - len(primes)

# Leaky sieve (omit first 4 operators)
def leaky_sieve(N, k=11):
    n_max = (N - k) // 90
    marked = set()
    operators = [(120, 34, 7, 13), (60, 11, 11, 19), (80, 17, 17, 23), (100, 29, 29, 31)]
    for l, m, z, o in operators[4:]:  # Omit 4
        x_max = int(math.sqrt(N / 90)) + 1
        for x in range(1, x_max + 1):
            n = 90 * x**2 - l * x + m
            if 0 <= n <= n_max and 90 * n + k == (z + 90 * (x - 1)) * (o + 90 * (x - 1)):
                marked.add(n)
    primes = [n for n in range(n_max + 1) if n not in marked and is_prime(90 * n + k)]
    return len(primes)

# Simulation
N_values = [100, 1000, 10000, 100000, 1000000]
full_pi, leaky_pi, composites, zeta_uncorr, zeta_corr = [], [], [], [], []

for N in N_values:
    pi_full, c_full = full_sieve(N)
    pi_leaky = leaky_sieve(N)
    full_pi.append(pi_full)
    leaky_pi.append(pi_leaky)
    composites.append(c_full)
    zeta_uncorr.append(li(N) / 24)  # Uncorrected zeta per class
    zeta_corr.append(known_pi[N] / 24)  # Corrected zeta per class

# Plotting
plt.figure(figsize=(10, 6))
plt.loglog(N_values, full_pi, label="Full Sieve \( \pi_{90,11}(N) \)", marker='o')
plt.loglog(N_values, leaky_pi, label="Leaky Sieve \( \pi'_{90,11}(N) \)", marker='x')
plt.loglog(N_values, composites, label="Sieve Composites \( |C_{11}(N)| \)", marker='s')
plt.loglog(N_values, zeta_uncorr, label="Lossy Zeta \( \text{Li}(N)/24 \)", marker='^')
plt.loglog(N_values, zeta_corr, label="Complete Zeta \( \pi(N)/24 \)", marker='*')
plt.xlabel("N (log scale)")
plt.ylabel("Count (log scale)")
plt.legend()
plt.title("Complementarity: Quadratic Sieve vs. Zeta Function")
plt.grid(True, which="both", ls="--")
plt.show()

# Print results
print("N\tFull π\tLeaky π\t|C_{11}|\tLi(N)/24\tπ(N)/24")
for i, N in enumerate(N_values):
    print(f"{N}\t{full_pi[i]}\t{leaky_pi[i]}\t{composites[i]}\t{zeta_uncorr[i]:.2f}\t{zeta_corr[i]:.2f}")