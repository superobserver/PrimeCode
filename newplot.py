import matplotlib.pyplot as plt
from matplotlib import pyplot
import numpy as np
from scipy import optimize

# Data points for the sequence
x_values = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 3200]
y_values = [364949, 1248754, 2578225, 4321127, 6458565, 8975005, 11858988, 15103156, 18696518, 22635370, 26913361, 31523641, 36465614, 41734250, 47324088, 53229359, 59450633, 65982659, 72826773, 79975058, 87427586, 95185547, 103245073, 111601761, 120257755, 129208061, 138447902, 147984667, 157806078, 167921264, 178320321, 189004707]

# Calculate first differences (rate of change)
first_diff = np.diff(y_values)

# Calculate second differences (rate of change of rate of change)
second_diff = np.diff(first_diff)

# Calculate third differences (jerk)
third_diff = np.diff(second_diff)

# Calculate fourth differences
fourth_diff = np.diff(third_diff)

# Calculate ratios between consecutive terms
ratios = [y_values[i+1]/y_values[i] for i in range(len(y_values)-1)]

# Figure for sequence and ratios
fig_seq, axs_seq = plt.subplots(2, 1, figsize=(12, 12))

# Plot original sequence with annotations
axs_seq[0].scatter(x_values, y_values, color='blue', label='Sequence Points')
axs_seq[0].plot(x_values, y_values, color='red', label='Growth Curve')
axs_seq[0].set_yscale('log')
axs_seq[0].set_xlabel('x')
axs_seq[0].set_ylabel('y (log scale)')
axs_seq[0].set_title('Exponential Growth of the Sequence with Trend Analysis')

# Annotate points on the sequence plot
for i, txt in enumerate(y_values):
    axs_seq[0].annotate(f'{txt}', (x_values[i], y_values[i]), textcoords="offset points", xytext=(0,10), ha='center')

# Fit and plot exponential trend for original sequence
log_y = np.log(y_values)
slope, intercept = np.polyfit(x_values, log_y, 1)
trend_line = np.exp(intercept + slope * np.array(x_values))
axs_seq[0].plot(x_values, trend_line, color='green', label=f'Exponential Trend: y = {np.exp(intercept):.2e} * {np.exp(slope):.2f}^x')

# Additional analysis for sequence behavior
poly_fit = np.polyfit(x_values, np.log(y_values), 2)  # Quadratic fit in log space
poly_trend = np.exp(np.poly1d(poly_fit)(x_values))
axs_seq[0].plot(x_values, poly_trend, color='orange', linestyle='--', label='Quadratic Trend in Log Space')

axs_seq[0].legend()

# Plot ratios with annotations
axs_seq[1].scatter(x_values[:-1], ratios, color='blue', label='Ratio of Terms')
axs_seq[1].set_xlabel('x')
axs_seq[1].set_ylabel('Ratio')
axs_seq[1].set_title('Ratio of Consecutive Terms with Trend Analysis')

# Annotate points on the ratio plot
for i, txt in enumerate(ratios):
    axs_seq[1].annotate(f'{txt:.3f}', (x_values[i], ratios[i]), textcoords="offset points", xytext=(0,10), ha='center')

# Fit a polynomial trend for ratios
coeffs = np.polyfit(x_values[:-1], ratios, 3)
poly_fit = np.poly1d(coeffs)
x_fit = np.linspace(min(x_values), max(x_values[:-1]), 1000)
y_fit = poly_fit(x_fit)

axs_seq[1].plot(x_fit, y_fit, color='green', label='3rd Degree Polynomial Trend')

# Additional trend analysis for ratios
coeffs_linear = np.polyfit(x_values[:-1], ratios, 1)
linear_fit = np.poly1d(coeffs_linear)(x_fit)
axs_seq[1].plot(x_fit, linear_fit, color='orange', linestyle='--', label='Linear Trend')

axs_seq[1].legend()

plt.tight_layout()
# Show the sequence and ratios plot in a
plt.show()
