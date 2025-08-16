import math

# Conway Primitives as defined in the document (page 11)
CONWAY_PRIMES = [7, 11, 13, 17, 23, 29, 31, 37, 41, 43, 47, 49, 53, 57, 59, 61, 67, 71, 73, 77, 79, 83, 89, 91]

def non_self_referential_sieve(limit):
    """Non-Self-Referential Conway Sieve: Tests numbers up to limit for primality using Conway Primitives."""
    # Initialize a list to mark numbers (0: prime, 1+: composite)
    sieve = [0] * (limit + 1)
    sieve[0] = sieve[1] = 1  # 0 and 1 are not prime
    
    # Mark trivial composites (page 7)
    for n in range(2, limit + 1):
        # Rule 1: Digital root 3, 6, 9 (except 3)
        digits = str(n)
        digital_root = sum(int(d) for d in digits) % 9 or 9
        if digital_root in [3, 6, 9] and n != 3:
            sieve[n] = 1
        # Rule 2: Numbers ending in 0, 2, 4, 6, 8 (except 2)
        if digits[-1] in '02468' and n != 2:
            sieve[n] = 1
        # Rule 3: Numbers ending in 0, 1, 5 (except 5)
        if digits[-1] in '015' and n != 5:
            sieve[n] = 1
    
    # Apply Conway Primitives for nontrivial composites (page 11)
    for p in CONWAY_PRIMES:
        for n in range(p, limit + 1, 90):  # Use p + 90n formula
            sieve[n] += 1
    
    # Collect primes (amplitude 0)
    primes = [i for i, mark in enumerate(sieve) if mark == 0]
    return primes

def self_referential_sieve(limit):
    """Self-Referential Conway Sieve: Modified Sieve of Eratosthenes with 24 classes (page 12)."""
    # Initialize 24 lists for Conway Nontrivial Prime classes (e.g., A142315, A142317, etc.)
    prime_classes = {f'A1423{i:02d}': [] for i in range(15, 35)}  # Placeholder for 24 classes
    sieve = [0] * (limit + 1)
    sieve[0] = sieve[1] = 1
    
    # Mark trivial composites as in non-self-referential sieve
    for n in range(2, limit + 1):
        digits = str(n)
        digital_root = sum(int(d) for d in digits) % 9 or 9
        if digital_root in [3, 6, 9] and n != 3:
            sieve[n] = 1
        if digits[-1] in '02468' and n != 2:
            sieve[n] = 1
        if digits[-1] in '015' and n != 5:
            sieve[n] = 1
    
    # Apply Conway Primitives with modular arithmetic (page 15)
    for p in CONWAY_PRIMES:
        for x in range(1, (limit // 90) + 1):
            for params in [
                (120, 34, 7, 53), (132, 48, 19, 29), (120, 38, 17, 43),
                (90, 11, 13, 77), (78, -1, 11, 91), (108, 32, 31, 41),
                (90, 17, 23, 67), (120, 48, 29, 59), (90, 38, 37, 49),
                (78, 5, 47, 73), (60, 17, 61, 71), (60, 4, 79, 89)
            ]:
                l, m, z, o = params
                y = 90 * x * x + l * x + m
                if y > limit:
                    break
                if y >= 0:
                    sieve[y] += 1
                    p1 = z + 90 * (x - 1)
                    p2 = o + 90 * (x - 1)
                    if p1 <= limit:
                        sieve[p1] += 1
                    if p2 <= limit:
                        sieve[p2] += 1
    
    # Assign primes to classes based on digital root and last digit
    for n in range(2, limit + 1):
        if sieve[n] == 0:  # Prime
            digital_root = sum(int(d) for d in str(n)) % 9 or 9
            last_digit = int(str(n)[-1])
            # Map to one of 24 classes (simplified; actual mapping requires OEIS sequence logic)
            class_key = f'A1423{randint(15, 34):02d}'  # Placeholder for class assignment
            if class_key in prime_classes:
                prime_classes[class_key].append(n)
    
    return prime_classes

def twin_prime_sieve(limit):
    """Twin Prime Sieve: Combines A201804 and A201816 to find twin primes (page 23)."""
    primes = non_self_referential_sieve(limit)
    twin_primes = []
    for i in range(len(primes) - 1):
        if primes[i + 1] - primes[i] == 2:
            twin_primes.append((primes[i], primes[i + 1]))
    return twin_primes

# Example usage
if __name__ == "__main__":
    import platform
    import asyncio
    from random import randint  # For placeholder class assignment
    
    async def main():
        limit = 1000  # Example limit
        print("Non-Self-Referential Sieve Primes:", non_self_referential_sieve(limit))
        print("Self-Referential Sieve Classes:", self_referential_sieve(limit))
        print("Twin Primes:", twin_prime_sieve(limit))
        await asyncio.sleep(1.0 / 60)  # Control frame rate for Pyodide

    if platform.system() == "Emscripten":
        asyncio.ensure_future(main())
    else:
        asyncio.run(main())