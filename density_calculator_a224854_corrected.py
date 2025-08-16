import math
import logging

# Configure logging to match your output format
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

def is_prime(n):
    """Check if n is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def compute_epoch(h):
    """Compute epoch for given h."""
    return 90 * h * h - 12 * h + 1

def sieve_subsequence(n_start, n_end, operators, k, x_max_factor=250):
    """Sieve a chunk for a single subsequence (90n + k)."""
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
    
    primes = [n for n in range(n_start, n_end) if A[n - n_start] == 0 and is_prime(90 * n + k)]
    total_marks = len(marked_indices)
    raw_marks = sum(A)
    unique_density = total_marks / chunk_size if chunk_size > 0 else 0
    raw_density = raw_marks / chunk_size if chunk_size > 0 else 0
    return primes, total_marks, raw_marks, unique_density, raw_density

def sieve_chunk(n_start, n_end, operators, x_max_factor=250):
    """Sieve for A224854 (combined 90n + 11 and 90n + 13)."""
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
    
    twin_primes = []
    for i in range(chunk_size):
        n = n_start + i
        if A[i] == 0:
            p1 = 90 * n + 11
            p2 = 90 * n + 13
            if is_prime(p1) and is_prime(p2):
                twin_primes.append(n)
    
    total_marks = len(marked_indices)
    raw_marks = sum(A)
    unique_density = total_marks / chunk_size if chunk_size > 0 else 0
    raw_density = raw_marks / chunk_size if chunk_size > 0 else 0
    return twin_primes, total_marks, raw_marks, unique_density, raw_density

def sieve_a224854_density(h_values):
    """Compute density for A224854 and its subsequences."""
    operators_11 = [
        (120, 34, 7, 53), (132, 48, 19, 29), (120, 38, 17, 43),
        (90, 11, 13, 77), (78, -1, 11, 91), (108, 32, 31, 41),
        (90, 17, 23, 67), (72, 14, 49, 59), (60, 4, 37, 83),
        (60, 8, 47, 73), (48, 6, 61, 71), (12, 0, 79, 89)
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
        primes_11, marks_11, raw_marks_11, unique_density_11, raw_density_11 = sieve_subsequence(
            n_start, n_end, operators_11, k=11
        )
        
        # Sieve for 90n + 13
        primes_13, marks_13, raw_marks_13, unique_density_13, raw_density_13 = sieve_subsequence(
            n_start, n_end, operators_13, k=13
        )
        
        # Sieve for A224854
        twin_primes, total_marks, raw_marks, unique_density, raw_density = sieve_chunk(
            n_start, n_end, all_operators
        )
        
        # Compute twin primes as intersection
        twin_primes_intersection = [n for n in primes_11 if n in primes_13]
        
        # Compute variance
        mean_density = (unique_density_11 + unique_density_13) / 2
        variance = ((unique_density_11 - mean_density)**2 + (unique_density_13 - mean_density)**2) / 2
        
        results.append({
            'h': h,
            'epoch': N_h,
            'primes_11_count': len(primes_11),
            'primes_13_count': len(primes_13),
            'twin_primes_count': len(twin_primes_intersection),
            'unique_density_11': unique_density_11,
            'raw_density_11': raw_density_11,
            'unique_density_13': unique_density_13,
            'raw_density_13': raw_density_13,
            'unique_density_a224854': unique_density,
            'raw_density_a224854': raw_density,
            'density_variance': variance
        })
        
        # Log results
        logger.info(f"\nEpoch h = {h}, N = {N_h}:")
        logger.info(f"Primes in 90n + 11: {len(primes_11)}")
        logger.info(f"Unique density (90n + 11): {unique_density_11:.4f}")
        logger.info(f"Raw density (90n + 11): {raw_density_11:.4f}")
        logger.info(f"Primes in 90n + 13: {len(primes_13)}")
        logger.info(f"Unique density (90n + 13): {unique_density_13:.4f}")
        logger.info(f"Raw density (90n + 13): {raw_density_13:.4f}")
        logger.info(f"Twin primes (A224854): {len(twin_primes_intersection)}")
        logger.info(f"Unique density (A224854): {unique_density:.4f}")
        logger.info(f"Raw density (A224854): {raw_density:.4f}")
        logger.info(f"Density variance between subsequences: {variance:.6f}")
    
    return results

def main():
    h_values = [140, 280, 360]  # Test provided and larger epochs
    results = sieve_a224854_density(h_values)
    return results

if __name__ == "__main__":
    main()