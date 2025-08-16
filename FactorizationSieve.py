#!/usr/bin/env python
import math
import time
from collections import defaultdict

# Precompute small primes for factoring (Page 3, primes >= 7)
small_primes = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89]

# User input for limit (h, as in original, Page 10)
try:
    h = int(input("Give a number for limit (will be multiplied by 90^2): "))
    if h <= 0:
        raise ValueError("Limit must be positive")
except ValueError as e:
    print(f"Error: {e}")
    exit(1)

# Compute epoch and limit as in original
limit = 90 * (h * h) - 12 * h + 1
base10_limit = (limit * 90) + 11

# Initialize factor map: defaultdict for sparse storage
factor_map = defaultdict(list)

# Digital root and last digit check (Page 3, map space constraints)
def is_valid(num):
    dr = num
    while dr > 9:
        dr = sum(int(d) for d in str(dr))
    ld = num % 10
    return dr in [1, 2, 4, 5, 7, 8] and ld in [1, 3, 7, 9]

# Function to record factors without duplicates
def record_factors(x, l, m, p, q, factor_map, k=11):
    y = 90 * (x * x) - l * x + m
    if 0 <= y <= limit:
        base10_num = 90 * y + k
        if is_valid(base10_num):
            factor_pair = tuple(sorted([p, q]))
            factor_tuple = (*factor_pair, l, m, x)
            if factor_tuple not in factor_map[y]:
                factor_map[y].append(factor_tuple)
    
    # Mark multiples with p_x and q_x
    p_x = p + (90 * (x - 1))
    q_x = q + (90 * (x - 1))
    
    # Multiples for p_x
    t_p_max = min(int((limit - y) / p_x) + 1, limit + 1)
    seen_y = set()
    for t in range(t_p_max):
        newy = y + (p_x * t)
        if 0 <= newy <= limit and newy not in seen_y:
            base10_num = 90 * newy + k
            if is_valid(base10_num):
                paired_factor = base10_num // p_x
                factor_pair = tuple(sorted([p_x, paired_factor]))
                factor_tuple = (*factor_pair, l, m, x)
                if factor_tuple not in factor_map[newy]:
                    factor_map[newy].append(factor_tuple)
                    seen_y.add(newy)
    
    # Multiples for q_x
    if q_x != p_x:
        t_q_max = min(int((limit - y) / q_x) + 1, limit + 1)
        for t in range(t_q_max):
            newy = y + (q_x * t)
            if 0 <= newy <= limit and newy not in seen_y:
                base10_num = 90 * newy + k
                if is_valid(base10_num):
                    paired_factor = base10_num // q_x
                    factor_pair = tuple(sorted([q_x, paired_factor]))
                    factor_tuple = (*factor_pair, l, m, x)
                    if factor_tuple not in factor_map[newy]:
                        factor_map[newy].append(factor_tuple)
                        seen_y.add(newy)

# Operators for k = 11 (Table 8, Page 25)
operators = [
    {"p": 7, "q": 53, "l": 120, "m": 34},
    {"p": 19, "q": 29, "l": 132, "m": 48},
    {"p": 17, "q": 43, "l": 120, "m": 38},
    {"p": 13, "q": 77, "l": 90, "m": 11},
    {"p": 11, "q": 91, "l": 78, "m": -1},
    {"p": 31, "q": 41, "l": 108, "m": 32},
    {"p": 23, "q": 67, "l": 90, "m": 17},
    {"p": 49, "q": 59, "l": 72, "m": 14},
    {"p": 37, "q": 83, "l": 60, "m": 4},
    {"p": 47, "q": 73, "l": 60, "m": 8},
    {"p": 61, "q": 71, "l": 48, "m": 6},
    {"p": 79, "q": 89, "l": 12, "m": 0}
]

# Apply operators (Page 7, quadratic operators)
start_time = time.time()
for op in operators:
    p, q, l, m = op["p"], op["q"], op["l"], op["m"]
    x_max = int(math.sqrt(limit / 90)) + 2
    for x in range(1, x_max):
        record_factors(x, l, m, p, q, factor_map, k=11)
end_time = time.time()

# Process factor_map to extract primes and factorizations
primes = []
composites = []
omega_counts = []
factor_cache = {}
high_hit_composites = []

def factor_composite(factors):
    """Extract unique prime factors from factor pairs (Page 23, Step 5)."""
    primes = set()
    for p_x, q_x, _, _, _ in factors:
        for num in [p_x, q_x]:
            if num in factor_cache:
                primes.update(factor_cache[num])
                continue
            temp_primes = set()
            n = num
            for d in small_primes:
                if n < d * d:
                    break
                while n % d == 0:
                    temp_primes.add(d)
                    n //= d
            if n > 1:
                for d in range(max(small_primes[-1] + 2, 91), int(math.sqrt(n)) + 1, 2):
                    while n % d == 0:
                        temp_primes.add(d)
                        n //= d
                if n > 1:
                    temp_primes.add(n)
            primes.update(temp_primes)
            factor_cache[num] = temp_primes
    return sorted(primes)

for n in range(limit + 1):
    base10_num = 90 * n + 11
    factors = factor_map[n]
    if not factors:
        primes.append(base10_num)
    else:
        composites.append((base10_num, factors))
        prime_factors = factor_composite(factors)
        omega_counts.append((base10_num, len(prime_factors), prime_factors))
        if len(factors) >= 4:
            high_hit_composites.append((base10_num, len(factors), factors, prime_factors))

# Compute average factor list size
avg_factor_list_size = sum(len(factors) for _, factors in composites) / len(composites) if composites else 0

# Sort high-hit composites by hit count
high_hit_composites.sort(key=lambda x: x[1], reverse=True)
top_high_hit = high_hit_composites[:5]

# Test large numbers: last 10 n values
large_n_test = [limit - i for i in range(10)]
large_number_results = []
for n in large_n_test:
    base10_num = 90 * n + 11
    factors = factor_map.get(n, [])
    prime_factors = factor_composite(factors) if factors else []
    large_number_results.append((base10_num, len(factors), factors, prime_factors))

# Output results (matches provided format)
print(f"Total numbers processed: {limit + 1}")
print(f"Primes (holes, empty factor lists): {len(primes)}")
print(f"First few primes: {primes[:10]}")
print(f"Composites with factor lists (first 5):")
for base10_num, factors in composites[:5]:
    print(f"  {base10_num}: {factors}")
print(f"Omega(n) and prime factors (first 5):")
for base10_num, omega, prime_factors in omega_counts[:5]:
    print(f"  {base10_num}: Omega = {omega}, Factors = {prime_factors}")
print(f"Base-10 limit: {base10_limit}")
print(f"Number of operators applied: {12 * (int(math.sqrt(limit / 90)) + 1)}")
print(f"Execution time: {end_time - start_time:.4f} seconds")
print(f"Average factor list size per composite: {avg_factor_list_size:.2f}")

# Output for high-hit and large numbers
print("\nTop 5 composites with most operator hits:")
for base10_num, hit_count, factors, prime_factors in top_high_hit:
    print(f"  {base10_num}: Hits = {hit_count}, Factors = {prime_factors}, Pairs = {factors}")

print("\nTested large numbers:")
for base10_num, hit_count, factors, prime_factors in large_number_results:
    print(f"  {base10_num}: Hits = {hit_count}, Factors = {prime_factors}, Pairs = {factors}")