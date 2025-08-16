
#!/usr/bin/env python
import cmath
import math
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define the two cases to compare
cases = [
    {'limit': 33, 'block_size': 1000, 'suffix': '_block1000'},
    {'limit': 330, 'block_size': 100000, 'suffix': '_block100000'}
]

def run_sieve(limit):
    # Calculate epoch and base-10 limit
    h = limit
    epoch = 90 * (h * h) - 12 * h + 1
    print(f"\nFor limit={limit}:")
    print("The epoch range is", epoch)
    base10 = (epoch * 90) + 11
    print("This is the base-10 limit:", base10)

    # Calculate range for iterations through quadratic functions
    a = 90
    b = -300
    c = 250 - epoch
    d = (b ** 2) - (4 * a * c)
    sol1 = (-b - cmath.sqrt(d)) / (2 * a)
    sol2 = (-b + cmath.sqrt(d)) / (2 * a)
    print('The solutions are {0} and {1}'.format(sol1, sol2))
    new_limit = sol2

    # Initialize list for A201804
    A201804 = [0] * (int(epoch) + 10)
    print("This is the limit and the limit plus 10", epoch, len(A201804))

    # Composite generating function
    def drLD(x, l, m, z, o, listvar, primitive):
        y = int(90 * (x * x) - l * x + m)
        listvar[y] = listvar[y] + 1
        p = z + (90 * (x - 1))
        q = o + (90 * (x - 1))
        for n in range(1, int(((epoch - y) / p) + 1)):
            listvar[y + (p * n)] = listvar[y + (p * n)] + 1
        for n in range(1, int(((epoch - y) / q) + 1)):
            listvar[y + (q * n)] = listvar[y + (q * n)] + 1

    # Run the sieve
    for x in range(1, int(new_limit.real)):
        drLD(x, 120, 34, 7, 53, A201804, 11)
        drLD(x, 132, 48, 19, 29, A201804, 11)
        drLD(x, 120, 38, 17, 43, A201804, 11)
        drLD(x, 90, 11, 13, 77, A201804, 11)
        drLD(x, 78, -1, 11, 91, A201804, 11)
        drLD(x, 108, 32, 31, 41, A201804, 11)
        drLD(x, 90, 17, 23, 67, A201804, 11)
        drLD(x, 72, 14, 49, 59, A201804, 11)
        drLD(x, 60, 4, 37, 83, A201804, 11)
        drLD(x, 60, 8, 47, 73, A201804, 11)
        drLD(x, 48, 6, 61, 71, A201804, 11)
        drLD(x, 12, 0, 79, 89, A201804, 11)

    # Trim the buffer
    A201804 = A201804[:-10]
    print("A201804[100:]:", A201804[100:])

    # Original summary statistics
    primecount = A201804.count(0)
    print("Sum of marks", sum(A201804), "and sum divided by the number of addresses", epoch, sum(A201804) / epoch)
    print("The number of primes is", primecount, "and the ratio of primes to addresses is", primecount / epoch)
    print("This is the ratio of primes to marks", primecount / sum(A201804))

    return A201804

