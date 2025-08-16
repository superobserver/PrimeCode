import matplotlib.pyplot as plt
from matplotlib import pyplot
import numpy as np

# Data points for the sequence
x_values = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700]
y_values = [364949, 1248754, 2578225, 4321127, 6458565, 8975005, 11858988, 15103156, 18696518, 22635370, 26913361, 31523641, 36465614, 41734250, 47324088, 53229359, 59450633, 65982659, 72826773, 79975058, 87427586, 95185547, 103245073, 111601761, 120257755, 129208061, 138447902]

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
axs_seq[0].set_title('Exponential Growth of the Sequence')
axs_seq[0].legend()

# Annotate points on the sequence plot with smaller font size
for i, txt in enumerate(y_values):
    axs_seq[0].annotate(f'{txt}', (x_values[i], y_values[i]), textcoords="offset points", xytext=(0,10), ha='center', fontsize='small')

# Fit and plot exponential trend for original sequence
log_y = np.log(y_values)
slope, intercept = np.polyfit(x_values, log_y, 1)
trend_line = np.exp(intercept + slope * np.array(x_values))
axs_seq[0].plot(x_values, trend_line, color='green', label=f'Exponential Trend: y = {np.exp(intercept):.2e} * {np.exp(slope):.2f}^x')
axs_seq[0].legend()

# Plot ratios with annotations with smaller font size
axs_seq[1].scatter(x_values[:-1], ratios, color='blue', label='Ratio of Terms')
axs_seq[1].set_xlabel('x')
axs_seq[1].set_ylabel('Ratio')
axs_seq[1].set_title('Ratio of Consecutive Terms')

# Annotate points on the ratio plot with smaller font size
for i, txt in enumerate(ratios):
    axs_seq[1].annotate(f'{txt:.3f}', (x_values[i], ratios[i]), textcoords="offset points", xytext=(0,10), ha='center', fontsize='small')

# Fit linear trend for ratios
slope, intercept = np.polyfit(x_values[:-1], ratios, 1)
axs_seq[1].plot(x_values[:-1], slope * np.array(x_values[:-1]) + intercept, color='green', label='Linear Trend')
axs_seq[1].legend()

plt.tight_layout()
# Show the sequence and ratios plot in a new window
pyplot.show(block=False)

# Figure for derivatives
fig_deriv, axs_deriv = plt.subplots(4, 1, figsize=(12, 20))

# Plot first derivative (rate of change)
axs_deriv[0].scatter(x_values[:-1], first_diff, color='blue', label='First Derivative')
axs_deriv[0].set_xlabel('x')
axs_deriv[0].set_ylabel('First Derivative')
axs_deriv[0].set_title('First Derivative (Rate of Change)')

# Fit linear trend for first derivative
slope, intercept = np.polyfit(x_values[:-1], first_diff, 1)
axs_deriv[0].plot(x_values[:-1], slope * np.array(x_values[:-1]) + intercept, color='green', label='Linear Trend')
axs_deriv[0].legend()

# Plot second derivative (acceleration)
axs_deriv[1].scatter(x_values[:-2], second_diff, color='blue', label='Second Derivative')
axs_deriv[1].set_xlabel('x')
axs_deriv[1].set_ylabel('Second Derivative')
axs_deriv[1].set_title('Second Derivative (Acceleration)')

# Fit linear trend for second derivative
slope, intercept = np.polyfit(x_values[:-2], second_diff, 1)
axs_deriv[1].plot(x_values[:-2], slope * np.array(x_values[:-2]) + intercept, color='green', label='Linear Trend')
axs_deriv[1].legend()

# Plot third derivative (jerk)
axs_deriv[2].scatter(x_values[:-3], third_diff, color='blue', label='Third Derivative')
axs_deriv[2].set_xlabel('x')
axs_deriv[2].set_ylabel('Third Derivative')
axs_deriv[2].set_title('Third Derivative (Jerk)')

# Fit linear trend for third derivative
slope, intercept = np.polyfit(x_values[:-3], third_diff, 1)
axs_deriv[2].plot(x_values[:-3], slope * np.array(x_values[:-3]) + intercept, color='green', label='Linear Trend')
axs_deriv[2].legend()

# Plot fourth derivative
axs_deriv[3].scatter(x_values[:-4], fourth_diff, color='blue', label='Fourth Derivative')
axs_deriv[3].set_xlabel('x')
axs_deriv[3].set_ylabel('Fourth Derivative')
axs_deriv[3].set_title('Fourth Derivative')

# Fit linear trend for fourth derivative
slope, intercept = np.polyfit(x_values[:-4], fourth_diff, 1)
axs_deriv[3].plot(x_values[:-4], slope * np.array(x_values[:-4]) + intercept, color='green', label='Linear Trend')
axs_deriv[3].legend()

plt.tight_layout()
# Show the derivatives plot in a new window
pyplot.show(block=False)

# Keep the script running so windows stay open
plt.show()