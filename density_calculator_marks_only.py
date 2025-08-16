import math
import logging
import multiprocessing as mp
from functools import partial

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

def compute_epoch(h):
    """Compute epoch for given h."""
    return 90 * h * h - 12 * h + 1

def sieve_subsequence_chunk(n_start, n_end, operators, x_max_factor=250):
    """Sieve a chunk to produce marks for a subsequence."""
    chunk_size = n_end - n_start
    A = [0] * chunk_size  # Amplitude array
    marked_indices = set()  # Unique marked indices
    
    x_max = math.floor(math.sqrt(x_max_factor * n_end / 90))
    
    for l, m, z, o in operators:
        for x in range(1, x_max + 1):
            y = 90 * x * x - l * x + m
            p = z + 90 * (x - 1)
            q = o + 90 * (x - 1)
            
            if n_start <= y < n_end:
                idx = y - n_start
                A[idx] += 1
                marked_indices.add(y)
            
            n_min = math.ceil((n_start - y) / p) if y < n_start else 0
            n_max = math.floor((n_end - y - 1) / p)
            for n in range(max(0, n_min), n_max + 1):
                idx = y + n * p
                if n_start <= idx < n_end:
                    A[idx - n_start] += 1
                    marked_indices.add(idx)
            
            n_min = math.ceil((n_start - y) / q) if y < n_start else 0
            n_max = math.floor((n_end - y - 1) / q)
            for n in range(max(0, n_min), n_max + 1):
                idx = y + n * q
                if n_start <= idx < n_end:
                    A[idx - n_start] += 1
                    marked_indices.add(idx)
    
    total_marks = len(marked_indices)
    return A, total_marks

def sieve_subsequence(n_start, n_end, operators, x_max_factor=250, num_processes=None):
    """Sieve a subsequence using multiple processes, returning marks."""
    if num_processes is None:
        num_processes = mp.cpu_count()
    
    chunk_size = (n_end - n_start) // num_processes
    if chunk_size == 0:
        return sieve_subsequence_chunk(n_start, n_end, operators, x_max_factor)
    
    tasks = []
    for i in range(num_processes):
        chunk_start = n_start + i * chunk_size
        chunk_end = chunk_start + chunk_size if i < num_processes - 1 else n_end
        tasks.append((chunk_start, chunk_end))
    
    with mp.Pool(processes=num_processes) as pool:
        results = pool.starmap(
            partial(sieve_subsequence_chunk, operators=operators, x_max_factor=x_max_factor),
            tasks
        )
    
    # Aggregate results
    total_chunk_size = n_end - n_start
    A = [0] * total_chunk_size
    total_marks = 0
    for chunk_A, chunk_marks in results:
        chunk_start = tasks[results.index((chunk_A, chunk_marks))][0]
        offset = chunk_start - n_start
        for i, value in enumerate(chunk_A):
            A[i + offset] += value
        total_marks += chunk_marks
    
    return A, total_marks

def sieve_chunk_chunk(n_start, n_end, operators, x_max_factor=250):
    """Sieve a chunk to produce marks for A224854."""
    chunk_size = n_end - n_start
    A = [0] * chunk_size
    marked_indices = set()
    
    x_max = math.floor(math.sqrt(x_max_factor * n_end / 90))
    
    for l, m, z, o in operators:
        for x in range(1, x_max + 1):
            y = 90 * x * x - l * x + m
            p = z + 90 * (x - 1)
            q = o + 90 * (x - 1)
            
            if n_start <= y < n_end:
                idx = y - n_start
                A[idx] += 1
                marked_indices.add(y)
            
            n_min = math.ceil((n_start - y) / p) if y < n_start else 0
            n_max = math.floor((n_end - y - 1) / p)
            for n in range(max(0, n_min), n_max + 1):
                idx = y + n * p
                if n_start <= idx < n_end:
                    A[idx - n_start] += 1
                    marked_indices.add(idx)
            
            n_min = math.ceil((n_start - y) / q) if y < n_start else 0
            n_max = math.floor((n_end - y - 1) / q)
            for n in range(max(0, n_min), n_max + 1):
                idx = y + n * q
                if n_start <= idx < n_end:
                    A[idx - n_start] += 1
                    marked_indices.add(idx)
    
    total_marks = len(marked_indices)
    return A, total_marks

