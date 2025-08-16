import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

x_values = [10, 20, 30, 40, 50, 60, 70, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300]
y_values = [6758, 22263, 44616, 73508, 108350, 148875, 195064, 364949, 1248754, 2578225, 4321127, 6458565, 8975005, 11858988, 15103156, 18696518, 22635370, 26913361, 31523641, 36465614, 41734250, 47324088, 53229359, 59450633, 65982659, 72826773, 79975058, 87427586, 95185547, 103245073]

# Create the plot
plt.figure(figsize=(10, 6))

# Plot scatter points
plt.scatter(x_values, y_values, color='blue', label='Sequence Points')

# Use log scale for y-axis to better visualize exponential growth
plt.yscale('log')

# Fit a linear regression to the log of y-values to estimate exponential growth
log_y = np.log(y_values)
slope, intercept, r_value, p_value, std_err = stats.linregress(x_values, log_y)

# Calculate the trend line in original scale
trend_line = np.exp(intercept + slope * np.array(x_values))

# Plot the trend line
plt.plot(x_values, trend_line, color='red', label=f'Exponential Trend: y = {np.exp(intercept):.2e} * {np.exp(slope):.2f}^x')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Divergent Sequence Analysis with Trend Line')
plt.legend()

# Add grid for better readability
plt.grid(True, which="both", ls="-", alpha=0.2)

plt.show()