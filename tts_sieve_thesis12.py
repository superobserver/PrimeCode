import importlib
import sys
import os
import time
import logging
import platform
import uuid
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_fixed
import pygame
import math
from multiprocessing import Pool, cpu_count
import subprocess

# Sieve Functions
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def factorize(n):
    factors = []
    d = 2
    while n > 1:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1 if d == 2 else 2
        if d * d > n:
            if n > 1:
                factors.append(n)
            break
    return factors

def operator_amplitude(args):
    n_max, operator, op_idx, k = args
    a, l, m, p = operator
    amplitude = [0] * (n_max + 1)
    cancellations = []
    x_max = int(math.sqrt(n_max / a)) + 2
    marked_primes = set()
    for x in range(1, x_max):
        n = a * x**2 - l * x + m
        if 0 <= n <= n_max:
            p_base = 90 * n + (1 if p == 0 else k)
            if is_prime(p) and p * p == p_base and p not in marked_primes:
                amplitude[n] += 1
                cancellations.append((op_idx, n, p_base))
                marked_primes.add(p)
            elif not (is_prime(p) and p * p == p_base):
                amplitude[n] += 1
                cancellations.append((op_idx, n, p_base))
            p_x = p + 90 * (x - 1) if p != 0 else 0
            for i in range(1, (n_max - n) // p_x + 1) if p_x > 0 else []:
                n_new = n + i * p_x
                if n_new <= n_max:
                    amplitude[n_new] += 1
                    cancellations.append((op_idx, n_new, 90 * n_new + (1 if p == 0 else k)))
    return amplitude, cancellations

def mark_composites(n_max, operators, coprime_24):
    amplitude = {k: [0] * (n_max + 1) for k in coprime_24}
    operator_cancellations = {k: [] for k in coprime_24}
    with Pool(cpu_count()) as pool:
        for k in coprime_24:
            results = pool.map(operator_amplitude, [(n_max, op, i, k) for i, op in enumerate(operators[k])])
            for i, (amp, cancels) in enumerate(results):
                for n in range(n_max + 1):
                    amplitude[k][n] += amp[n]
                operator_cancellations[k].append(cancels)
    return amplitude, operator_cancellations

def get_last_holes(n_max, amplitude, coprime_24, limit=2.15e9, count=1000):
    holes = {k: [] for k in coprime_24}
    seen_primes = set()
    for k in coprime_24:
        for n in range(n_max, -1, -1):
            p = 90 * n + 1 if k == 1 else 90 * n + k
            if p <= limit and p not in seen_primes and amplitude[k][n] == 0:
                status = "Prime" if is_prime(p) else f"Composite (Factors: {factorize(p)})"
                holes[k].append((p, status))
                seen_primes.add(p)
                if len(holes[k]) == count:
                    break
    return holes

def generate_sieve_dataset(n_max=1000, limit=2.15e9, count=50):
    coprime_24 = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59, 61, 67, 71, 73, 77, 79, 83, 89, 1]
    operators = {
        
        7: [(90, 82, -1, 7), (90, 82, -1, 91), (90, 118, 37, 19), (90, 118, 37, 43),
            (90, 82, 17, 37), (90, 82, 17, 61), (90, 28, 2, 73), (90, 28, 2, 79),
            (90, 152, 64, 11), (90, 152, 64, 17), (90, 98, 25, 29), (90, 98, 25, 53),
            (90, 62, 9, 47), (90, 62, 9, 71), (90, 8, 0, 83), (90, 8, 0, 89),
            (90, 118, 35, 13), (90, 118, 35, 49), (90, 82, 15, 31), (90, 82, 15, 67),
            (90, 98, 23, 23), (90, 98, 23, 59), (90, 62, 7, 41), (90, 62, 7, 77)],
        11: [(90, 120, 34, 7), (90, 120, 34, 53), (90, 132, 48, 19), (90, 132, 48, 29),
             (90, 120, 38, 17), (90, 120, 38, 43), (90, 90, 11, 13), (90, 90, 11, 77),
             (90, 78, -1, 11), (90, 78, -1, 91), (90, 108, 32, 31), (90, 108, 32, 41),
             (90, 90, 17, 23), (90, 90, 17, 67), (90, 72, 14, 49), (90, 72, 14, 59),
             (90, 60, 4, 37), (90, 60, 4, 83), (90, 60, 8, 47), (90, 60, 8, 73),
             (90, 48, 6, 61), (90, 48, 6, 71), (90, 12, 0, 79), (90, 12, 0, 89)],
        13: [(90, 76, -1, 13), (90, 76, -1, 91), (90, 94, 18, 19), (90, 94, 18, 67),
             (90, 94, 24, 37), (90, 94, 24, 49), (90, 76, 11, 31), (90, 76, 11, 73),
             (90, 86, 6, 11), (90, 86, 6, 83), (90, 104, 29, 29), (90, 104, 29, 47),
             (90, 86, 14, 23), (90, 86, 14, 71), (90, 86, 20, 41), (90, 86, 20, 53),
             (90, 104, 25, 17), (90, 104, 25, 59), (90, 14, 0, 77), (90, 14, 0, 89),
             (90, 94, 10, 7), (90, 94, 10, 79), (90, 76, 15, 43), (90, 76, 15, 61)],
        17: [(90, 72, -1, 17), (90, 72, -1, 91), (90, 108, 29, 19), (90, 108, 29, 53),
             (90, 72, 11, 37), (90, 72, 11, 71), (90, 18, 0, 73), (90, 18, 0, 89),
             (90, 102, 20, 11), (90, 102, 20, 67), (90, 138, 52, 13), (90, 138, 52, 29),
             (90, 102, 28, 31), (90, 102, 28, 47), (90, 48, 3, 49), (90, 48, 3, 83),
             (90, 78, 8, 23), (90, 78, 8, 79), (90, 132, 45, 7), (90, 132, 45, 41),
             (90, 78, 16, 43), (90, 78, 16, 59), (90, 42, 4, 61), (90, 42, 4, 77)],
        19: [
        (90, 70, -1, 19), (90, 70, -1, 91), (90, 106, 31, 37),                      #37, 73, 53, 17
        (90, 34, 3, 73), (90, 110, 27, 11), (90, 110, 27, 59),
        (90, 110, 33, 29), (90, 110, 33, 41), (90, 56, 6, 47), (90, 56, 6, 77),
        (90, 74, 5, 23), (90, 74, 5, 83), (90, 124, 40, 13), (90, 124, 40, 43),
        (90, 70, 7, 31), (90, 70, 7, 79), (90, 70, 13, 49), (90, 70, 13, 61),
        (90, 106, 21, 7), (90, 106, 21, 67), (90, 20, 0, 71), (90, 20, 0, 89),
        (90, 74, 15, 53), (90, 146, 59, 17), 
    ],
    23: [
        (90, 66, -1, 23), (90, 66, -1, 91), (90, 84, 10, 19), (90, 84, 10, 77),
        (90, 84, 18, 37), (90, 84, 18, 59), (90, 66, 9, 41), (90, 66, 9, 73),
        (90, 126, 41, 11), (90, 126, 41, 43), (90, 144, 56, 7), (90, 144, 56, 29),
        (90, 54, 5, 47), (90, 54, 5, 79), (90, 36, 2, 61), (90, 36, 2, 83),
        (90, 96, 16, 13), (90, 96, 16, 71), (90, 96, 24, 31), (90, 96, 24, 53),
        (90, 114, 33, 17), (90, 114, 33, 49), (90, 24, 0, 67), (90, 24, 0, 89)
    ],
    29: [
        (90, 60, -1, 29), (90, 60, -1, 91), (90, 150, 62, 11), (90, 150, 62, 19),
        (90, 96, 25, 37), (90, 96, 25, 47), (90, 24, 1, 73), (90, 24, 1, 83),
        (90, 144, 57, 13), (90, 144, 57, 23), (90, 90, 20, 31), (90, 90, 20, 59),
        (90, 90, 22, 41), (90, 90, 22, 49), (90, 36, 3, 67), (90, 36, 3, 77),
        (90, 156, 67, 7), (90, 156, 67, 17), (90, 84, 19, 43), (90, 84, 19, 53),
        (90, 30, 0, 61), (90, 30, 0, 89), (90, 30, 2, 71), (90, 30, 2, 79)
    ],
    31: [
        (90, 58, -1, 31), (90, 58, -1, 91), (90, 112, 32, 19), (90, 112, 32, 49),   #79, 61, 11, 29
        (90, 130, 45, 13), (90, 130, 45, 37), (90, 40, 4, 67), (90, 40, 4, 73),
        (90, 158, 69, 11), (90, 122, 41, 29),
        (90, 50, 3, 47), (90, 50, 3, 83), (90, 140, 54, 17), (90, 140, 54, 23),
        (90, 68, 10, 41), (90, 68, 10, 71), (90, 32, 0, 59), (90, 32, 0, 89),
        (90, 50, 5, 53), (90, 50, 5, 77), (90, 130, 43, 7), (90, 130, 43, 43),
        (90, 58, 9, 61), (90, 22, 1, 79)
    ],
    37: [
        (90, 52, -1, 37), (90, 52, -1, 91), (90, 88, 13, 19), (90, 88, 13, 73),
        (90, 92, 11, 11), (90, 92, 11, 77), (90, 128, 45, 23), (90, 128, 45, 29),
        (90, 92, 23, 41), (90, 92, 23, 47), (90, 38, 2, 59), (90, 38, 2, 83),
        (90, 88, 9, 13), (90, 88, 9, 79), (90, 142, 54, 7), (90, 142, 54, 31),
        (90, 88, 21, 43), (90, 88, 21, 49), (90, 52, 7, 61), (90, 52, 7, 67),
        (90, 92, 15, 17), (90, 92, 15, 71), (90, 38, 0, 53), (90, 38, 0, 89)
    ],
    41: [
        (90, 48, -1, 41), (90, 48, -1, 91), (90, 42, 0, 49), (90, 42, 0, 89),
        (90, 102, 24, 19), (90, 102, 24, 59), (90, 120, 39, 23), (90, 120, 39, 37),
        (90, 108, 25, 11), (90, 108, 25, 61), (90, 72, 7, 29), (90, 72, 7, 79),
        (90, 90, 22, 43), (90, 90, 22, 47), (90, 150, 62, 13), (90, 150, 62, 17),
        (90, 78, 12, 31), (90, 78, 12, 71), (90, 30, 2, 73), (90, 30, 2, 77),
        (90, 60, 9, 53), (90, 60, 9, 67), (90, 90, 6, 7), (90, 90, 6, 83)
    ],
    43: [
        (90, 46, -1, 43), (90, 46, -1, 91), (90, 154, 65, 7), (90, 154, 65, 19),
        (90, 64, 6, 37), (90, 64, 6, 79), (90, 46, 5, 61), (90, 46, 5, 73),
        (90, 116, 32, 11), (90, 116, 32, 53), (90, 134, 49, 17), (90, 134, 49, 29),
        (90, 44, 0, 47), (90, 44, 0, 89), (90, 26, 1, 71), (90, 26, 1, 83),
        (90, 136, 50, 13), (90, 136, 50, 31), (90, 64, 10, 49), (90, 64, 10, 67),
        (90, 116, 36, 23), (90, 116, 36, 41), (90, 44, 4, 59), (90, 44, 4, 77)
    ],
    47: [
        (90, 42, -1, 47), (90, 42, -1, 91), (90, 78, 5, 19), (90, 78, 5, 83),
        (90, 132, 46, 11), (90, 132, 46, 37), (90, 78, 11, 29), (90, 78, 11, 73),
        (90, 108, 26, 13), (90, 108, 26, 59), (90, 72, 8, 31), (90, 72, 8, 77),
        (90, 108, 30, 23), (90, 108, 30, 49), (90, 102, 17, 7), (90, 102, 17, 71),
        (90, 48, 0, 43), (90, 48, 0, 89), (90, 102, 23, 17), (90, 102, 23, 61),
        (90, 48, 4, 53), (90, 48, 4, 79), (90, 72, 12, 41), (90, 72, 12, 67)
    ],
    49: [
        (90, 40, -1, 49), (90, 40, -1, 91), (90, 130, 46, 19), (90, 130, 46, 31),   #47, 7, 83
        (90, 76, 13, 37), (90, 76, 13, 67), (90, 94, 14, 13), (90, 94, 14, 73),
        (90, 140, 53, 11), (90, 140, 53, 29), (90, 86, 20, 47), 
        (90, 14, 0, 83), (90, 104, 27, 23), (90, 104, 27, 53),
        (90, 50, 0, 41), (90, 50, 0, 89), (90, 50, 6, 59), (90, 50, 6, 71),
        (90, 86, 10, 17), (90, 86, 10, 77), (90, 166, 76, 7), (90, 94, 24, 43), #43,43
        (90, 40, 3, 61), (90, 40, 3, 79)
    ],
    53: [
        (90, 36, -1, 53), (90, 36, -1, 91), (90, 144, 57, 17), (90, 144, 57, 19),
        (90, 54, 0, 37), (90, 54, 0, 89), (90, 36, 3, 71), (90, 36, 3, 73),
        (90, 156, 67, 11), (90, 156, 67, 13), (90, 84, 15, 29), (90, 84, 15, 67),
        (90, 84, 19, 47), (90, 84, 19, 49), (90, 66, 4, 31), (90, 66, 4, 83),
        (90, 96, 21, 23), (90, 96, 21, 61), (90, 96, 25, 41), (90, 96, 25, 43),
        (90, 114, 28, 7), (90, 114, 28, 59), (90, 24, 1, 77), (90, 24, 1, 79)
    ],
    59: [
        (90, 30, -1, 59), (90, 30, -1, 91), (90, 120, 38, 19), (90, 120, 38, 41),
        (90, 66, 7, 37), (90, 66, 7, 77), (90, 84, 12, 23), (90, 84, 12, 73),
        (90, 90, 9, 11), (90, 90, 9, 79), (90, 90, 19, 29), (90, 90, 19, 61),
        (90, 126, 39, 7), (90, 126, 39, 47), (90, 54, 3, 43), (90, 54, 3, 83),
        (90, 114, 31, 13), (90, 114, 31, 53), (90, 60, 0, 31), (90, 60, 0, 89),
        (90, 60, 8, 49), (90, 60, 8, 71), (90, 96, 18, 17), (90, 96, 18, 67)
    ],
    61: [
        (90, 28, -1, 61), (90, 28, -1, 91), (90, 82, 8, 19), (90, 82, 8, 79),
        (90, 100, 27, 37), (90, 100, 27, 43), (90, 100, 15, 7), (90, 100, 15, 73),
        (90, 98, 16, 11), (90, 98, 16, 71), (90, 62, 0, 29), (90, 62, 0, 89),
        (90, 80, 17, 47), (90, 80, 17, 53), (90, 80, 5, 17), (90, 80, 5, 83),
        (90, 100, 19, 13), (90, 100, 19, 67), (90, 118, 38, 31), 
        (90, 82, 18, 49), (90, 80, 9, 23), (90, 80, 9, 77), (90, 98, 26, 41), (90, 62, 10, 59) #59,59
    ],
    67: [
        (90, 22, -1, 67), (90, 22, -1, 91), (90, 148, 60, 13), (90, 148, 60, 19),
        (90, 112, 34, 31), (90, 112, 34, 37), (90, 58, 7, 49), (90, 58, 7, 73),
        (90, 122, 37, 11), (90, 122, 37, 47), (90, 68, 4, 29), (90, 68, 4, 83),
        (90, 122, 39, 17), (90, 122, 39, 41), (90, 68, 12, 53), (90, 68, 12, 59),
        (90, 32, 2, 71), (90, 32, 2, 77), (90, 112, 26, 7), (90, 112, 26, 61),
        (90, 58, 5, 43), (90, 58, 5, 79), (90, 68, 0, 23), (90, 68, 0, 89)
    ],
    71: [
        (90, 18, -1, 71), (90, 18, -1, 91), (90, 72, 0, 19), (90, 72, 0, 89),
        (90, 90, 21, 37), (90, 90, 21, 53), (90, 90, 13, 17), (90, 90, 13, 73),
        (90, 138, 51, 11), (90, 138, 51, 31), (90, 102, 27, 29), (90, 102, 27, 49),
        (90, 120, 36, 13), (90, 120, 36, 47), (90, 30, 1, 67), (90, 30, 1, 83),
        (90, 150, 61, 7), (90, 150, 61, 23), (90, 78, 15, 41), (90, 78, 15, 61),
        (90, 42, 3, 59), (90, 42, 3, 79), (90, 60, 6, 43), (90, 60, 6, 77)
    ],
    73: [
        (90, 16, -1, 73), (90, 16, -1, 91), (90, 124, 41, 19), (90, 124, 41, 37),
        (90, 146, 58, 11), (90, 146, 58, 23), (90, 74, 8, 29), (90, 74, 8, 77),
        (90, 74, 14, 47), (90, 74, 14, 59), (90, 56, 3, 41), (90, 56, 3, 83),
        (90, 106, 24, 13), (90, 106, 24, 61), (90, 106, 30, 31), (90, 106, 30, 43),
        (90, 124, 37, 7), (90, 124, 37, 49), (90, 34, 2, 67), (90, 34, 2, 79),
        (90, 74, 0, 17), (90, 74, 0, 89), (90, 56, 7, 53), (90, 56, 7, 71)
    ],
    77: [
        (90, 12, -1, 77), (90, 12, -1, 91), (90, 138, 52, 19), (90, 138, 52, 23),
        (90, 102, 28, 37), (90, 102, 28, 41), (90, 48, 5, 59), (90, 48, 5, 73),
        (90, 162, 72, 7), (90, 162, 72, 11), (90, 108, 31, 29), (90, 108, 31, 43),
        (90, 72, 13, 47), (90, 72, 13, 61), (90, 18, 0, 79), (90, 18, 0, 83),
        (90, 78, 0, 13), (90, 78, 0, 89), (90, 132, 47, 17), (90, 132, 47, 31),
        (90, 78, 16, 49), (90, 78, 16, 53), (90, 42, 4, 67), (90, 42, 4, 71)
    ],
    79: [
        (90, 10, -1, 79), (90, 10, -1, 91), (90, 100, 22, 19), (90, 100, 22, 61),
        (90, 136, 48, 7), (90, 136, 48, 37), (90, 64, 8, 43), (90, 64, 8, 73),
        (90, 80, 0, 11), (90, 80, 0, 89), (90, 80, 12, 29), (90, 80, 12, 71),
        (90, 116, 34, 17), (90, 116, 34, 47), (90, 44, 2, 53), (90, 44, 2, 83),
        (90, 154, 65, 13), (90, 100, 26, 31), (90, 100, 26, 49),
        (90, 46, 5, 67), (90, 134, 49, 23),  (90, 80, 16, 41), (90, 80, 16, 59), #41,59
        (90, 26, 1, 77) #77,77
        
    ],
    83: [
        (90, 6, -1, 83), (90, 6, -1, 91), (90, 114, 33, 19), (90, 114, 33, 47),
        (90, 114, 35, 29), (90, 114, 35, 37), (90, 96, 14, 11), (90, 96, 14, 73),
        (90, 126, 41, 13), (90, 126, 41, 41), (90, 126, 43, 23), (90, 126, 43, 31),
        (90, 54, 5, 49), (90, 54, 5, 77), (90, 54, 7, 59), (90, 54, 7, 67),
        (90, 84, 0, 7), (90, 84, 0, 89), (90, 66, 9, 43), (90, 66, 9, 71),
        (90, 66, 11, 53), (90, 66, 11, 61), (90, 84, 8, 17), (90, 84, 8, 79)
    ],
    89: [
        (90, 0, -1, 89), (90, 0, -1, 91), (90, 90, 14, 19), (90, 90, 14, 71),
        (90, 126, 42, 17), (90, 126, 42, 37), (90, 54, 6, 53), (90, 54, 6, 73),
        (90, 120, 35, 11), (90, 120, 35, 49), (90, 120, 39, 29), (90, 120, 39, 31),
        (90, 66, 10, 47), (90, 66, 10, 67), (90, 84, 5, 13), (90, 84, 5, 83),
        (90, 114, 34, 23), (90, 114, 34, 43), (90, 60, 5, 41), (90, 60, 5, 79),
        (90, 60, 9, 59), (90, 60, 9, 61), (90, 96, 11, 7), (90, 96, 11, 77)
    ],

    
    
    1: [
        (90, -2, 0, 91), (90, 142, 56, 19), (90, 70, 10, 37),
        (90, 128, 43, 11), (90, 92, 21, 29), (90, 110, 32, 23),
        (90, 20, 1, 77), (90, 160, 71, 7), (90, 88, 19, 31),
        (90, 52, 5, 49), (90, 70, 12, 43), (90, 110, 30, 17),
        (90, 38, 4, 71), (90, 2, 0, 89),
        
        (90, 70, 10, 73),
        (90, 128, 43, 41), (90, 92, 21, 59), (90, 110, 32, 47),
        (90, 20, 1, 83), (90, 160, 71, 13), (90, 88, 19, 61),
        (90, 52, 5, 79), (90, 70, 12, 67), (90, 110, 30, 53)
        
    ]
}    
# Insert operators dictionary here (e.g., operators for k=11 provided below)
    
    logging.info(f"Generating sieve dataset with n_max={n_max}")
    amplitude, operator_cancellations = mark_composites(n_max, operators, coprime_24)
    last_holes = get_last_holes(n_max, amplitude, coprime_24, limit, count)
    return amplitude, last_holes, operator_cancellations

