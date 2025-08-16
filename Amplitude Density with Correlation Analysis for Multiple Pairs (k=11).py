#!/usr/bin/env python
import time
from collections import defaultdict
import matplotlib.pyplot as plt
from sympy import isprime, factorint
from scipy.stats import pearsonr

# Configuration
k = 11
n_max = 2191
operators = [
    (120, 34, 7, 53),   # z=1
    (132, 48, 19, 29),
    (120, 38, 17, 43),
    (90, 11, 13, 77),
    (78, -1, 11, 91),
    (108, 32, 31, 41),
    (90, 17, 23, 67),
    (72, 14, 49, 59),
    (60, 4, 37, 83),
    (60, 8, 47, 73),
    (48, 6, 61, 71),
    (12, 0, 79, 89)
]

# Start timing
start_time = time.time()

# Compute insertion addresses and factors for all x
x_max = 5  # From prior calculation
channels = []
for z, (l, m, p_z, q_z) in enumerate(operators, 1):
    for x in range(1, x_max + 1):
        y_x = 90 * x * x - l * x + m
        if 0 <= y_x <= n_max:
            p_x = p_z + 90 * (x - 1)
            q_x = q_z + 90 * (x - 1)
            channels.append((z, x, y_x, p_x, 'p'))
            channels.append((z, x, y_x, q_x, 'q'))

# Compute amplitude for each address
amplitude = defaultdict(int)
total_marks = 0
for z, x, y_x, step, channel_type in channels:
    if y_x < 5:
        t_start = (5 - y_x + step - 1) // step
    else:
        t_start = 0
    t_max = (n_max - y_x) // step
    for t in range(t_start, t_max + 1):
        n = y_x + t * step
        if 5 <= n <= n_max:
            amplitude[n] += 1
            total_marks += 1
        else:
            break

# Verify total marks
print(f"Total Marks: {total_marks} (Expected: 2437)")

# Compute distribution of amplitudes
amplitude_distribution = defaultdict(int)
for n in range(5, n_max + 1):
    amp = amplitude[n]
    amplitude_distribution[amp] += 1

# Output distribution
print("Amplitude Distribution:")
total_addresses = n_max - 5 + 1
for amp in sorted(amplitude_distribution.keys()):
    count = amplitude_distribution[amp]
    percentage = (count / total_addresses) * 100
    print(f"Amplitude {amp}: {count} addresses ({percentage:.2f}%)")

# Verify semiprime property for amplitude 1
print("\nVerifying Semiprime Property for Amplitude 1:")
semiprime_violations = 0
for n in range(5, n_max + 1):
    if amplitude[n] == 1:
        num = 90 * n + k
        factors = factorint(num)
        if len(factors) != 2 or any(exp != 1 for exp in factors.values()):
            semiprime_violations += 1
            print(f"Address {n} (90n+k = {num}) has amplitude 1 but is not a semiprime: {factors}")
            if semiprime_violations >= 5:
                print("Stopping after 5 violations...")
                break
if semiprime_violations == 0:
    print("All addresses with amplitude 1 are semiprimes.")
else:
    print(f"Found {semiprime_violations} addresses with amplitude 1 that are not semiprimes.")

# Evaluate amplitude 0 addresses for primality
print("\nEvaluating Amplitude 0 Addresses for Primality:")
non_prime_amplitude_0 = 0
for n in range(5, n_max + 1):
    if amplitude[n] == 0:
        num = 90 * n + k
        if not isprime(num):
            non_prime_amplitude_0 += 1
            print(f"Address {n} (90n+k = {num}) has amplitude 0 but is not prime: {factorint(num)}")
            if non_prime_amplitude_0 >= 5:
                print("Stopping after 5 non-prime examples...")
                break
if non_prime_amplitude_0 == 0:
    print("All addresses with amplitude 0 are primes.")
else:
    print(f"Found {non_prime_amplitude_0} addresses with amplitude 0 that are not prime.")