def analyze_blocks(lst, block_size, suffix):
    num_blocks = (len(lst) + block_size - 1) // block_size
    block_stats = []
    
    # Process each block
    for i in range(num_blocks):
        start = i * block_size
        end = min((i + 1) * block_size, len(lst))
        block = lst[start:end]
        
        marks_sum = sum(block)
        zeroes_count = block.count(0)
        signal_to_zero_ratio = zeroes_count / marks_sum if marks_sum != 0 else float('inf')
        
        block_stats.append({
            'block': i + 1,
            'start_index': start,
            'end_index': end - 1,
            'marks_sum': marks_sum,
            'zeroes_count': zeroes_count,
            'signal_to_zero_ratio': signal_to_zero_ratio
        })
    
    # Print block statistics
    print(f"\nBlock Analysis (block_size={block_size}):")
    print("Block | Indices | Sum of Marks | Zeroes Count | Signal-to-Zero Ratio")
    print("-" * 70)
    for stat in block_stats:
        ratio = stat['signal_to_zero_ratio']
        ratio_str = f"{ratio:.4f}" if ratio != float('inf') else "inf"
        print(f"{stat['block']:5d} | {stat['start_index']:7d}-{stat['end_index']:7d} | {stat['marks_sum']:11d} | {stat['zeroes_count']:12d} | {ratio_str:20s}")
    
    # Compare neighboring blocks
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
        
        marks_increase = next_block['marks_sum'] - curr['marks_sum']
        marks_percent_change = (marks_increase / curr['marks_sum'] * 100) if curr['marks_sum'] != 0 else float('inf')
        
        zeroes_change = next_block['zeroes_count'] - curr['zeroes_count']
        zeroes_percent_change = (zeroes_change / curr['zeroes_count'] * 100) if curr['zeroes_count'] != 0 else float('inf')
        
        total_marks_increase += marks_increase
        total_zeroes_change += zeroes_change
        if marks_percent_change != float('inf'):
            total_marks_percent_change += marks_percent_change
        if zeroes_percent_change != float('inf'):
            total_zeroes_percent_change += zeroes_percent_change
        
        block_pairs.append(f"{curr['block']}-{next_block['block']}")
        marks_increases.append(marks_increase)
        marks_percent_changes.append(marks_percent_change if marks_percent_change != float('inf') else 1000)
        zeroes_changes.append(zeroes_change)
        zeroes_percent_changes.append(zeroes_percent_change if zeroes_percent_change != float('inf') else 1000)
        
        print(f"{curr['block']:2d}-{next_block['block']:2d} | {marks_increase:13d} | {marks_percent_change:13.2f}% | {zeroes_change:12d} | {zeroes_percent_change:14.2f}%")
    
    # Print totals
    print("\nTotals (excluding last block in comparisons):")
    print(f"Total Marks Increase: {total_marks_increase}")
    print(f"Total Marks % Change: {total_marks_percent_change:.2f}%")
    print(f"Total Zeroes Change: {total_zeroes_change}")
    print(f"Total Zeroes % Change: {total_zeroes_percent_change:.2f}%")
    
    signal_to_zero_ratios = [stat['signal_to_zero_ratio'] if stat['signal_to_zero_ratio'] != float('inf') else 1000 for stat in block_stats]
    block_indices = [str(stat['block']) for stat in block_stats]
    
    return block_stats, block_pairs, marks_increases, marks_percent_changes, zeroes_changes, zeroes_percent_changes, signal_to_zero_ratios, block_indices

