import math

def compute_marks_operators_11_deinterlaced(n_end):
    """Compute marks per epoch for all operators in operators_11."""
    operators_11 = [
        (120, 34, 7, 53), (132, 48, 19, 29), (120, 38, 17, 43),
        (90, 11, 13, 77), (78, -1, 11, 91), (108, 32, 31, 41),
        (90, 17, 23, 67), (72, 14, 49, 59), (60, 4, 37, 83),
        (60, 8, 47, 73), (48, 6, 61, 71), (12, 0, 79, 89)
    ]
    
    x_max = math.floor(math.sqrt(250 * n_end / 90))
    results = []
    
    for op_idx, (l, m, z, o) in enumerate(operators_11):
        y_marks = []
        p_marks = []
        q_marks = []
        total_marks = 0
        
        for x in range(1, x_max + 1):
            y = 90 * x * x - l * x + m
            y_mark = 1 if 0 <= y < n_end else 0
            y_marks.append(y_mark)
            
            p = z + 90 * (x - 1)
            q = o + 90 * (x - 1)
            
            p_mark = q_mark = 0
            if 0 <= y < n_end:
                k_max_p = math.floor((n_end - 1 - y) / p)
                p_mark = max(0, k_max_p + 1)
                k_max_q = math.floor((n_end - 1 - y) / q)
                q_mark = max(0, k_max_q + 1)
            
            p_marks.append(p_mark)
            q_marks.append(q_mark)
            total_marks += y_mark + p_mark + q_mark
        
        results.append({
            'operator': (l, m, z, o),
            'y_marks': y_marks,
            'p_marks': p_marks,
            'q_marks': q_marks,
            'total_marks': total_marks,
            'density': total_marks / n_end if n_end > 0 else 0
        })
    
    return results, x_max

def print_marks_table(n_end_values):
    """Print table of marks per epoch for all operators."""
    print("n_end | Op | x | y_marks | p_marks | q_marks | Total")
    print("-" * 50)
    
    for n_end in n_end_values:
        results, x_max = compute_marks_operators_11_deinterlaced(n_end)
        for op_idx, res in enumerate(results):
            l, m, z, o = res['operator']
            for x in range(1, x_max + 1):
                if x < len(res['y_marks']):
                    total = res['y_marks'][x-1] + res['p_marks'][x-1] + res['q_marks'][x-1]
                    print(f"{n_end:<12} | {op_idx:<2} | {x:<2} | {res['y_marks'][x-1]:<7} | {res['p_marks'][x-1]:<7} | {res['q_marks'][x-1]:<7} | {total:<5}")
            print(f"{'Total':<12} | {op_idx:<2} | {'':<2} | {sum(res['y_marks']):<7} | {sum(res['p_marks']):<7} | {sum(res['q_marks']):<7} | {res['total_marks']:<5} | Density: {res['density']:.4f}")
        print("-" * 50)

def get_density_data(n_end_values):
    """Collect density data for plotting."""
    densities_data = {f"Operator {i}": [] for i in range(12)}
    for n_end in n_end_values:
        results, _ = compute_marks_operators_11_deinterlaced(n_end)
        for op_idx, res in enumerate(results):
            densities_data[f"Operator {op_idx}"].append(res['density'])
    return densities_data

if __name__ == "__main__":
    n_end_values = [10000, 50000, 1000000, 5000000, 10000000, 50000000, 500000000]
    print_marks_table(n_end_values)
    
    # Generate density data for plotting
    density_data = get_density_data(n_end_values)
    print("\nDensity Data for Plotting:")
    for op, densities in density_data.items():
        print(f"{op}: {densities}")