import math

def operator_amplitude(n_max, operator):
    a, l, m, p, q = operator
    amplitude = [0] * (n_max + 1)
    for x in range(1, int((n_max / 90)**0.5) + 2):
        n = a * x**2 - l * x + m
        if 0 <= n <= n_max:
            amplitude[n] += 1
            p_x = p + 90 * (x - 1)
            q_x = q + 90 * (x - 1)
            for i in range(1, (n_max - n) // p_x + 1):
                if n + i * p_x <= n_max:
                    amplitude[n + i * p_x] += 1
            for i in range(1, (n_max - n) // q_x + 1):
                if n + i * q_x <= n_max:
                    amplitude[n + i * q_x] += 1
    return amplitude

def mark_composites_k(n_max, operators):
    amplitude = [0] * (n_max + 1)
    for op in operators:
        amp = operator_amplitude(n_max, op)
        for n in range(n_max + 1):
            amplitude[n] += amp[n]
    return amplitude

# Operators for k = 11
operators_11 = [
    (90, 120, 34, 7, 53), (90, 132, 48, 19, 29), (90, 120, 38, 17, 43),
    (90, 90, 11, 13, 77), (90, 78, -1, 11, 91), (90, 108, 32, 31, 41),
    (90, 90, 17, 23, 67), (90, 72, 14, 49, 59), (90, 60, 4, 37, 83),
    (90, 60, 8, 47, 73), (90, 48, 6, 61, 71), (90, 12, 0, 79, 89)
]

# Test with n_max = 1000 to match your example length
n_max = 1000
amplitude_list = mark_composites_k(n_max, operators_11)

print(f"Amplitude List for k = 11 (n_max = {n_max}):")
print(amplitude_list)
new_amplitude = [i for i,x in amplitude_list if x == 0]
print(new_amplitude)
print(f"Length: {len(amplitude_list)}")
print(f"Holes (amplitude = 0): {sum(1 for x in amplitude_list if x == 0)}")
print(f"Max Amplitude: {max(amplitude_list)}")

# Test with n_max = 100,000 to match your last run
n_max = 100000
amplitude_list_large = mark_composites_k(n_max, operators_11)

print(f"\nAmplitude List for k = 11 (n_max = {n_max}, first 1000):")
print(amplitude_list_large[:1000])
print(f"Length: {len(amplitude_list_large)}")
print(f"Holes (amplitude = 0): {sum(1 for x in amplitude_list_large if x == 0)}")
print(f"Max Amplitude: {max(amplitude_list_large)}")