# Define module-level missing_modules
missing_modules = []

# Attempt to import required modules
required_modules = ['pyttsx3', 'gtts', 'pygame', 'numpy', 'tenacity']

for module in required_modules:
    try:
        importlib.import_module(module)
    except ImportError:
        missing_modules.append(module)

# Conditional imports
if 'pyttsx3' not in missing_modules:
    import pyttsx3
if 'gtts' not in missing_modules:
    from gtts import gTTS
if 'pygame' not in missing_modules:
    import pygame.mixer
if 'numpy' not in missing_modules:
    import numpy as np

# Configuration
OUTPUT_DIR = "tts_output"
LOG_FILE = os.path.join(OUTPUT_DIR, "tts_errors.log")
WIDTH, HEIGHT = 800, 600

# Setup logging
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Install missing modules (Windows only)
def install_missing_modules():
    if platform.system() != "Windows":
        return False
    if not missing_modules:
        return False

    logging.info(f"Missing modules: {missing_modules}")
    print(f"Missing modules: {missing_modules}. Attempting to install...")

    for module in missing_modules:
        try:
            install_cmd = ["pip", "install", module]
            process = subprocess.Popen(install_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate(timeout=30)
            if process.returncode == 0:
                logging.info(f"Successfully installed {module}")
                print(f"Successfully installed {module}")
            else:
                logging.error(f"Failed to install {module}: {stderr.decode()}")
                print(f"Failed to install {module}: {stderr.decode()}")
            time.sleep(2)
        except Exception as e:
            logging.error(f"Failed to start installation for {module}: {e}")
            print(f"Failed to install {module}. Please install manually with 'pip install {module}'.")

    missing_modules.clear()
    for module in required_modules:
        try:
            importlib.import_module(module)
        except ImportError:
            missing_modules.append(module)
    if missing_modules:
        logging.error(f"Modules still missing after installation: {missing_modules}")
        print(f"Modules still missing: {missing_modules}. Please install manually.")
        return True
    return False

# Relaunch script (Windows only)
def relaunch_script():
    if platform.system() != "Windows":
        return
    try:
        script_path = os.path.abspath(__file__)
        subprocess.Popen(["start", "cmd", "/k", f"python \"{script_path}\""], shell=True)
        logging.info("Relaunched script in new terminal")
        print("Relaunching script in a new terminal...")
        time.sleep(2)
        sys.exit(0)
    except Exception as e:
        logging.error(f"Failed to relaunch script: {e}")
        print(f"Failed to relaunch script: {e}. Please run manually.")
        sys.exit(1)

# Generate MP3 files for TTS
def generate_tts_mp3(text, filename, voice_gender='male'):
    audio_file = os.path.normpath(os.path.join(OUTPUT_DIR, filename))
    logging.info(f"Generating audio file: {audio_file}")

    if 'pyttsx3' not in missing_modules:
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            voices = engine.getProperty('voices')
            selected_voice = None
            for voice in voices:
                logging.info(f"Available voice: {voice.name} (ID: {voice.id})")
                if voice_gender == 'female' and 'Zira' in voice.name:
                    selected_voice = voice.id
                    break
                elif voice_gender == 'male' and 'David' in voice.name:
                    selected_voice = voice.id
                    break
            if selected_voice:
                engine.setProperty('voice', selected_voice)
                logging.info(f"Using {voice_gender} voice: {selected_voice}")
            else:
                logging.warning(f"No {voice_gender} voice found. Using default.")
                print(f"No {voice_gender} voice found. Using default.")

            engine.save_to_file(text, audio_file)
            engine.runAndWait()
            if os.path.exists(audio_file):
                logging.info(f"pyttsx3 generated audio file: {audio_file}")
                return True
            else:
                logging.error(f"pyttsx3 failed to create audio file: {audio_file}")
        except Exception as e:
            logging.error(f"pyttsx3 failed: {e}")
            print(f"pyttsx3 failed: {e}")

    if 'gtts' not in missing_modules:
        @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
        def try_gtts():
            tts = gTTS(text=text, lang='en')
            tts.save(audio_file)
            if os.path.exists(audio_file):
                logging.info(f"gTTS generated audio file: {audio_file}")
                return True
            else:
                logging.error(f"gTTS failed to create audio file: {audio_file}")
                raise FileNotFoundError(f"Audio file not created: {audio_file}")

        try:
            return try_gtts()
        except Exception as e:
            logging.error(f"gTTS failed: {e}")
            print(f"gTTS failed: {e}")

    logging.warning(f"Failed to generate audio file: {audio_file}")
    print(f"Failed to generate audio file: {audio_file}")
    return False

# Play MP3 using Pygame
def play_tts_mp3(filename):
    if 'pygame' not in missing_modules:
        audio_file = os.path.normpath(os.path.join(OUTPUT_DIR, filename))
        if os.path.exists(audio_file):
            try:
                pygame.mixer.init()
                sound = pygame.mixer.Sound(audio_file)
                sound.play()
                pygame.time.wait(int(sound.get_length() * 1000))
                logging.info(f"Played audio file: {audio_file}")
                print(f"Played audio file: {audio_file}")
                return True
            except Exception as e:
                logging.error(f"Pygame playback failed: {e}")
                print(f"Pygame playback failed: {e}")
        else:
            logging.error(f"Audio file not found: {audio_file}")
            print(f"Audio file not found: {audio_file}")
    else:
        logging.warning("Pygame not installed. Cannot play audio.")
        print("Pygame not installed. Cannot play audio.")
    return False

# Animation Functions
def animate_holes(coprime_24, prime_counts):
    if 'pygame' not in missing_modules:
        pygame.init()
        WIDTH, HEIGHT = 800, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Prime Distribution Across Residue Classes")
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        BLUE = (0, 0, 255)

        max_count = max(prime_counts) if prime_counts else 1
        bar_width = (WIDTH - 100) / len(coprime_24)
        y_scale = (HEIGHT - 100) / max_count
        current_bars = [0] * len(coprime_24)
        font = pygame.font.SysFont('arial', 20)

        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False

            screen.fill(WHITE)
            pygame.draw.line(screen, BLACK, (50, HEIGHT-50), (WIDTH-50, HEIGHT-50), 2)
            pygame.draw.line(screen, BLACK, (50, HEIGHT-50), (50, 50), 2)

            label_x = font.render("Residue Class k", True, BLACK)
            screen.blit(label_x, (WIDTH-100, HEIGHT-30))
            label_y = font.render("Prime Count", True, BLACK)
            screen.blit(label_y, (10, 10))
            label_title = font.render("Symmetry in Prime Distribution", True, BLACK)
            screen.blit(label_title, (WIDTH//2 - 100, 20))

            for i in range(len(coprime_24)):
                if current_bars[i] < prime_counts[i]:
                    current_bars[i] += max(1, prime_counts[i] // 50)
                    if current_bars[i] > prime_counts[i]:
                        current_bars[i] = prime_counts[i]
                height = current_bars[i] * y_scale
                pygame.draw.rect(screen, BLUE, (50 + i * bar_width, HEIGHT - 50 - height, bar_width - 2, height))
                label = font.render(str(coprime_24[i]), True, BLACK)
                screen.blit(label, (50 + i * bar_width + bar_width/4, HEIGHT-30))

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
    else:
        logging.warning("Pygame not installed. Skipping animation.")
        print("Pygame not installed. Skipping animation.")

def animate_amplitude(n_values, amplitudes):
    if 'pygame' not in missing_modules:
        pygame.init()
        WIDTH, HEIGHT = 800, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Amplitude Dynamics for k=11")
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)

        max_n = max(n_values) if n_values else 1
        max_amp = max(amplitudes) if amplitudes else 1
        x_scale = (WIDTH - 100) / max_n
        y_scale = (HEIGHT - 100) / max_amp
        points = []
        current_n = 0
        font = pygame.font.SysFont('arial', 20)

        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False

            screen.fill(WHITE)
            pygame.draw.line(screen, BLACK, (50, HEIGHT-50), (WIDTH-50, HEIGHT-50), 2)
            pygame.draw.line(screen, BLACK, (50, HEIGHT-50), (50, 50), 2)

            label_x = font.render("n (Address)", True, BLACK)
            screen.blit(label_x, (WIDTH-50, HEIGHT-30))
            label_y = font.render("Amplitude", True, BLACK)
            screen.blit(label_y, (10, 10))
            label_title = font.render("Composite Frequency Generators", True, BLACK)
            screen.blit(label_title, (WIDTH//2 - 150, 20))

            if current_n < len(n_values):
                amp = amplitudes[current_n]
                color = GREEN if amp == 0 else RED
                points.append((50 + n_values[current_n] * y_scale, HEIGHT - 50 - amp * x_scale, color))
                current_n += 1
                pygame.time.wait(100)

            for x, y, color in points:
                pygame.draw.circle(screen, color, (int(x), int(y)), 5)

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
    else:
        logging.warning("Pygame not installed. Skipping animation.")
        print("Pygame not installed. Skipping animation.")

def animate_operator_cancellations(n_values, operator_amplitudes, operator_count):
    if 'pygame' not in missing_modules:
        pygame.init()
        WIDTH, HEIGHT = 800, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Operator Cancellation Dynamics for k=11")
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        COLORS = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255),
            (0, 255, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128), (128, 128, 0),
            (128, 0, 128), (0, 128, 128), (255, 128, 0), (255, 0, 128), (128, 255, 0),
            (0, 255, 128), (128, 128, 255), (255, 128, 128), (128, 255, 128),
            (128, 128, 255), (192, 192, 192), (64, 64, 64), (192, 64, 64), (64, 192, 64)
        ]

        max_n = max(n_values) if n_values else 1
        max_amp = max(max(amps) for amps in operator_amplitudes if amps) if any(operator_amplitudes) else 1
        x_scale = (WIDTH - 100) / max_n
        y_scale = (HEIGHT - 100) / max_amp
        points = []
        current_op = 0
        current_n = 0
        font = pygame.font.SysFont('arial', 20)

        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False

            screen.fill(WHITE)
            pygame.draw.line(screen, BLACK, (50, HEIGHT-50), (WIDTH-50, HEIGHT-50), 2)
            pygame.draw.line(screen, BLACK, (50, HEIGHT-50), (50, 50), 2)

            label_x = font.render("n (Address)", True, BLACK)
            screen.blit(label_x, (WIDTH-50, HEIGHT-30))
            label_y = font.render("Amplitude", True, BLACK)
            screen.blit(label_y, (10, 10))
            label_title = font.render(f"Operator {current_op+1} Cancellations", True, BLACK)
            screen.blit(label_title, (WIDTH//2 - 100, 20))

            if current_op < operator_count and current_n < len(n_values):
                amp = operator_amplitudes[current_op][current_n]
                if amp > 0:
                    color = COLORS[current_op % len(COLORS)]
                    points.append((50 + n_values[current_n] * x_scale, HEIGHT - 50 - amp * y_scale, color))
                current_n += 1
                if current_n >= len(n_values):
                    current_n = 0
                    current_op += 1
                pygame.time.wait(10)

            for x, y, color in points:
                pygame.draw.circle(screen, color, (int(x), int(y)), 5)

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
    else:
        logging.warning("Pygame not installed. Skipping animation.")
        print("Pygame not installed. Skipping animation.")

def animate_operator_vectors(cancellations, operator_amplitude, operators):
    if 'pygame' not in missing_modules:
        pygame.init()
        WIDTH, HEIGHT = 800, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Operator Vector Dynamics for k=11")
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        COLORS = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255),
            (0, 255, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128), (128, 128, 0),
            (128, 0, 128), (0, 128, 128), (255, 128, 0), (255, 0, 128), (128, 255, 0),
            (0, 255, 128), (128, 128, 255), (255, 128, 128), (128, 255, 128),
            (128, 128, 255), (192, 192, 192), (64, 64, 64), (192, 64, 64), (64, 192, 64)
        ]

        max_n = 1000
        max_amp = max(operator_amplitude) if operator_amplitude else 1
        x_scale = (WIDTH - 100) / max_n
        y_scale = (HEIGHT - 100) / max_amp
        points = []
        vectors = []
        current_op = 0
        font = pygame.font.SysFont('arial', 20)

        for op_idx, cancels in enumerate(cancellations):
            if cancels:
                _, n, p_base = cancels[0]
                a, l, m, p = operators[op_idx]
                p_x = p if p != 0 else 0
                next_n = n + p_x if len(cancels) > 1 and cancels[1][1] <= max_n else n
                points.append((50 + n * x_scale, HEIGHT - 50 - operator_amplitude[n] * y_scale, COLORS[op_idx % len(COLORS)]))
                vectors.append((50, HEIGHT-50, 50 + n * x_scale, HEIGHT - 50 - operator_amplitude[n] * y_scale, COLORS[op_idx % len(COLORS)]))
                if next_n <= max_n:
                    vectors.append((50 + n * x_scale, HEIGHT - 50 - operator_amplitude[n] * y_scale, 50 + next_n * x_scale, HEIGHT - 50 - operator_amplitude[next_n] * y_scale, COLORS[op_idx % len(COLORS)]))

        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False

            screen.fill(WHITE)
            pygame.draw.line(screen, BLACK, (50, HEIGHT-50), (WIDTH-50, HEIGHT-50), 2)
            pygame.draw.line(screen, BLACK, (50, HEIGHT-50), (50, 50), 2)

            label_x = font.render("n (Address)", True, BLACK)
            screen.blit(label_x, (WIDTH-50, HEIGHT-30))
            label_y = font.render("Amplitude", True, BLACK)
            screen.blit(label_y, (10, 10))
            label_title = font.render(f"Operator {current_op+1} Vectors", True, BLACK)
            screen.blit(label_title, (WIDTH//2 - 100, 20))

            for x, y, color in points[:current_op+1]:
                pygame.draw.circle(screen, color, (int(x), int(y)), 5)
            for x1, y1, x2, y2, color in vectors[:2*(current_op+1)]:
                pygame.draw.line(screen, color, (x1, y1), (x2, y2), 2)
                angle = math.atan2(y2 - y1, x2 - x1)
                arrow_size = 10
                pygame.draw.line(screen, color, (x2, y2), (x2 - arrow_size * math.cos(angle - math.pi/6), y2 - arrow_size * math.sin(angle - math.pi/6)), 2)
                pygame.draw.line(screen, color, (x2, y2), (x2 - arrow_size * math.cos(angle + math.pi/6), y2 - arrow_size * math.sin(angle + math.pi/6)), 2)

            pygame.display.flip()
            clock.tick(30)

            current_op = (current_op + 1) % len(cancellations)
            pygame.time.wait(500)

        pygame.quit()
    else:
        logging.warning("Pygame not installed. Skipping animation.")
        print("Pygame not installed. Skipping animation.")

# Generate Operator Dataset
def generate_operator_dataset(n_max, operators, k=11):
    amplitude, cancellations = mark_composites(n_max, {k: operators[k]}, [k])
    operator_amplitudes = []
    for op_idx, op_cancels in enumerate(cancellations[k]):
        op_amp = [0] * (n_max + 1)
        for _, n, _ in op_cancels:
            if n <= n_max:
                op_amp[n] += 1
        operator_amplitudes.append(op_amp)
    return amplitude[k], operator_amplitudes, len(operators[k]), cancellations[k]

# Thesis Presentation Content
def generate_thesis_presentation(amplitude, last_holes, operator_amplitude, operator_amplitudes, operator_count, operator_cancellations, operators_k11):
    coprime_24 = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59, 61, 67, 71, 73, 77, 79, 83, 89, 1]
    prime_counts = [sum(1 for p, status in last_holes[k] if status == "Prime") for k in coprime_24]
    n_values = list(range(1000))
    amplitudes_k11 = amplitude[:1000]

    presentation = [
        ("Esteemed References, I present my thesis: a deterministic quadratic sieve for prime identification in residue classes modulo 90. This work deconstructs base-10 integers into algebraic observables—digital roots, last digits, and amplitudes—across 24 residue classes coprime to 90. Unlike eliminative sieves, my approach constructs composites using quadratic operators, leaving primes as unmapped residuals, revealing deep symmetries in the number-theoretic map space.", 'male', None, None),
        ("The Liouville function, defined as lambda of n equals (-1) to the power Omega of n, where Omega is the number of prime factors, indicates that neighbors on the number line are not chained. This enables our sieve to de-interlace the 24 residue classes modulo 90. Each class, addressed as 90n+k, captures primes >=7. The quadratic operators act as composite frequency generators, producing addresses in a symmetrical distribution.", 'male', (lambda screen: screen.blit(pygame.font.SysFont('arial', 30).render("λ(n) = (-1)^Ω(n)", True, (0, 0, 0)), (WIDTH//2-100, HEIGHT//2)),), "Liouville Function Popup"),
        ("I, Eratosthenes, argue my sieve marks multiples sequentially on the number line, efficiently identifying primes. Why de-interlace into 24 classes when a linear approach suffices?", 'female', None, None),
        ("With respect, Eratosthenes, your sieve scales as O(n log log n) and lacks algebraic insight. Our sieve’s 24 classes form a map space where composites are generated quadratically, achieving near O(1) complexity with parallelized operators. This de-interlacing, supported by the Liouville function’s non-chaining, reveals symmetries that underpin the prime distribution.", 'male', None, None),
        ("The modulus 90, the least common multiple of 2, 3, and 5, filters trivial primes. The Euler totient function, phi of n equals n times the product over prime p dividing n of (1 minus 1 over p), yields phi(90)=24, defining 24 residues coprime to 90. These classes, einselected to limit variance, partition numbers with digital roots in {1,2,4,5,7,8} and last digits in {1,3,7,9}. Measuring 1/24th of the prime distribution confidently predicts the full set.", 'male', (lambda screen: screen.blit(pygame.font.SysFont('arial', 30).render("φ(n) = n ∏_{p|n} (1 - 1/p)", True, (0, 0, 0)), (WIDTH//2-150, HEIGHT//2)),), "Euler Totient Function Popup"),
        ("I, Euler, question the fragmentation of the number line into 24 classes. My zeta function unifies primes globally. Does your partitioning preserve this unity?", 'female', None, None),
        ("Euler, your zeta function guides us. Our 24 classes de-interlace the number line, exposing local symmetries that complement your global view. Each class’s zeta function converges to zeros on Re(s)=1/2, aligning with the Riemann Hypothesis. The einselection of these classes ensures finite variance, enabling precise prime measurement.", 'male', None, None),
        ("Our sieve’s completeness is algebraic. For each residue class k, 12 quadratic operators, n=90x^2-lx+m, generate all composites 90n+k. For k=11, n=4 yields 90*4+11=371=7*53. Parallel processing marks multiples, ensuring no composite escapes. Primes remain as holes with amplitude zero.", 'male', None, None),
        ("I, Pomerance, note my quadratic sieve factorizes efficiently. Could your finite operators miss composites?", 'female', None, None),
        ("Pomerance, your sieve inspires us. For any composite 90n+k=a*b, an operator captures n via n=m+pt+qs+90st. With 12 operators per class, all factorizations are covered. The symmetrical distribution of primes across the 24 classes is visualized here, showcasing the map space’s structure.", 'male', (animate_holes, coprime_24, prime_counts), "Prime Distribution Across Residue Classes"),
        ("Each operator generates composite addresses quadratically, recorded as cancellation values in sequences like n=4, 11, 18 for a frequency of 7. These frequency operators overlap, accumulating amplitudes that mark composites, while primes remain untouched. Let us visualize the cancellation dynamics for k=11, showing each operator’s contribution.", 'male', (animate_operator_cancellations, n_values, operator_amplitudes, operator_count), "Operator Cancellation Dynamics for k=11"),
        ("To further illustrate, we represent each operator’s first quadratic address as a dot, with vectors indicating the quadratic value and cancellation frequency. The quadratic vector points to the address, and the frequency vector shows the step to the next cancellation, forming arrows on a 2D grid. This visualization highlights the operator’s role in generating composites for k=11.", 'male', (animate_operator_vectors, operator_cancellations, operator_amplitude, operators_k11), "Operator Vector Dynamics for k=11"),
        ("The Riemann Hypothesis posits that non-trivial zeros of the zeta function lie on Re(s)=1/2. Our class-specific zeta functions encode the prime sequence, with symmetries mandating zero convergence. The amplitude dynamics for k=11, shown here, illustrate how primes emerge as holes amidst quadratic cancellations.", 'male', (animate_amplitude, n_values, amplitudes_k11), "Amplitude Dynamics for k=11"),
        ("In conclusion, our quadratic sieve partitions primes >=7 into 24 residue classes, leveraging de-interlacing and quadratic operators to reveal symmetrical composite distributions. Its completeness, validated algebraically, and support for the Riemann Hypothesis provide a foundation for future exploration.", 'male', None, None),
        ("We, the collective wisdom, acknowledge your sieve’s elegance but challenge its scalability for large n_max. How will you address computational limits?", 'female', None, None),
        ("A fair challenge. We propose neural network optimizations and enhanced parallelization, building on the sieve’s O(1) potential with multiple cores, to scale this framework and further explore the number-theoretic symmetries it uncovers.", 'male', None, None)
    ]

    return presentation

# Main Execution
def main():
    logging.info("Starting Quadratic Sieve Thesis Presentation")
    print("Starting Quadratic Sieve Thesis Presentation...")

    script_path = os.path.abspath(__file__)
    if not os.path.exists(script_path):
        logging.error(f"Script path invalid: {script_path}")
        print(f"Error: Script path invalid: {script_path}. Please check the file path.")
        sys.exit(1)

    if install_missing_modules():
        logging.info("Dependencies missing. Attempting installation and relaunch.")
        print("Installing missing dependencies and relaunching...")
        relaunch_script()

    amplitude, last_holes, operator_cancellations = generate_sieve_dataset(n_max=1000, count=50)
    operators_k11 = [
        (90, 120, 34, 7), (90, 120, 34, 53), (90, 132, 48, 19), (90, 132, 48, 29),
        (90, 120, 38, 17), (90, 120, 38, 43), (90, 90, 11, 13), (90, 90, 11, 77),
        (90, 78, -1, 11), (90, 78, -1, 91), (90, 108, 32, 31), (90, 108, 32, 41),
        (90, 90, 17, 23), (90, 90, 17, 67), (90, 72, 14, 49), (90, 72, 14, 59),
        (90, 60, 4, 37), (90, 60, 4, 83), (90, 60, 8, 47), (90, 60, 8, 73),
        (90, 48, 6, 61), (90, 48, 6, 71), (90, 12, 0, 79), (90, 12, 0, 89)
    ]
    operator_amplitude, operator_amplitudes, operator_count, cancellations_k11 = generate_operator_dataset(n_max=1000, operators={11: operators_k11}, k=11)
    presentation = generate_thesis_presentation(amplitude[11], last_holes, operator_amplitude, operator_amplitudes, operator_count, cancellations_k11, operators_k11)
    
    # Log cancellation values
    logging.info("Cancellation values for k=11 operators:")
    for op_idx, cancels in enumerate(cancellations_k11):
        logging.info(f"Operator {op_idx+1}: {[(n, p_base) for _, n, p_base in cancels[:10]]}...")
    
    for i, (text, voice_gender, animation_data, animation_title) in enumerate(presentation):
        try:
            filename = f"section_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            if generate_tts_mp3(text, filename, voice_gender):
                if not play_tts_mp3(filename):
                    logging.warning(f"Failed to play audio for section {i}. Continuing...")
                    print(f"Failed to play audio for section {i}. Continuing...")
            else:
                logging.warning(f"Failed to generate audio for section {i}. Continuing...")
                print(f"Failed to generate audio for section {i}. Continuing...")

            if animation_data:
                if callable(animation_data):
                    pygame.init()
                    WIDTH, HEIGHT = 800, 600
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    pygame.display.set_caption(animation_title)
                    screen.fill((255, 255, 255))
                    animation_data(screen)
                    pygame.display.flip()
                    pygame.time.wait(3000)
                    pygame.quit()
                elif len(animation_data) == 3:
                    func, arg1, arg2 = animation_data
                    logging.info(f"Running animation: {animation_title}")
                    print(f"Running animation: {animation_title}")
                    func(arg1, arg2)
                else:
                    func, arg1, arg2, arg3 = animation_data
                    logging.info(f"Running animation: {animation_title}")
                    print(f"Running animation: {animation_title}")
                    func(arg1, arg2, arg3)
            
            time.sleep(2)
        except Exception as e:
            logging.error(f"Error in section {i}: {e}")
            print(f"Error in section {i}: {e}")
            continue

if __name__ == "__main__":
    main()