
#!/usr/bin/env python
import cmath
import numpy
import sys
import multiprocessing
import time

numpy.set_printoptions(threshold=sys.maxsize)

def get_limit():
    """Safely get limit input from user."""
    try:
        limit = int(input("limit value here: "))
        if limit <= 0:
            raise ValueError("Limit must be positive")
        return limit
    except ValueError as e:
        print(f"Error: Invalid input. {e}")
        sys.exit(1)

# Calculate epoch and iteration range
def calculate_parameters(limit):
    h = limit
    epoch = 90 * (h * h) - 12 * h + 1
    base10 = (epoch * 90) + 11
    a, b, c = 90, -300, 250 - epoch
    d = (b**2) - (4 * a * c)
    sol1 = (-b - cmath.sqrt(d)) / (2 * a)
    sol2 = (-b + cmath.sqrt(d)) / (2 * a)
    new_limit = int(sol2.real)
    return epoch, base10, sol1, sol2, new_limit

# Composite generating function
def drLD(x, l, m, z, o, A201804_np, marks_np, limit):
    y = 90 * (x * x) - l * x + m
    if 0 <= y < len(A201804_np):
        A201804_np[y] += 1
        marks_np[y] += 1
    p = z + (90 * (x - 1))
    q = o + (90 * (x - 1))
    for n in range(1, int(((limit - y) / p) + 1)):
        idx = int(y + p * n)
        if 0 <= idx < len(A201804_np):
            A201804_np[idx] += 1
            marks_np[idx] += 1
    for n in range(1, int(((limit - y) / q) + 1)):
        idx = int(y + q * n)
        if 0 <= idx < len(A201804_np):
            A201804_np[idx] += 1
            marks_np[idx] += 1

# Worker function for a subset of operators
def process_operators(operator_indices, A201804_shared, marks_per_operator_shared, limit, new_limit, operator_params):
    try:
        A201804_np = numpy.frombuffer(A201804_shared, dtype=numpy.int32)
        marks_per_operator_np = [numpy.frombuffer(marks_per_operator_shared[i], dtype=numpy.int32) for i in operator_indices]
        for x in range(1, new_limit):
            for idx, op_idx in enumerate(operator_indices):
                l, m, z, o = operator_params[op_idx]
                drLD(x, l, m, z, o, A201804_np, marks_per_operator_np[idx], limit)
    except Exception as e:
        print(f"Error in process_operators: {e}")
        raise

# Main function to distribute work
def main():
    start_time = time.time()
    
    # Get limit and calculate parameters
    limit = get_limit()
    epoch, base10, sol1, sol2, new_limit = calculate_parameters(limit)
    print(f"The epoch range is {epoch}")
    print(f"This is the base-10 limit: {base10}")
    print(f"The solutions are {sol1} and {sol2}")

    # Initialize shared arrays
    array_size = int(limit + 10)
    A201804_shared = multiprocessing.Array('i', [0] * array_size, lock=False)
    marks_per_operator_shared = [multiprocessing.Array('i', [0] * array_size, lock=False) for _ in range(12)]
    
    # Operator parameters
    operator_params = [
        (120, 34, 7, 53),   # Operator 1
        (132, 48, 19, 29),  # Operator 2
        (120, 38, 17, 43),  # Operator 3
        (90, 11, 13, 77),   # Operator 4
        (78, -1, 11, 91),   # Operator 5
        (108, 32, 31, 41),  # Operator 6
        (90, 17, 23, 67),   # Operator 7
        (72, 14, 49, 59),   # Operator 8
        (60, 4, 37, 83),    # Operator 9
        (60, 8, 47, 73),    # Operator 10
        (48, 6, 61, 71),    # Operator 11
        (12, 0, 79, 89)     # Operator 12
    ]

    # Split operators across processes
    num_cores = min(multiprocessing.cpu_count(), len(operator_params))
    print(f"Using {num_cores} CPU cores")
    operators_per_process = len(operator_params) // num_cores + 1
    process_tasks = [list(range(i, min(i + operators_per_process, len(operator_params)))) for i in range(0, len(operator_params), operators_per_process)]
    
    # Create and start processes
    processes = []
    try:
        for task in process_tasks:
            p = multiprocessing.Process(
                target=process_operators,
                args=(task, A201804_shared, marks_per_operator_shared, limit, new_limit, operator_params)
            )
            processes.append(p)
            p.start()
        
        # Wait for all processes to complete
        for p in processes:
            p.join()
    except Exception as e:
        print(f"Error during multiprocessing: {e}")
        sys.exit(1)
    
    # Convert shared arrays to numpy for final processing
    A201804 = numpy.frombuffer(A201804_shared, dtype=numpy.int32)[:-10]
    marks_per_operator = [numpy.frombuffer(marks_per_operator_shared[i], dtype=numpy.int32)[:-10] for i in range(12)]
    
    # Identify forbidden values
    forbidden_values = [k for k in range(len(A201804)) if A201804[k] == 0]
    print("Forbidden values (k where 90k + 11 are prime):", forbidden_values[:10], "...")
    print("Number of forbidden values:", len(forbidden_values))
    
    # Calculate density of marks
    marks = len(A201804) - (A201804 == 0).sum()
    density = marks / len(A201804)
    print("Total marks:", marks)
    print("Density of marks:", density)
    
    # Analyze marks per operator
    for i, (l, m, z, o) in enumerate(operator_params):
        total_marks = marks_per_operator[i].sum()
        print(f"Operator {i+1} (z={z}, o={o}): Total marks = {total_marks}")
    
    # Analyze cancellation frequencies for the first operator
    def analyze_frequencies(op_index, z, o):
        frequencies = {}
        for x in range(1, new_limit):
            y = 90 * (x * x) - operator_params[op_index][0] * x + operator_params[op_index][1]
            p = z + (90 * (x - 1))
            q = o + (90 * (x - 1))
            if 0 <= y < limit:
                frequencies[y] = frequencies.get(y, 0) + 1
            for n in range(1, int(((limit - y) / p) + 1)):
                idx = int(y + p * n)
                if 0 <= idx < limit:
                    frequencies[idx] = frequencies.get(idx, 0) + 1
            for n in range(1, int(((limit - y) / q) + 1)):
                idx = int(y + q * n)
                if 0 <= idx < limit:
                    frequencies[idx] = frequencies.get(idx, 0) + 1
        return frequencies
    
    freqs = analyze_frequencies(0, 7, 53)
    print("Mark frequencies for Operator 1 (z=7, o=53):", dict(sorted(freqs.items())[:20]))
    
    # Print runtime
    print(f"Runtime: {time.time() - start_time:.2f} seconds")

if __name__ == '__main__':
    multiprocessing.freeze_support()  # Required for Windows compatibility
    main()