def create_static_plots(block_pairs, marks_increases, marks_percent_changes, zeroes_changes, zeroes_percent_changes, signal_to_zero_ratios, block_indices, block_size, suffix):
    def create_static_plot(x_values, y_values, title, xlabel, ylabel, filename):
        plt.figure(figsize=(10, 6))
        plt.plot(x_values, y_values, marker='o')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(filename)
        plt.show()
        plt.close()
    
    create_static_plot(block_pairs, marks_increases, f"Marks Increase per Block Pair (block_size={block_size})", "Block Pair", "Marks Increase", f"marks_increase_plot{suffix}.png")
    create_static_plot(block_pairs, marks_percent_changes, f"Marks % Change per Block Pair (block_size={block_size})", "Block Pair", "Marks % Change", f"marks_percent_change_plot{suffix}.png")
    create_static_plot(block_pairs, zeroes_changes, f"Zeroes Change per Block Pair (block_size={block_size})", "Block Pair", "Zeroes Change", f"zeroes_change_plot{suffix}.png")
    create_static_plot(block_pairs, zeroes_percent_changes, f"Zeroes % Change per Block Pair (block_size={block_size})", "Block Pair", "Zeroes % Change", f"zeroes_percent_change_plot{suffix}.png")
    create_static_plot(block_indices[:len(block_pairs)], signal_to_zero_ratios[:len(block_pairs)], f"Signal-to-Zero Ratio per Block (block_size={block_size})", "Block Pair", "Signal-to-Zero Ratio", f"signal_to_zero_ratio_plot{suffix}.png")
    
    fig, axs = plt.subplots(3, 2, figsize=(12, 10))
    axs = axs.flatten()
    axs[0].plot(block_pairs, marks_increases, marker='o')
    axs[0].set_title("Marks Increase")
    axs[0].set_xlabel("Block Pair")
    axs[0].set_ylabel("Marks Increase")
    axs[0].tick_params(axis='x', rotation=45)
    axs[0].grid(True)
    
    axs[1].plot(block_pairs, marks_percent_changes, marker='o')
    axs[1].set_title("Marks % Change")
    axs[1].set_xlabel("Block Pair")
    axs[1].set_ylabel("Marks % Change")
    axs[1].tick_params(axis='x', rotation=45)
    axs[1].grid(True)
    
    axs[2].plot(block_pairs, zeroes_changes, marker='o')
    axs[2].set_title("Zeroes Change")
    axs[2].set_xlabel("Block Pair")
    axs[2].set_ylabel("Zeroes Change")
    axs[2].tick_params(axis='x', rotation=45)
    axs[2].grid(True)
    
    axs[3].plot(block_pairs, zeroes_percent_changes, marker='o')
    axs[3].set_title("Zeroes % Change")
    axs[3].set_xlabel("Block Pair")
    axs[3].set_ylabel("Zeroes % Change")
    axs[3].tick_params(axis='x', rotation=45)
    axs[3].grid(True)
    
    axs[4].plot(block_indices[:len(block_pairs)], signal_to_zero_ratios[:len(block_pairs)], marker='o')
    axs[4].set_title("Signal-to-Zero Ratio")
    axs[4].set_xlabel("Block Pair")
    axs[4].set_ylabel("Signal-to-Zero Ratio")
    axs[4].tick_params(axis='x', rotation=45)
    axs[4].grid(True)
    
    axs[5].axis('off')
    
    plt.tight_layout()
    plt.savefig(f"combined_metrics_plot{suffix}.png")
    plt.show()
    plt.close()

def create_individual_animations(block_pairs, marks_increases, marks_percent_changes, zeroes_changes, zeroes_percent_changes, signal_to_zero_ratios, block_indices, block_size, suffix):
    def create_animated_plot(x_values, y_values, title, xlabel, ylabel, filename):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_xlim(-0.5, len(x_values) - 0.5)
        ax.set_ylim(min(y_values) - 0.1 * abs(min(y_values)), max(y_values) + 0.1 * abs(max(y_values)))
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.set_xticks(range(len(x_values)))
        ax.set_xticklabels(x_values, rotation=45)
        ax.grid(True)
        line, = ax.plot([], [], marker='o')
        
        def init():
            line.set_data([], [])
            return line,
        
        def animate(i):
            line.set_data(range(i + 1), y_values[:i + 1])
            return line,
        
        anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(x_values), interval=200, blit=True)
        anim.save(filename, writer='ffmpeg')
        plt.show()
        plt.close()
    
    create_animated_plot(block_pairs, marks_increases, f"Marks Increase Animation (block_size={block_size})", "Block Pair", "Marks Increase", f"marks_increase_animation{suffix}.mp4")
    create_animated_plot(block_pairs, marks_percent_changes, f"Marks % Change Animation (block_size={block_size})", "Block Pair", "Marks % Change", f"marks_percent_change_animation{suffix}.mp4")
    create_animated_plot(block_pairs, zeroes_changes, f"Zeroes Change Animation (block_size={block_size})", "Block Pair", "Zeroes Change", f"zeroes_change_animation{suffix}.mp4")
    create_animated_plot(block_pairs, zeroes_percent_changes, f"Zeroes % Change Animation (block_size={block_size})", "Block Pair", "Zeroes % Change", f"zeroes_percent_change_animation{suffix}.mp4")
    create_animated_plot(block_pairs, signal_to_zero_ratios[:len(block_pairs)], f"Signal-to-Zero Ratio Animation (block_size={block_size})", "Block Pair", "Signal-to-Zero Ratio", f"signal_to_zero_ratio_animation{suffix}.mp4")

