import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Operator data for k=17 (partial, extrapolated)
operators = [
    (114, 32, 11, 67),  # 11·67
    (108, 30, 13, 85),  # 13·85
    (96, 24, 23, 71),   # 23·71
    (120, 34, 7, 41),   # 7·41 (inferred)
    (120, 38, 17, 43),  # 17·43
    (132, 48, 19, 53),  # 19·53
    (90, 11, 29, 37),   # 29·37
    (108, 32, 31, 47),  # 31·47
    (72, 14, 49, 59),   # 49·59
    (90, 17, 61, 67),   # 61·67
    (60, 4, 73, 79),    # 73·79
    (48, 6, 83, 89)     # 83·89
]

def compute_vector(x, l, m, p, q):
    n = 90 * x**2 - l * x + m
    p_x = p + 90 * (x - 1)
    q_x = q + 90 * (x - 1)
    return p_x, q_x, n

# Plot setup
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
x_vals = np.arange(1, 6)  # x=1 to 5

# Plot each operator
for l, m, p, q in operators:
    p_vals, q_vals, n_vals = [], [], []
    for x in x_vals:
        p_x, q_x, n = compute_vector(x, l, m, p, q)
        p_vals.append(p_x)
        q_vals.append(q_x)
        n_vals.append(n)
    ax.plot(p_vals, q_vals, n_vals, marker='o', label=f'{p}·{q} Operator')

# Customize plot
ax.set_xlabel('p_x')
ax.set_ylabel('q_x')
ax.set_zlabel('n')
ax.set_title('Vector Paths for k=17 Operators')
ax.legend()
plt.show()