import numpy as np
import matplotlib.pyplot as plt

# Data points for terms
n = np.array([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 3200, 3300])
terms = np.array([40571, 138835, 285950, 479246, 716343, 995766, 1315403, 1675698, 2075395, 2512852, 2988670, 3501612, 4050609, 4636361, 5256970, 5913598, 6605065, 7330036, 8090368, 8885083, 9712828, 10575738, 11471318, 12400184, 13361879, 14354525, 15381964, 16440830, 17532030, 18655358, 19811420, 20998554, 22219612])

# Calculate the average rate of change
rate_of_change = np.diff(terms) / np.diff(n)

# Create the plot
plt.figure(figsize=(12, 10))

# Plot the terms with trend line
plt.subplot(2, 1, 1)
plt.plot(n, terms, 'b-', label='Sequence Terms')
plt.scatter(n, terms, color='blue')  # Adding points for clarity
# Fit a polynomial of degree 4 for the terms (quartic polynomial)
coefficients_terms = np.polyfit(n, terms, 4)
poly_terms = np.poly1d(coefficients_terms)
plt.plot(n, poly_terms(n), 'g--', label='Trend Line (Quartic Fit)')
# Annotate each point with its value, using smaller font size for clarity
for i, txt in enumerate(terms):
    plt.annotate(f'{txt}', (n[i], terms[i]), fontsize=6, xytext=(5, 5), textcoords='offset points')
plt.xlabel('n')
plt.ylabel('Sequence Value')
plt.title('Sequence Terms vs. n')
plt.legend()

# Plot the rate of change with trend line
plt.subplot(2, 1, 2)
plt.plot(n[:-1], rate_of_change, 'r-', label='Average Rate of Change')
plt.scatter(n[:-1], rate_of_change, color='red')  # Adding points for clarity
# Fit a polynomial of degree 3 for the rate of change (cubic polynomial)
coefficients_rate = np.polyfit(n[:-1], rate_of_change, 3)
poly_rate = np.poly1d(coefficients_rate)
plt.plot(n[:-1], poly_rate(n[:-1]), 'g--', label='Trend Line (Cubic Fit)')
# Annotate each rate of change point with its value
for i, txt in enumerate(rate_of_change):
    plt.annotate(f'{txt:.2f}', (n[i], rate_of_change[i]), fontsize=6, xytext=(5, 5), textcoords='offset points')
plt.xlabel('n')
plt.ylabel('Average Rate of Change')
plt.title('Average Rate of Change vs. n')
plt.legend()

# Adjust layout to prevent overlapping
plt.tight_layout()
plt.show()