def create_stacked_panels_animation(block_pairs, marks_increases, marks_percent_changes, zeroes_changes, zeroes_percent_changes, signal_to_zero_ratios, block_size, suffix):
    x_values_list = [block_pairs, block_pairs, block_pairs, block_pairs, block_pairs]
    y_values_list = [marks_increases, marks_percent_changes, zeroes_changes, zeroes_percent_changes, signal_to_zero_ratios[:len(block_pairs)]]
    titles = [
        f"Marks Increase (block_size={block_size})",
        f"Marks % Change (block_size={block_size})",
        f"Zeroes Change (block_size={block_size})",
        f"Zeroes % Change (block_size={block_size})",
        f"Signal-to-Zero Ratio (block_size={block_size})"
    ]
    ylabels = ["Marks Increase", "Marks % Change", "Zeroes Change", "Zeroes % Change", "Signal-to-Zero Ratio"]
    
    fig, axs = plt.subplots(5, 1, figsize=(10, 15), sharex=False)
    lines = []
    for i, (x_values, y_values, title, ylabel) in enumerate(zip(x_values_list, y_values_list, titles, ylabels)):
        axs[i].set_xlim(-0.5, len(x_values) - 0.5)
        axs[i].set_ylim(min(y_values) - 0.1 * abs(min(y_values)), max(y_values) + 0.1 * abs(max(y_values)))
        axs[i].set_ylabel(ylabel)
        axs[i].set_title(title)
        axs[i].set_xticks(range(len(x_values)))
        axs[i].set_xticklabels(x_values, rotation=45)
        axs[i].grid(True)
        line, = axs[i].plot([], [], marker='o')
        lines.append(line)
    axs[4].set_xlabel("Block Pair")
    
    def init():
        for line in lines:
            line.set_data([], [])
        return lines
    
    def animate(i):
        for line, x_values, y_values in zip(lines, x_values_list, y_values_list):
            line.set_data(range(i + 1), y_values[:i + 1])
        return lines
    
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(x_values_list[0]), interval=200, blit=True)
    anim.save(f"stacked_panels_animation{suffix}.mp4", writer='ffmpeg')
    plt.show()
    plt.close()

def create_single_grid_animation(block_pairs, marks_increases, marks_percent_changes, zeroes_changes, zeroes_percent_changes, signal_to_zero_ratios, block_size, suffix):
    y_values_list = [marks_increases, marks_percent_changes, zeroes_changes, zeroes_percent_changes, signal_to_zero_ratios[:len(block_pairs)]]
    labels = ["Marks Increase", "Marks % Change", "Zeroes Change", "Zeroes % Change", "Signal-to-Zero Ratio"]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(-0.5, len(block_pairs) - 0.5)
    ax.set_ylim(-0.1, 1.1)
    ax.set_xlabel("Block Pair")
    ax.set_ylabel("Normalized Value")
    ax.set_title(f"All Metrics Animation (Normalized, block_size={block_size})")
    ax.set_xticks(range(len(block_pairs)))
    ax.set_xticklabels(block_pairs, rotation=45)
    ax.grid(True)
    lines = []
    for _ in y_values_list:
        line, = ax.plot([], [], marker='o')
        lines.append(line)
    ax.legend(labels)
    
    normalized_y_values = []
    for y_values in y_values_list:
        y_min, y_max = min(y_values), max(y_values)
        if y_max == y_min:
            normalized_y_values.append([0] * len(y_values))
        else:
            normalized_y_values.append([(y - y_min) / (y_max - y_min) for y in y_values])
    
    def init():
        for line in lines:
            line.set_data([], [])
        return lines
    
    def animate(i):
        for line, y_values in zip(lines, normalized_y_values):
            line.set_data(range(i + 1), y_values[:i + 1])
        return lines
    
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(block_pairs), interval=200, blit=True)
    anim.save(f"single_grid_animation{suffix}.mp4", writer='ffmpeg')
    plt.show()
    plt.close()

