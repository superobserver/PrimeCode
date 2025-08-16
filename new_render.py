# Define the quadratic operator function
def operator_space(x):
    return 90 * x * x - x + 13

# Compute the curve data
def generate_curve_data():
    x_limit = 10
    step_size = 0.1  # Fine step for smoothness
    curve_data = []
    for x in range(int(-x_limit * 10), int(x_limit * 10) + 1, 1):
        scaled_x = x / 10.0
        y = operator_space(scaled_x)
        curve_data.append((scaled_x, y))
    return curve_data

# Main execution
if __name__ == "__main__":
    curve_data = generate_curve_data()
    # Placeholder for saving or using the data (e.g., to an image file)
    # Example: print(curve_data) or pass to an image generation library
    for x, y in curve_data:
        print(f"x={x}, y={y}")