#!/usr/bin/env python
import cmath
import math
import sys
import matplotlib.pyplot as plt

# Get a value for the limit of the range to be sieved
limit = int(input("limit value here: "))  # Value for the "epoch"
limit = int(limit)  # Convert to int type

# Calculate epoch and base-10 limit
h = limit
epoch = 90 * (h * h) - 12 * h + 1  # Largest element within scope of cancellations
print("The epoch range is", epoch)
limit = epoch
base10 = (limit * 90) + 11
print("This is the base-10 limit:", base10)

# Calculate range for iterations through quadratic functions
a = 90
b = -300
c = 250 - limit
d = (b ** 2) - (4 * a * c)  # Discriminant
sol1 = (-b - cmath.sqrt(d)) / (2 * a)
sol2 = (-b + cmath.sqrt(d)) / (2 * a)
print('The solutions are {0} and {1}'.format(sol1, sol2))
new_limit = sol2

# Initialize list for A201804
A201804 = [0] * (limit + 10)
print("This is the limit and the limit plus 10", limit, len(A201804))
oplist = []  # Tracks number of zeroes per round

# Composite generating function
def drLD(x, l, m, z, o, listvar, primitive):
    """This is a composite generating function"""
    y = 90 * (x * x) - l * x + m
    listvar[y] = listvar[y] + 1
    p = z + (90 * (x - 1))
    q = o + (90 * (x - 1))
    for n in range(1, int(((limit - y) / p) + 1)):
        listvar[y + (p * n)] = listvar[y + (p * n)] + 1
    for n in range(1, int(((limit - y) / q) + 1)):
        listvar[y + (q * n)] = listvar[y + (q * n)] + 1

# Run the sieve
for x in range(1, int(new_limit.real)):
    drLD(x, 120, 34, 7, 53, A201804, 11)   # 7,53  @4,  154 1
    drLD(x, 132, 48, 19, 29, A201804, 11)  # 19,29 @6,  144 2
    drLD(x, 120, 38, 17, 43, A201804, 11)  # 17,43 @8,  158 3
    drLD(x, 90, 11, 13, 77, A201804, 11)   # 13,77 @11, 191 4
    drLD(x, 78, -1, 11, 91, A201804, 11)   # 11,91 @11, 203 5
    drLD(x, 108, 32, 31, 41, A201804, 11)  # 31,41 @14, 176 6
    drLD(x, 90, 17, 23, 67, A201804, 11)   # 23,67 @17, 197 7
    drLD(x, 72, 14, 49, 59, A201804, 11)   # 49,59 @32, 230issante
    drLD(x, 60, 4, 37, 83, A201804, 11)    # 37,83 @34, 244 9
    drLD(x, 60, 8, 47, 73, A201804, 11)    # 47,73 @38, 248 10
    drLD(x, 48, 6, 61, 71, A201804, 11)    # 61,71 @48, 270 11
    drLD(x, 12, 0, 79, 89, A201804, 11)    # 79,89 @78, 336 12

# Trim the buffer
A201804 = A201804[:-10]
print(A201804[100:])

# Original summary statistics
primecount = A201804.count(0)
print("Sum of marks", sum(A201804), "and sum divided by the number of addresses", limit, sum(A201804) / limit)
print("The number of primes is", primecount, "and the ratio of primes to addresses is", primecount / limit)
print("This is the ratio of primes to marks", primecount / sum(A201804))