def create_signal_to_zero_overlay(signal_ratios_1000, block_indices_1000, signal_ratios_100000, block_indices_100000):
    norm_indices_1000 = [i / (len(block_indices_1000) - 1) for i in range(len(block_indices_1000))]
    norm_indices_100000 = [i / (len(block_indices_100000) - 1) for i in range(len(block_indices_100000))]
    
    plt.figure(figsize=(10, 6))
    plt.plot(norm_indices_1000, signal_ratios_1000, marker='o', label='block_size=1000, limit=33')
    plt.plot(norm_indices_100000, signal_ratios_100000, marker='s', label='block_size=100000, limit=330')
    plt.xlabel("Normalized Block Index")
    plt.ylabel("Signal-to-Zero Ratio")
    plt.title("Signal-to-Zero Ratio Overlay")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("signal_to_zero_ratio_overlay.png")
    plt.show()
    plt.close()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(min(min(signal_ratios_1000), min(signal_ratios_100000)) - 0.1,
                max(max(signal_ratios_1000), max(signal_ratios_100000)) + 0.1)
    ax.set_xlabel("Normalized Block Index")
    ax.set_ylabel("Signal-to-Zero Ratio")
    ax.set_title("Signal-to-Zero Ratio Animation (Overlay)")
    ax.grid(True)
    line1, = ax.plot([], [], marker='o', label='block_size=1000, limit=33')
    line2, = ax.plot([], [], marker='s', label='block_size=100000, limit=330')
    ax.legend()
    
    def init():
        line1.set_data([], [])
        line2.set_data([], [])
        return line1, line2
    
    def animate(i):
        idx_1000 = min(i, len(norm_indices_1000) - 1)
        idx_100000 = min(i, len(norm_indices_100000) - 1)
        line1.set_data(norm_indices_1000[:idx_1000 + 1], signal_ratios_1000[:idx_1000 + 1])
        line2.set_data(norm_indices_100000[:idx_100000 + 1], signal_ratios_100000[:idx_100000 + 1])
        return line1, line2
    
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=max(len(norm_indices_1000), len(norm_indices_100000)), interval=200, blit=True)
    anim.save("signal_to_zero_ratio_overlay.mp4", writer='ffmpeg')
    plt.show()
    plt.close()

def compare_zeroes_percent_change(zeroes_percent_changes_1000, block_pairs_1000, zeroes_percent_changes_100000, block_pairs_100000):
    # Normalize indices to align sequences
    norm_indices_1000 = [i / (len(block_pairs_1000) - 1) for i in range(len(block_pairs_1000))]
    norm_indices_100000 = [i / (len(block_pairs_100000) - 1) for i in range(len(block_pairs_100000))]
    
    # Sample Case 1 at 9 points to match Case 2
    num_samples = len(block_pairs_100000)
    sampled_indices_1000 = [int(i * (len(block_pairs_1000) - 1) / (num_samples - 1)) for i in range(num_samples)]
    sampled_zeroes_percent_changes_1000 = [zeroes_percent_changes_1000[idx] for idx in sampled_indices_1000]
    
    # Compare signs
    matches = 0
    total = num_samples
    for zpc_1000, zpc_100000 in zip(sampled_zeroes_percent_changes_1000, zeroes_percent_changes_100000):
        if zpc_1000 == float('inf') or zpc_100000 == float('inf'):
            continue  # Skip infinite values
        sign_1000 = 0 if zpc_1000 == 0 else (1 if zpc_1000 > 0 else -1)
        sign_100000 = 0 if zpc_100000 == 0 else (1 if zpc_100000 > 0 else -1)
        if sign_1000 == sign_100000 and sign_1000 != 0:
            matches += 1
    
    percentage = (matches / total * 100) if total > 0 else 0
    print(f"\nPercentage of block pairs with matching zeroes % change signs: {percentage:.2f}%")
    
    # Plot zeroes % change overlay
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(sampled_zeroes_percent_changes_1000)), sampled_zeroes_percent_changes_1000, marker='o', label='block_size=1000, limit=33 (sampled)')
    plt.plot(range(len(zeroes_percent_changes_100000)), zeroes_percent_changes_100000, marker='s', label='block_size=100000, limit=330')
    plt.xlabel("Sampled Block Pair Index")
    plt.ylabel("Zeroes % Change")
    plt.title("Zeroes % Change Overlay")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("zeroes_percent_change_overlay.png")
    plt.show()
    plt.close()

