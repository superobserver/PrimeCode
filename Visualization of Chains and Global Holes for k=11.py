#!/usr/bin/env python
import matplotlib.pyplot as plt

# Data from output
global_holes = [0, 1, 2, 3, 5, 7, 9, 10, 12, 13] + [...]  # First 10 + placeholder
operators = [
    (120, 34, 7, 53, 'Operator 1'),
    (132, 48, 19, 29, 'Operator 2'),
    (120, 38, 17, 43, 'Operator 3'),
    (90, 11, 13, 77, 'Operator 4'),
    (78, -1, 11, 91, 'Operator 5'),
    (108, 32, 31, 41, 'Operator 6'),
    (90, 17, 23, 67, 'Operator 7'),
    (72, 14, 49, 59, 'Operator 8'),
    (60, 4, 37, 83, 'Operator 9'),
    (60, 8, 47, 73, 'Operator 10'),
    (48, 6, 61, 71, 'Operator 11'),
    (12, 0, 79, 89, 'Operator 12')
]
n_max = 2191
x_max = int((n_max / 90) ** 0.5) + 2

# Generate insertion addresses
insertions = []
for l, m, p, q, label in operators:
    ins = []
    for x in range(1, min(5, x_max)):
        n = 90 * x * x - l * x + m
        if 0 <= n <= n_max:
            ins.append(n)
    insertions.append((label, ins))

# Sample chain for Operator 1 (p_x=7, x=1)
chain_op1 = [4, 11, 18, 25, 32]  # From previous output

# Plot
plt.figure(figsize=(12, 6))
# Plot global holes
plt.scatter(global_holes[:50], [0] * len(global_holes[:50]), color='red', label='Global Holes', marker='o')
# Plot insertion addresses
for label, ins in insertions:
    plt.scatter(ins, [int(label.split()[1])] * len(ins), label=label, alpha=0.6)
# Plot sample chain
plt.plot(chain_op1, [0.5] * len(chain_op1), color='blue', label='Operator 1 Chain (p=7)', marker='x')
plt.xlabel('Address (n)')
plt.ylabel('Operator / Level')
plt.title('Chain Growth Patterns and Global Holes for k=11')
plt.legend()
plt.grid(True)
plt.show()