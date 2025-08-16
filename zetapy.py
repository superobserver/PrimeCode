import math
from itertools import product
from prettytable import PrettyTable

# Constants
MOD = 90
RESIDUES = [1, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59, 61, 67, 71, 73, 77, 79, 83, 89]
PRIMITIVES = [91, 73, 37, 19, 11, 83, 47, 29, 31, 13, 67, 49, 41, 23, 77, 59, 61, 43, 7, 79, 71, 53, 17, 89]
ALL_PAIRS = list(product(PRIMITIVES, repeat=2))  # 576 pairs
DR_PRIMITIVES = {1: 19, 2: 11, 4: 13, 5: 23, 7: 7, 8: 17}  # From Table 1, LD=9 for DR consistency

# Digital root calculation
def digital_root(num):
    return 1 + ((num - 1) % 9) if num > 0 else 0

# Generate composite addresses for a given k, z, o pair within bounds
def generate_composites(k, z, o, lower_bound, upper_bound):
    composites = set()
    x_min = max(1, math.ceil(1 + math.sqrt(max(0, lower_bound - k - z * o)) / 90))
    x_max = int(1 + math.sqrt(upper_bound - k - z * o) / 90) + 1
    for x in range(x_min, x_max + 1):
        p = (z + 90 * (x - 1)) * (o + 90 * (x - 1))
        if p < lower_bound:
            continue
        if p > upper_bound:
            break
        n = (p - k) / 90
        if n.is_integer() and n >= 0:
            composites.add(int(p))
    return composites

# Optimized sieve for a segmented range
def quadratic_sieve_segment(lower_bound, upper_bound):
    all_numbers = {k: set() for k in RESIDUES}
    composites = {k: set() for k in RESIDUES}
    for k in RESIDUES:
        n_min = math.ceil((lower_bound - k) / 90)
        n_max = (upper_bound - k) // 90
        for n in range(n_min, n_max + 1):
            num = 90 * n + k
            if lower_bound <= num <= upper_bound:
                all_numbers[k].add(num)
    for k in RESIDUES:
        for z, o in ALL_PAIRS:
            comps = generate_composites(k, z, o, lower_bound, upper_bound)
            composites[k].update(comps)
    primes = {k: all_numbers[k] - composites[k] for k in RESIDUES}
    return primes, composites, all_numbers

# Standard primality test
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# Test a specific number
def test_number(num):
    dr = digital_root(num)
    ld = num % 10
    print(f"\nTesting number: {num}")
    print(f"Digital Root: {dr}, Last Digit: {ld}")
    
    # Rejection criteria
    if dr in [3, 6, 9] or ld in [0, 2, 4, 6, 8]:
        print(f"{num} is trivial (DR in [3,6,9] or LD in [0,2,4,6,8]) - not coprime to 90.")
        return None, None, None
    
    # Identification
    if dr in [1, 2, 4, 5, 7, 8] and ld in [1, 3, 7, 9]:
        k = num % 90
        if k not in RESIDUES:
            print(f"{num} does not belong to the 24 coprime residue classes.")
            return None, None, None
        primitive = DR_PRIMITIVES[dr]
        print(f"Valid number: DR {dr}, LD {ld}, Residue k = {k}, DR Primitive = {primitive}")
        
        # Compute n and test primality
        n = (num - primitive) / 90
        if not n.is_integer():
            print(f"{num} - {primitive} = {num - primitive} is not divisible by 90.")
            return None, None, None
        n = int(n)
        print(f"n = ({num} - {primitive}) / 90 = {n}")
        
        # Use sieve to test n's corresponding number in context
        lower_bound = max(0, num - 100)  # Small range around num
        upper_bound = num + 100
        primes, _, all_numbers = quadratic_sieve_segment(lower_bound, upper_bound)
        is_prime_result = num in primes[k]
        print(f"Primality test result: {num} is {'prime' if is_prime_result else 'composite'}")
        return n, k, is_prime_result
    else:
        print(f"{num} does not meet DR/LD criteria for testing.")
        return None, None, None

# Create tables
def print_tables(primes, all_numbers, lower_bound, upper_bound):
    print(f"\nQuadratic Sieve Results for range {lower_bound} to {upper_bound}:")
    for i in range(0, len(RESIDUES), 4):
        table = PrettyTable()
        table.field_names = ["Residue (k)", "Total Numbers", "Primes Found", "Actual Primes", "Correct", "Sample Primes"]
        for k in RESIDUES[i:i+4]:
            found_primes = primes[k]
            actual_primes = {n for n in all_numbers[k] if is_prime(n)}
            sample = sorted(list(found_primes))[:5]
            table.add_row([k, len(all_numbers[k]), len(found_primes), len(actual_primes),
                          "Yes" if found_primes == actual_primes else "No", sample])
        print(f"\nTable {i//4 + 1}:")
        print(table)

# Main function
def main():
    # User input
    while True:
        try:
            user_num = int(input("Enter a number to test (or -1 to skip to sieve): "))
            if user_num == -1:
                break
            n, k, is_prime_result = test_number(user_num)
            if n is not None and k is not None:
                # Test n's primality directly for comparison
                n_prime = is_prime(n)
                print(f"Testing n = {n} for primality: {'prime' if n_prime else 'composite'}")
            print()
        except ValueError:
            print("Please enter a valid integer.")
    
    # Segmented sieve
    LOWER_BOUND = 10000
    UPPER_BOUND = 11000
    primes, _, all_numbers = quadratic_sieve_segment(LOWER_BOUND, UPPER_BOUND)
    print_tables(primes, all_numbers, LOWER_BOUND, UPPER_BOUND)
    
    total_primes = set().union(*primes.values())
    total_actual = sum(1 for n in range(LOWER_BOUND, UPPER_BOUND + 1) if is_prime(n) and n % 90 in RESIDUES)
    print(f"\nTotal primes found in range: {len(total_primes)}")
    print(f"Total actual primes in range: {total_actual}")

if __name__ == "__main__":
    main()