# Analyze growth pattern: addresses with each amplitude across intervals
interval_size = 100
intervals = [(start, min(start + interval_size - 1, n_max)) for start in range(5, n_max + 1, interval_size)]
growth_pattern = {amp: [] for amp in range(max(amplitude_distribution.keys()) + 1)}
density_amplitudes = {amp: [] for amp in range(max(amplitude_distribution.keys()) + 1)}

for start, end in intervals:
    interval_amplitudes = defaultdict(int)
    interval_size_actual = end - start + 1
    for n in range(start, end + 1):
        amp = amplitude[n]
        interval_amplitudes[amp] += 1
    for amp in growth_pattern:
        growth_pattern[amp].append(interval_amplitudes[amp])
        density_amplitudes[amp].append(interval_amplitudes[amp] / interval_size_actual)

# Calculate decay/growth rates for amplitude 0 and 1 (for reference)
decay_rate_amplitude_0 = []
growth_rate_amplitude_1 = []
for i in range(1, len(intervals)):
    decay_rate_amplitude_0.append(density_amplitudes[0][i-1] - density_amplitudes[0][i])
    growth_rate_amplitude_1.append(density_amplitudes[1][i] - density_amplitudes[1][i-1])

# Check proportionality (for reference)
print("\nDecay Rate of Amplitude 0 Density and Growth Rate of Amplitude 1 Density:")
proportionality_ratios = []
for i in range(len(decay_rate_amplitude_0)):
    decay = decay_rate_amplitude_0[i]
    growth = growth_rate_amplitude_1[i]
    if decay != 0:
        ratio = growth / decay
        proportionality_ratios.append(ratio)
        ratio_display = f"{ratio:.4f}"
    else:
        ratio_display = "N/A"
    print(f"Interval {intervals[i][0]}-{intervals[i][1]}: Decay Rate (Amp 0) = {decay:.4f}, Growth Rate (Amp 1) = {growth:.4f}, Ratio = {ratio_display}")

# Compute Pearson correlation coefficients for selected amplitude pairs
pairs_to_analyze = [(1, 3), (2, 3), (1, 2)]
print("\nCorrelation Analysis Between Amplitude Pairs:")
for amp1, amp2 in pairs_to_analyze:
    correlation, p_value = pearsonr(density_amplitudes[amp1], density_amplitudes[amp2])
    print(f"Pearson Correlation Coefficient between Amplitude {amp1} and Amplitude {amp2} Densities: {correlation:.4f}")
    print(f"P-value: {p_value:.4e}")

# Plot densities for amplitudes 0, 1, 2, 3
plt.figure(figsize=(12, 6))
for amp in [0, 1, 2, 3]:
    plt.plot(range(len(intervals)), density_amplitudes[amp], label=f"Density of Amplitude {amp}")
plt.xlabel('Interval (100 addresses each)')
plt.ylabel('Density')
plt.title('Density of Amplitudes 0, 1, 2, and 3 Across Intervals')
plt.legend()
plt.grid(True)
plt.xticks(range(len(intervals)), [f"{start}-{end}" for start, end in intervals], rotation=45)
plt.tight_layout()
plt.show()

# Plot growth pattern for all amplitudes
plt.figure(figsize=(12, 6))
for amp in growth_pattern:
    if amp > 0:  # Skip amplitude 0 for clarity
        plt.plot(range(len(intervals)), growth_pattern[amp], label=f"Amplitude {amp}")
plt.xlabel('Interval (100 addresses each)')
plt.ylabel('Number of Addresses')
plt.title('Growth Pattern of Amplitudes Across Intervals')
plt.legend()
plt.grid(True)
plt.xticks(range(len(intervals)), [f"{start}-{end}" for start, end in intervals], rotation=45)
plt.tight_layout()
plt.show()

# Execution time
print(f"\nExecution time: {time.time() - start_time:.2f} seconds")