import numpy as np
import matplotlib.pyplot as plt

# Operators for k=11 (simplified subset for visualization)
OPERATORS_K11 = [
    (120, 34, 7, 13),  # n = 90x^2 - 120x + 34
    (60, 11, 11, 19),  # n = 90x^2 - 60x + 11
    (48, 7, 17, 23),   # n = 90x^2 - 48x + 7
]

n_max = 100
n_values = np.arange(n_max + 1)
k = 11

# Generate signals for each operator
signals = []
for l, m, z1, z2 in OPERATORS_K11:
    signal = np.zeros_like(n_values, dtype=float)
    for x in range(1, int(np.sqrt(n_max / 90)) + 1):
        n = 90 * x**2 - l * x + m
        if 0 <= n <= n_max:
            p = 90 * n + k
            if p % 90 == z1 or p % 90 == z2:  # Signal peaks at composite addresses
                signal[n] = 1.0  # Normalized amplitude per signal
    signals.append(signal)

# Compute total amplitude (constructive interference)
total_amplitude = np.sum(signals, axis=0)

# Identify holes (amplitude = 0)
holes = n_values[total_amplitude == 0]
hole_primes = 90 * holes + k

# Plotting
plt.figure(figsize=(12, 6))
for i, signal in enumerate(signals):
    plt.plot(n_values, signal + i * 1.5, label=f"Operator {i+1}", alpha=0.5)
plt.plot(n_values, total_amplitude, 'k-', lw=2, label="Total Amplitude")
plt.scatter(holes, np.zeros_like(holes), color='red', label="Holes (Primes)", zorder=5)
plt.xlabel("Address \( n \)")
plt.ylabel("Signal Amplitude")
plt.title("Quadratic Sieve Signals for \( k = 11 \), \( n_{\max} = 100 \)")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

# Print some results
print("Holes (n):", holes)
print("Corresponding Primes (90n + 11):", hole_primes)