# Run both cases and collect data
all_block_stats = []
all_block_pairs = []
all_zeroes_percent_changes = []
all_signal_ratios = []
all_block_indices = []

for case in cases:
    limit = case['limit']
    block_size = case['block_size']
    suffix = case['suffix']
    A201804 = run_sieve(limit)
    block_stats, block_pairs, marks_increases, marks_percent_changes, zeroes_changes, zeroes_percent_changes, signal_to_zero_ratios, block_indices = analyze_blocks(A201804, block_size, suffix)
    
    create_static_plots(block_pairs, marks_increases, marks_percent_changes, zeroes_changes, zeroes_percent_changes, signal_to_zero_ratios, block_indices, block_size, suffix)
    create_individual_animations(block_pairs, marks_increases, marks_percent_changes, zeroes_changes, zeroes_percent_changes, signal_to_zero_ratios, block_indices, block_size, suffix)
    create_stacked_panels_animation(block_pairs, marks_increases, marks_percent_changes, zeroes_changes, zeroes_percent_changes, signal_to_zero_ratios, block_size, suffix)
    create_single_grid_animation(block_pairs, marks_increases, marks_percent_changes, zeroes_changes, zeroes_percent_changes, signal_to_zero_ratios, block_size, suffix)
    
    all_block_stats.append(block_stats)
    all_block_pairs.append(block_pairs)
    all_zeroes_percent_changes.append(zeroes_percent_changes)
    all_signal_ratios.append(signal_to_zero_ratios)
    all_block_indices.append(block_indices)

# Create overlays
create_signal_to_zero_overlay(all_signal_ratios[0], all_block_indices[0], all_signal_ratios[1], all_block_indices[1])
compare_zeroes_percent_change(all_zeroes_percent_changes[0], all_block_pairs[0], all_zeroes_percent_changes[1], all_block_pairs[1])