def sieve_chunk(n_start, n_end, operators, x_max_factor=250, num_processes=None):
    """Sieve A224854 using multiple processes, returning marks."""
    if num_processes is None:
        num_processes = mp.cpu_count()
    
    chunk_size = (n_end - n_start) // num_processes
    if chunk_size == 0:
        return sieve_chunk_chunk(n_start, n_end, operators, x_max_factor)
    
    tasks = []
    for i in range(num_processes):
        chunk_start = n_start + i * chunk_size
        chunk_end = chunk_start + chunk_size if i < num_processes - 1 else n_end
        tasks.append((chunk_start, chunk_end))
    
    with mp.Pool(processes=num_processes) as pool:
        results = pool.starmap(
            partial(sieve_chunk_chunk, operators=operators, x_max_factor=x_max_factor),
            tasks
        )
    
    # Aggregate results
    total_chunk_size = n_end - n_start
    A = [0] * total_chunk_size
    total_marks = 0
    for chunk_A, chunk_marks in results:
        chunk_start = tasks[results.index((chunk_A, chunk_marks))][0]
        offset = chunk_start - n_start
        for i, value in enumerate(chunk_A):
            A[i + offset] += value
        total_marks += chunk_marks
    
    return A, total_marks

def sieve_a224854_marks(h_values, num_processes=None):
    """Compute marks for A224854 and its subsequences."""
    operators_11 = [
        (120, 34, 7, 53), (132, 48, 19, 29), (120, 38, 17, 43),
        (90, 11, 13, 77), (78, -1, 11, 91), (108, 32, 31, 41),
        (90, 17, 23, 67), (72, 14, 49, 59), (60, 4, 37, 83),
        (60, 8, 47, 73), (48, 6, 61, 71), (12, 90, 79, 89)
    ]
    operators_13 = [
        (76, -1, 13, 91), (94, 18, 19, 67), (94, 24, 37, 49),
        (76, 11, 31, 73), (86, 6, 11, 83), (104, 29, 29, 47),
        (86, 14, 23, 71), (86, 20, 41, 53), (104, 25, 17, 59),
        (14, 0, 77, 89), (94, 10, 7, 79), (76, 15, 43, 61)
    ]
    all_operators = operators_11 + operators_13
    
    results = []
    for h in h_values:
        N_h = compute_epoch(h)
        n_start = 0
        n_end = N_h
        
        # Sieve for 90n + 11
        A_11, marks_11 = sieve_subsequence(n_start, n_end, operators_11, num_processes=num_processes)
        
        # Sieve for 90n + 13
        A_13, marks_13 = sieve_subsequence(n_start, n_end, operators_13, num_processes=num_processes)
        
        # Sieve for A224854
        A_a224854, marks_a224854 = sieve_chunk(n_start, n_end, all_operators, num_processes=num_processes)
        
        results.append({
            'h': h,
            'epoch': N_h,
            'marks_11': marks_11,
            'marks_13': marks_13,
            'marks_a224854': marks_a224854,
            'A_11': A_11,
            'A_13': A_13,
            'A_a224854': A_a224854
        })
        
        # Log results
        logger.info(f"\nEpoch h = {h}, N = {N_h}:")
        logger.info(f"Unique marks (90n + 11): {marks_11}")
        logger.info(f"Unique marks (90n + 13): {marks_13}")
        logger.info(f"Unique marks (A224854): {marks_a224854}")
    
    return results

def main():
    h_values = [40, 80, 160]  # Test provided and larger epochs
    results = sieve_a224854_marks(h_values)
    return results

if __name__ == "__main__":
    main()