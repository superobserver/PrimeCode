import math

def compute_raw_marks_11(n_end):
    """Compute exact raw markings for operators_11 up to n_end."""
    operators_11 = [
        (120, 34, 7, 53), (132, 48, 19, 29), (120, 38, 17, 43),
        (90, 11, 13, 77), (78, -1, 11, 91), (108, 32, 31, 41),
        (90, 17, 23, 67), (72, 14, 49, 59), (60, 4, 37, 83),
        (60, 8, 47, 73), (48, 6, 61, 71), (12, 0, 79, 89)
    ]
    
    total_marks = 0
    x_max = math.floor(math.sqrt(250 * n_end / 90))
    
    for l, m, z, o in operators_11:
        # Quadratic marks
        for x in range(1, x_max + 1):
            y = 90 * x * x - l * x + m
            if 0 <= y < n_end:
                total_marks += 1
        
        # Arithmetic marks for p and q
        for x in range(1, x_max + 1):
            p = z + 90 * (x - 1)
            q = o + 90 * (x - 1)
            y = 90 * x * x - l * x + m
            if 0 <= y < n_end:
                # p marks
                k_min = 0 if y >= 0 else math.ceil(-y / p)
                k_max = math.floor((n_end - 1 - y) / p)
                total_marks += max(0, k_max - k_min + 1)
                # q marks
                k_min = 0 if y >= 0 else math.ceil(-y / q)
                k_max = math.floor((n_end - 1 - y) / q)
                total_marks += max(0, k_max - k_min + 1)
    
    return total_marks

def approximate_raw_marks_11(n_end):
    """Approximate raw markings using formula."""
    return 0.1333 * n_end * math.log(n_end) if n_end > 0 else 0

# Example usage
if __name__ == "__main__":
    n_end_values = [10000, 50000, 1000000, 5000000, 10000000, 50000000]
    for n_end in n_end_values:
        exact = compute_raw_marks_11(n_end)
        approx = approximate_raw_marks_11(n_end)
        print(f"n_end = {n_end}: Exact = {exact}, Approx = {approx:.0f}")