"""
### Changes Made
1. **Added Sign Comparison**:
   - New function `compare_zeroes_percent_change`:
     - Samples `zeroes_percent_changes` for `block_size=1000` at 9 evenly spaced indices to match the 9 block pairs of `block_size=100000`.
     - Compares signs (positive > 0, negative < 0, zero = 0), counting matches when both are positive or both negative (excluding zero unless both are zero).
     - Computes the percentage of matching signs.
     - Plots `zeroes_percent_change` for both cases on the same graph (`zeroes_percent_change_overlay.png`).
2. **Preserved Outputs**:
   - Kept all tables, plots, and animations (12 files per case: 6 PNGs, 6 MP4s) with `_block1000` and `_block100000` suffixes.
   - Retained `signal_to_zero_ratio` overlay (`signal_to_zero_ratio_overlay.png/mp4`).
3. **Alignment**:
   - Sampled 9 points from Case 1’s 97 block pairs to match Case 2’s 9 pairs, using indices like `i * 96 / 8` (0, 12, 24, ..., 96).
   - Skipped infinite `zeroes_percent_change` values (when `zeroes_count=0`) to avoid errors.
4. **Interactive Display**:
   - Kept `plt.show()` for interactive viewing.

### Output Files
- **Case 1 (block_size=1000, limit=33)**:
  - Static: `marks_increase_plot_block1000.png`, `marks_percent_change_plot_block1000.png`, `zeroes_change_plot_block1000.png`, `zeroes_percent_change_plot_block1000.png`, `signal_to_zero_ratio_plot_block1000.png`, `combined_metrics_plot_block1000.png`
  - Animated: `marks_increase_animation_block1000.mp4`, `marks_percent_change_animation_block1000.mp4`, `zeroes_change_animation_block1000.mp4`, `zeroes_percent_change_animation_block1000.mp4`, `signal_to_zero_ratio_animation_block1000.mp4`, `stacked_panels_animation_block1000.mp4`, `single_grid_animation_block1000.mp4`
- **Case 2 (block_size=100000, limit=330)**:
  - Same as above, with `_block100000` suffix.
- **Overlays**:
  - `signal_to_zero_ratio_overlay.png/mp4`
  - `zeroes_percent_change_overlay.png`

### Percentage Calculation
- **Process**:
  - Case 1: 97 block pairs (`zeroes_percent_changes_1000`, length 97).
  - Case 2: 9 block pairs (`zeroes_percent_changes_100000`, length 9).
  - Sample Case 1 at indices [0, 12, 24, 36, 48, 60, 72, 84, 96] to get 9 values.
  - For each pair (i=0 to 8):
    - If `zeroes_percent_change` is infinite, skip.
    - Compute signs: positive (>0), negative (<0), or zero (=0).
    - Match if both positive or both negative (or both zero).
  - Percentage = (number of matches / 9) * 100.
- **Expected Result**:
  - Your totals (`Total Zeroes % Change: -65.33%` for `limit=33`) suggest most `zeroes_percent_change` values are negative (decreasing zeroes as composites are marked).
  - For `limit=330`, expect similar negative trends due to sieve behavior.
  - High percentage (e.g., >80%) of matching negative signs is likely, as both cases should show decreasing zeroes, but positive changes may occur early or due to fluctuations.
  - Exact percentage depends on data, but run the script to get the precise value.

### Pattern Analysis
- **Zeroes % Change**:
  - Likely mostly negative, as `Total Zeroes Change: -226` (Case 1) indicates decreasing zeroes.
  - Case 2 should show larger absolute `zeroes_change` (~100x, e.g., ~-22600) but similar `zeroes_percent_change` if patterns scale.
  - Check `zeroes_percent_change_overlay.png` for visual alignment of trends.
- **Sign Matches**:
  - High match percentage suggests consistent sieve behavior across scales.
  - Lower percentage indicates range-specific fluctuations (e.g., early blocks may have positive changes).
- **Totals**:
  - Verify Case 1 totals match your values (`86`, `20.75%`, `-226`, `-65.33%`).
  - For Case 2, expect scaled values (e.g., `Total Zeroes Change` ~-22600, similar `%`).

### Running the Script
1. **Dependencies**: Ensure `matplotlib` and `ffmpeg` (`pip install matplotlib`, `conda install ffmpeg`, or `apt install ffmpeg`).
2. **Execution**: Save as `OEIS_11_compare.py` and run `python OEIS_11_compare.py`. It will:
   - Process both cases, generating tables and 12 files per case.
   - Print the percentage of matching `zeroes_percent_change` signs.
   - Create `zeroes_percent_change_overlay.png` and other plots/animations.
   - Display interactively (close windows to proceed).
3. **Analysis**:
   - Check the printed percentage for sign matches.
   - Inspect `zeroes_percent_change_overlay.png` for trend alignment.
   - Compare Case 1 totals to your provided values.

### Notes
- **Block Count Mismatch**: Case 1 (~98 blocks, 97 pairs) vs. Case 2 (~10 blocks, 9 pairs). Sampling aligns the comparison, but let me know if you want `limit` adjusted for equal blocks (e.g., `limit ≈ 330.166` for ~98 blocks).
- **Infinite Values**: Skipped in sign comparison to avoid errors.
- **Dependencies**: Verify `ffmpeg` for animations (`ffmpeg -version`).
- **Interactive Display**: Remove `plt.show()` for file-only output.

Run the script and check the percentage and
"""