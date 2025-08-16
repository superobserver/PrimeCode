#!/usr/bin/env python
import cmath
import math
import sys

# Constants for quadratic
a, b = 90, -300

def calculate_epoch(limit):
    return 90 * (limit * limit) - 12 * limit + 1

def solve_quadratic(c):
    d = (b**2) - (4*a*c)
    return (-b - cmath.sqrt(d)) / (2*a), (-b + cmath.sqrt(d)) / (2*a)

def drLD(x, l, m, z, o, listvar, primitive, limit):
    y = 90 * (x * x) - l * x + m
    if y > limit:  # Avoid out-of-bounds access
        return
    listvar[y] += 1
    p, q = z + 90 * (x - 1), o + 90 * (x - 1)
    max_n = int((limit - y) / min(p, q)) + 1  # Calculate max_n once
    for n in range(1, max_n + 1):
        if y + p * n <= limit:
            listvar[y + p * n] += 1
        if y + q * n <= limit:
            listvar[y + q * n] += 1

def process_in_chunks(limit, chunk_size=10000):
    epoch = calculate_epoch(limit)
    print("The epoch range is", epoch)
    c = 250 - epoch
    sol1, sol2 = solve_quadratic(c)
    new_limit = int(sol2.real)  # Only keep the real part of the positive solution
    print('The solutions are {0} and {1}'.format(sol1, sol2))
    
    base10 = (epoch * 90) + 11
    print("This is the base-10 limit:", base10)
    
    A224854 = []  # We'll build this list incrementally
    zero_count = 0
    
    def chunk_generator():
        chunk = [0] * chunk_size
        for x in range(1, new_limit + 1):
            if x % chunk_size == 1:  # New chunk
                yield chunk
                chunk = [0] * chunk_size
            for l, m, z, o, primitive in [
                (120, 34, 7, 53, 11), (132, 48, 19, 29, 11), (120, 38, 17, 43, 11), 
                (90, 11, 13, 77, 11), (78, -1, 11, 91, 11), (108, 32, 31, 41, 11),
                (90, 17, 23, 67, 11), (72, 14, 49, 59, 11), (60, 4, 37, 83, 11),
                (60, 8, 47, 73, 11), (48, 6, 61, 71, 11), (12, 0, 79, 89, 11),
                (76, -1, 13, 91, 13), (94, 18, 19, 67, 13), (94, 24, 37, 49, 13),
                (76, 11, 31, 73, 13), (86, 6, 11, 83, 13), (104, 29, 29, 47, 13),
                (86, 14, 23, 71, 13), (86, 20, 41, 53, 13), (104, 25, 17, 59, 13),
                (14, 0, 77, 89, 13), (94, 10, 7, 79, 13), (76, 15, 43, 61, 13)
            ]:
                drLD(x, l, m, z, o, chunk, primitive, epoch)
            if x % chunk_size == 0 or x == new_limit:  # Process the last chunk or at the end
                A224854.extend(chunk)
                zero_count += chunk.count(0)
        
    for chunk in chunk_generator():
        pass  # Here you can process the chunk if needed, but we're just collecting all into A224854

    # If we need to remove the last 100 elements:
    A224854 = A224854[:epoch]  # Adjust to epoch size if necessary
    new1 = zero_count  # Directly use zero_count since we've been counting zeros as we go

    return new1

# Main execution
if __name__ == "__main__":
    limit = 3300  # Example limit, adjust as needed
    print(process_in_chunks(limit))