# Function to analyze blocks of 1000 elements
def analyze_blocks(lst, block_size=10000):
    """Analyze the list in blocks of block_size elements for marks and zeroes."""
    num_blocks = (len(lst) + block_size - 1) // block_size  # Ceiling division
    block_stats = []
    
    # Process each block
    for i in range(num_blocks):
        start = i * block_size
        end = min((i + 1) * block_size, len(lst))
        block = lst[start:end]
        
        # Calculate sum of marks and count of zeroes
        marks_sum = sum(block)  # Sum of non-zero values (marks)
        zeroes_count = block.count(0)  # Count of zeroes
        
        block_stats.append({
            'block': i + 1,
            'start_index': start,
            'end_index': end - 1,
            'marks_sum': marks_sum,
            'zeroes_count': zeroes_count
        })
    
    # Print block statistics
    print("\nBlock Analysis (per 1000 elements):")
    print("Block | Indices | Sum of Marks | Zeroes Count")
    print("-" * 50)
    for stat in block_stats:
        print(f"{stat['block']:5d} | {stat['start_index']:7d}-{stat['end_index']:7d} | {stat['marks_sum']:11d} | {stat['zeroes_count']:12d}")
    
    # Compare neighboring blocks and accumulate totals
    print("\nComparison of Neighboring Blocks:")
    print("Block Pair | Marks Increase | Marks % Change | Zeroes Change | Zeroes % Change")
    print("-" * 70)
    total_marks_increase = 0
    total_marks_percent_change = 0
    total_zeroes_change = 0
    total_zeroes_percent_change = 0
    block_pairs = []
    marks_increases = []
    marks_percent_changes = []
    zeroes_changes = []
    zeroes_percent_changes = []
    
    for i in range(len(block_stats) - 1):
        curr = block_stats[i]
        next_block = block_stats[i + 1]
        
        # Marks increase
        marks_increase = next_block['marks_sum'] - curr['marks_sum']
        marks_percent_change = (marks_increase / curr['marks_sum'] * 100) if curr['marks_sum'] != 0 else float('inf')
        
        # Zeroes change
        zeroes_change = next_block['zeroes_count'] - curr['zeroes_count']
        zeroes_percent_change = (zeroes_change / curr['zeroes_count'] * 100) if curr['zeroes_count'] != 0 else float('inf')
        
        # Accumulate totals
        total_marks_increase += marks_increase
        total_zeroes_change += zeroes_change
        if marks_percent_change != float('inf'):
            total_marks_percent_change += marks_percent_change
        if zeroes_percent_change != float('inf'):
            total_zeroes_percent_change += zeroes_percent_change
        
        # Store for plotting
        block_pairs.append(f"{curr['block']}-{next_block['block']}")
        marks_increases.append(marks_increase)
        marks_percent_changes.append(marks_percent_change if marks_percent_change != float('inf') else 1000)
        zeroes_changes.append(zeroes_change)
        zeroes_percent_changes.append(zeroes_percent_change if zeroes_percent_change != float('inf') else 1000)
        
        print(f"{curr['block']:2d}-{next_block['block']:2d} | {marks_increase:13d} | {marks_percent_change:13.2f}% | {zeroes_change:12d} | {zeroes_percent_change:14.2f}%")
    
    # Print totals (excluding last block in comparisons)
    print("\nTotals (excluding last block in comparisons):")
    print(f"Total Marks Increase: {total_marks_increase}")
    print(f"Total Marks % Change: {total_marks_percent_change:.2f}%")
    print(f"Total Zeroes Change: {total_zeroes_change}")
    print(f"Total Zeroes % Change: {total_zeroes_percent_change:.2f}%")
    
    # Plotting individual plots
    # Plot 1: Marks Increase
    plt.figure(figsize=(10, 6))
    plt.bar(block_pairs, marks_increases)
    plt.xlabel('Block Pair')
    plt.ylabel('Marks Increase')
    plt.title('Marks Increase per Block Pair')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('marks_increase_plot.png')
    plt.close()
    
    # Plot 2: Marks % Change
    plt.figure(figsize=(10, 6))
    plt.bar(block_pairs, marks_percent_changes)
    plt.xlabel('Block Pair')
    plt.ylabel('Marks % Change')
    plt.title('Marks % Change per Block Pair')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('marks_percent_change_plot.png')
    plt.close()
    
    # Plot 3: Zeroes Change
    plt.figure(figsize=(10, 6))
    plt.bar(block_pairs, zeroes_changes)
    plt.xlabel('Block Pair')
    plt.ylabel('Zeroes Change')
    plt.title('Zeroes Change per Block Pair')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('zeroes_change_plot.png')
    plt.close()
    
    # Plot 4: Zeroes % Change
    plt.figure(figsize=(10, 6))
    plt.bar(block_pairs, zeroes_percent_changes)
    plt.xlabel('Block Pair')
    plt.ylabel('Zeroes % Change')
    plt.title('Zeroes % Change per Block Pair')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('zeroes_percent_change_plot.png')
    plt.close()
    
    # Fused plot: 2x2 subplot grid
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    
    # Subplot 1: Marks Increase
    axs[0, 0].bar(block_pairs, marks_increases)
    axs[0, 0].set_title('Marks Increase')
    axs[0, 0].set_xlabel('Block Pair')
    axs[0, 0].set_ylabel('Marks Increase')
    axs[0, 0].tick_params(axis='x', rotation=45)
    
    # Subplot 2: Marks % Change
    axs[0, 1].bar(block_pairs, marks_percent_changes)
    axs[0, 1].set_title('Marks % Change')
    axs[0, 1].set_xlabel('Block Pair')
    axs[0, 1].set_ylabel('Marks % Change')
    axs[0, 1].tick_params(axis='x', rotation=45)
    
    # Subplot 3: Zeroes Change
    axs[1, 0].bar(block_pairs, zeroes_changes)
    axs[1, 0].set_title('Zeroes Change')
    axs[1, 0].set_xlabel('Block Pair')
    axs[1, 0].set_ylabel('Zeroes Change')
    axs[1, 0].tick_params(axis='x', rotation=45)
    
    # Subplot 4: Zeroes % Change
    axs[1, 1].bar(block_pairs, zeroes_percent_changes)
    axs[1, 1].set_title('Zeroes % Change')
    axs[1, 1].set_xlabel('Block Pair')
    axs[1, 1].set_ylabel('Zeroes % Change')
    axs[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('combined_metrics_plot.png')
    plt.close()
    
    return block_stats

# Run the block analysis
analyze_blocks(A201804)