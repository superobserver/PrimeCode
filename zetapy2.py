import math
from prettytable import PrettyTable

# Constants
MOD = 90
RESIDUES = [1, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59, 61, 67, 71, 73, 77, 79, 83, 89]
PRIMITIVES = [91, 73, 37, 19, 11, 83, 47, 29, 31, 13, 67, 49, 41, 23, 77, 59, 61, 43, 7, 79, 71, 53, 17, 89]
BASE_PAIRS = [(7, 13), (11, 19), (17, 23), (29, 31), (37, 43), (41, 47),
              (53, 59), (61, 67), (71, 73), (79, 83), (89, 91), (49, 77)]

# Compute operator coefficients l, m for a pair (z, o) and k
def compute_operator(z, o, k):
    # Example: Solve for n1 = 90*1^2 - l*1 + m, n2 = 90*4 - l*2 + m based on paper’s tuning
    n1 = ((z + 90*(1-1)) * (o + 90*(1-1)) - k) / 90  # x=1
    n2 = ((z + 90*(2-1)) * (o + 90*(2-1)) - k) / 90  # x=2
    m = int(n1 + 0.5)  # Round to nearest integer
    l = int(90 - m + n1)  # Simplified derivation
    return l, m

# Precompute operators for each k
OPERATORS = {k: [compute_operator(z, o, k) for z, o in BASE_PAIRS] for k in RESIDUES}

# Broken neighborhood primality test
def is_broken_neighborhood(p):
    k = p % MOD
    if k not in RESIDUES or p < 2:
        return False
    n = (p - k) // MOD
    len_p = math.floor(math.log10(p)) + 1  # Digit length for O(len(p)) simulation
    
    # Check operators for k
    for l, m in OPERATORS[k]:
        # Solve quadratic: 90x^2 - lx + m - n = 0
        a, b, c = 90, -l, m - n
        discriminant = b**2 - 4 * a * c
        if discriminant >= 0:
            sqrt_disc = math.sqrt(discriminant)
            if sqrt_disc.is_integer():
                x1 = (-b + sqrt_disc) / (2 * a)
                x2 = (-b - sqrt_disc) / (2 * a)
                if (x1 >= 0 and x1.is_integer()) or (x2 >= 0 and x2.is_integer()):
                    return False  # Chained: p fits an operator
    return True  # Broken: p doesn’t fit any operator

# Standard primality test for verification
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# Main function with user prompt
def main():
    while True:
        try:
            p = int(input("Enter a number to test for primality (or -1 to exit): "))
            if p == -1:
                break
            if p < 0:
                print("Please enter a non-negative integer.")
                continue
            
            # Test primality
            is_broken = is_broken_neighborhood(p)
            is_actually_prime = is_prime(p)
            
            # Prepare table
            table = PrettyTable()
            table.field_names = ["Number", "Residue (k)", "Broken Neighborhood", "Is Prime", "Correct"]
            k = p % MOD if p % MOD in RESIDUES else "N/A"
            table.add_row([p, k, "Yes" if is_broken else "No", 
                          "Yes" if is_actually_prime else "No",
                          "Yes" if is_broken == is_actually_prime else "No"])
            
            print(f"\nPrimality Test Result for {p}:")
            print(table)
            print(f"Operators used for k = {k}: {OPERATORS.get(k, 'N/A')}")
            
        except ValueError:
            print("Please enter a valid integer.")
    
    print("Exiting...")

if __name__ == "__main__":
    main()