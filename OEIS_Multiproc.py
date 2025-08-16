
#!/usr/bin/env python
import cmath
import math
import sys
import matplotlib.pyplot as plt
import subprocess
import json

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
    drLD(x, 72, 14, 49, 59, A201804, 11)   # 49,59 @32, 230 8
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

# Function to analyze blocks of 1000 elements and create static and animated plots
def analyze_blocks(lst, block_size=1000):
    """Analyze the list in blocks of block_size elements for marks, zeroes, and signal-to-zero ratio, and generate plots."""
    num_blocks = (len(lst) + block_size - 1) // block_size  # Ceiling division
    block_stats = []
    
    # Process each block
    for i in range(num_blocks):
        start = i * block_size
        end = min((i + 1) * block_size, len(lst))
        block = lst[start:end]
        
        # Calculate sum of marks, count of zeroes, and signal-to-zero ratio
        marks_sum = sum(block)  # Sum of non-zero values (marks)
        zeroes_count = block.count(0)  # Count of zeroes
        signal_to_zero_ratio = zeroes_count / marks_sum if marks_sum != 0 else float('inf')
        
        block_stats.append({
            'block': i + 1,
            'start_index': start,
            'end_index': end - 1,
            'marks_sum': marks_sum,
            'zeroes_count': zeroes_count,
            'signal_to_zero_ratio': signal_to_zero_ratio
        })
    
    # Truncate block_stats to num_blocks - 5 to drop the last 5 blocks
    truncate_blocks = max(1, num_blocks - 5)
    block_stats = block_stats[:truncate_blocks]
    
    # Print block statistics
    print("\nBlock Analysis (per 1000 elements, truncated to first {} blocks):".format(truncate_blocks))
    print("Block | Indices | Sum of Marks | Zeroes Count | Signal-to-Zero Ratio")
    print("-" * 70)
    for stat in block_stats:
        ratio = stat['signal_to_zero_ratio']
        ratio_str = f"{ratio:.4f}" if ratio != float('inf') else "inf"
        print(f"{stat['block']:5d} | {stat['start_index']:7d}-{stat['end_index']:7d} | {stat['marks_sum']:11d} | {stat['zeroes_count']:12d} | {ratio_str:20s}")
    
    # Compare neighboring blocks and accumulate totals (truncate to num_blocks - 6 for pairs)
    print("\nComparison of Neighboring Blocks (truncated to first {} pairs):".format(truncate_blocks - 1))
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
    
    for i in range(min(len(block_stats) - 1, truncate_blocks - 1)):
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
    
    # Signal-to-zero ratio for plotting (truncate to match block_pairs length)
    signal_to_zero_ratios = [stat['signal_to_zero_ratio'] if stat['signal_to_zero_ratio'] != float('inf') else 1000 for stat in block_stats[:len(block_pairs)]]
    block_indices = [str(stat['block']) for stat in block_stats[:len(block_pairs)]]
    
    # Static standalone plots
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
        plt.show()  # Display interactively
        plt.close()
    
    # Create static standalone plots
    create_static_plot(block_pairs, marks_increases, "Marks Increase per Block Pair", "Block Pair", "Marks Increase", "marks_increase_plot.png")
    create_static_plot(block_pairs, marks_percent_changes, "Marks % Change per Block Pair", "Block Pair", "Marks % Change", "marks_percent_change_plot.png")
    create_static_plot(block_pairs, zeroes_changes, "Zeroes Change per Block Pair", "Block Pair", "Zeroes Change", "zeroes_change_plot.png")
    create_static_plot(block_pairs, zeroes_percent_changes, "Zeroes % Change per Block Pair", "Block Pair", "Zeroes % Change", "zeroes_percent_change_plot.png")
    create_static_plot(block_indices, signal_to_zero_ratios, "Signal-to-Zero Ratio per Block", "Block", "Signal-to-Zero Ratio", "signal_to_zero_ratio_plot.png")
    
    # Static combined plot (3x2 subplot to accommodate five metrics)
    fig, axs = plt.subplots(3, 2, figsize=(12, 10))
    axs = axs.flatten()  # Flatten for easier indexing
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
    
    axs[4].plot(block_indices, signal_to_zero_ratios, marker='o')
    axs[4].set_title("Signal-to-Zero Ratio")
    axs[4].set_xlabel("Block")
    axs[4].set_ylabel("Signal-to-Zero Ratio")
    axs[4].tick_params(axis='x', rotation=45)
    axs[4].grid(True)
    
    # Hide the unused subplot
    axs[5].axis('off')
    
    plt.tight_layout()
    plt.savefig("combined_metrics_plot.png")
    plt.show()  # Display interactively
    plt.close()
    
    # Spawn animations in separate processes
    animation_tasks = [
        {
            'type': 'single',
            'x_values': block_pairs,
            'y_values': marks_increases,
            'title': "Marks Increase Animation",
            'xlabel': "Block Pair",
            'ylabel': "Marks Increase",
            'filename': "marks_increase_animation.mp4"
        },
        {
            'type': 'single',
            'x_values': block_pairs,
            'y_values': marks_percent_changes,
            'title': "Marks % Change Animation",
            'xlabel': "Block Pair",
            'ylabel': "Marks % Change",
            'filename': "marks_percent_change_animation.mp4"
        },
        {
            'type': 'single',
            'x_values': block_pairs,
            'y_values': zeroes_changes,
            'title': "Zeroes Change Animation",
            'xlabel': "Block Pair",
            'ylabel': "Zeroes Change",
            'filename': "zeroes_change_animation.mp4"
        },
        {
            'type': 'single',
            'x_values': block_pairs,
            'y_values': zeroes_percent_changes,
            'title': "Zeroes % Change Animation",
            'xlabel': "Block Pair",
            'ylabel': "Zeroes % Change",
            'filename': "zeroes_percent_change_animation.mp4"
        },
        {
            'type': 'single',
            'x_values': block_indices,
            'y_values': signal_to_zero_ratios,
            'title': "Signal-to-Zero Ratio Animation",
            'xlabel': "Block",
            'ylabel': "Signal-to-Zero Ratio",
            'filename': "signal_to_zero_ratio_animation.mp4"
        },
        {
            'type': 'stacked',
            'x_values_list': [block_pairs, block_pairs, block_pairs, block_pairs, block_pairs],
            'y_values_list': [marks_increases, marks_percent_changes, zeroes_changes, zeroes_percent_changes, signal_to_zero_ratios],
            'titles': ["Marks Increase", "Marks % Change", "Zeroes Change", "Zeroes % Change", "Signal-to-Zero Ratio"],
            'ylabels': ["Marks Increase", "Marks % Change", "Zeroes Change", "Zeroes % Change", "Signal-to-Zero Ratio"],
            'filename': "stacked_panels_animation.mp4"
        },
        {
            'type': 'grid',
            'x_values': block_pairs,
            'y_values_list': [marks_increases, marks_percent_changes, zeroes_changes, zeroes_percent_changes, signal_to_zero_ratios],
            'labels': ["Marks Increase", "Marks % Change", "Zeroes Change", "Zeroes % Change", "Signal-to-Zero Ratio"],
            'filename': "single_grid_animation.mp4"
        }
    ]
    
    processes = []
    for task in animation_tasks:
        # Serialize task data to JSON string
        task_json = json.dumps(task)
        # Command to run render_animation.py in a new CMD window
        cmd = f'cmd /c python render_animation.py "{task_json}"'
        # Spawn process
        proc = subprocess.Popen(cmd, shell=True)
        processes.append(proc)
    
    # Wait for all processes to complete
    for proc in processes:
        proc.wait()
    
    return block_stats

# Run the block analysis
analyze_blocks(A201804)

"""
#### Auxiliary Script (`render_animation.py`)
<xaiArtifact artifact_id="1268248c-f8b3-4a16-a5a0-65087bb22465" artifact_version_id="d5c8c599-162b-42ba-b8ce-c3911fe480e3" title="render_animation.py" contentType="text/python">
```python
#!/usr/bin/env python
import sys
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def create_single_animation(x_values, y_values, title, xlabel, ylabel, filename):
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
    plt.show()  # Display interactively, closes process when window is closed
    plt.close()

def create_stacked_panels_animation(x_values_list, y_values_list, titles, ylabels, filename):
    fig, axs = plt.subplots(5, 1, figsize=(10, 15), sharex=True)
    lines = []
    for i, (x_values, y_values, title, ylabel) in enumerate(zip(x_values_list, y_values_list, titles, ylabels)):
        axs[i].set_xlim(-0.5, len(x_values) - 0.5)
        axs[i].set_ylim(min(y_values) - 0.1 * abs(min(y_values)), max(y_values) + 0.1 * abs(max(y_values)))
        axs[i].set_ylabel(ylabel)
        axs[i].set_title(title)
        axs[i].set_xticks(range(len(x_values)))
        axs[i].set_xticklabels(x_values, rotation=45)
        axs[i].grid(True)
        line, = ax.plot([], [], marker='o')
        lines.append(line)
    axs[4].set_xlabel("Block Pair")
    
    def init():
        for line in lines:
            line.set_data([], [])
        return lines
    
    def animate(i):
        for line, y_values in zip(lines, y_values_list):
            line.set_data(range(i + 1), y_values[:i + 1])
        return lines
    
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(x_values_list[0]), interval=200, blit=True)
    anim.save(filename, writer='ffmpeg')
    plt.show()  # Display interactively, closes process when window is closed
    plt.close()

def create_single_grid_animation(x_values, y_values_list, labels, filename):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(-0.5, len(x_values) - 0.5)
    ax.set_ylim(-0.1, 1.1)  # Normalized y-range
    ax.set_xlabel("Block Pair")
    ax.set_ylabel("Normalized Value")
    ax.set_title("All Metrics Animation (Normalized)")
    ax.set_xticks(range(len(x_values)))
    ax.set_xticklabels(x_values, rotation=45)
    ax.grid(True)
    lines = []
    for _ in y_values_list:
        line, = ax.plot([], [], marker='o')
        lines.append(line)
    ax.legend(labels)
    
    # Normalize y-values to [0, 1]
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
    
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(x_values), interval=200, blit=True)
    anim.save(filename, writer='ffmpeg')
    plt.show()  # Display interactively, closes process when window is closed
    plt.close()

if __name__ == "__main__":
    # Read task data from command-line argument
    task_json = sys.argv[1]
    task = json.loads(task_json)
    
    # Dispatch based on animation type
    if task['type'] == 'single':
        create_single_animation(
            task['x_values'],
            task['y_values'],
            task['title'],
            task['xlabel'],
            task['ylabel'],
            task['filename']
        )
    elif task['type'] == 'stacked':
        create_stacked_panels_animation(
            task['x_values_list'],
            task['y_values_list'],
            task['titles'],
            task['ylabels'],
            task['filename']
        )
    elif task['type'] == 'grid':
        create_single_grid_animation(
            task['x_values'],
            task['y_values_list'],
            task['labels'],
            task['filename']
        )
```

### Changes Made
1. **Removed Animation Logic from Main Script**:
   - Moved all animation functions (`create_animated_plot`, `create_stacked_panels_animation`, `create_single_grid_animation`) to `render_animation.py`.
   - Main script now generates data and spawns subprocesses to run animations.

2. **Subprocess for Animations**:
   - Added `subprocess` and `json` imports to the main script.
   - Defined `animation_tasks` as a list of dictionaries containing animation parameters (type, data, titles, etc.).
   - Used `subprocess.Popen` with `cmd /c python render_animation.py` to spawn each animation in a new CMD window on Windows.
   - Serialized task data as JSON strings to pass to the auxiliary script via command-line arguments.
   - Wait for all processes to complete using `proc.wait()`.

3. **Auxiliary Script (`render_animation.py`)**:
   - Created a new script to handle animation rendering based on command-line arguments.
   - Accepts a JSON string containing animation type (`single`, `stacked`, or `grid`) and relevant data.
   - Implements the three animation functions from the previous script, each saving an MP4 and displaying via `plt.show()`.
   - Exits when the user closes the Matplotlib window, closing the CMD window.

4. **Retained Existing Functionality**:
   - Kept all static plot generation, block analysis, signal-to-zero ratio calculations, and truncation logic (dropping last 5 blocks).
   - Outputs remain the same: 6 PNGs and 6 MP4s with identical filenames.

5. **Data Truncation**:
   - Maintained truncation to `num_blocks - 5` blocks and `num_blocks - 6` block pairs to ensure consistent lengths.
   - Ensured `signal_to_zero_ratios` and `block_indices` are truncated to match `block_pairs` length.

6. **Interactive Display**:
   - Static plots in the main script display via `plt.show()`.
   - Animations in the auxiliary script display via `plt.show()`, closing the CMD window when the user closes the Matplotlib window.

### Output Files
After running, you’ll find 12 files in your working directory:
- **Static (6 PNGs)**:
  - `marks_increase_plot.png`
  - `marks_percent_change_plot.png`
  - `zeroes_change_plot.png`
  - `zeroes_percent_change_plot.png`
  - `signal_to_zero_ratio_plot.png`
  - `combined_metrics_plot.png`
- **Animated (6 MP4s)**:
  - `marks_increase_animation.mp4`
  - `marks_percent_change_animation.mp4`
  - `zeroes_change_animation.mp4`
  - `zeroes_percent_change_animation.mp4`
  - `signal_to_zero_ratio_animation.mp4`
  - `stacked_panels_animation.mp4`
  - `single_grid_animation.mp4`

### Notes
- **Parallel Processing**: Each animation runs in a separate process, leveraging multiple CPU cores. The `subprocess` approach ensures isolation, and CMD windows provide visual feedback for each animation.
- **CMD Window Behavior**: On Windows, `cmd /c` ensures the CMD window closes when the Python process exits (after `plt.show()` is closed). On other platforms, adjust the command (e.g., `bash -c` for Linux/Mac).
- **Data Passing**: JSON serialization is used for simplicity. For large datasets, consider pickling if JSON becomes a bottleneck (let me know if needed).
- **Dependencies**: Requires Matplotlib and `ffmpeg`. Ensure `ffmpeg` is installed (e.g., `conda install ffmpeg`, `pip install ffmpeg-python`, or system package manager like `apt install ffmpeg`).
- **Interactive Display**: Animations display in their own Matplotlib windows, and closing them terminates the corresponding CMD window. Static plots display sequentially in the main process.
- **Error Handling**: The truncation logic prevents the previous shape mismatch error. If issues arise, verify `ffmpeg` installation or ensure `num_blocks ≥ 6`.
- **Performance**: Parallel execution reduces total runtime for animations, though each process’s speed depends on CPU and `ffmpeg` performance. Adjust `interval=200` in `render_animation.py` to change animation speed.
- **Alternative Approaches**:
  - **Multiprocessing**: Could use `multiprocessing` instead of `subprocess` to avoid a separate script, but it’s less intuitive for CMD window management and may complicate Matplotlib’s GUI backend.
  - **Separate Scripts**: Fully separate scripts for each animation are possible but less maintainable. The single `render_animation.py` with type-based dispatching is more modular.
  - **Pygame**: Given your past interest in Pygame animations (April 26, 2025), Pygame could be used for real-time visualization, but it lacks Matplotlib’s robust MP4 output. Let me know if you want to explore this.

### Setup Instructions
1. **Save Both Scripts**: Place `OEIS_11.py` and `render_animation.py` in the same directory.
2. **Install Dependencies**:
   - Ensure Python has `matplotlib` and `ffmpeg` installed.
   - Install `ffmpeg` via `conda install ffmpeg`, `pip install ffmpeg-python`, or system package manager (e.g., `apt install ffmpeg` on Linux, `brew install ffmpeg` on Mac, or download from `ffmpeg.org` for Windows).
3. **Run the Main Script**: Execute `python OEIS_11.py` and enter your limit value. It will:
   - Generate static plots, displaying each interactively.
   - Spawn 6 CMD windows, each running an animation process.
   - Save all MP4s and PNGs in the working directory.
   - Wait for all animations to complete before exiting.

### Example Workflow
- Run `OEIS_11.py` with `limit=200`.
- Static plots display one by one (close each to proceed).
- Six CMD windows open, each rendering and displaying an animation.
- Close each animation’s Matplotlib window to save the MP4 and close the CMD window.
- After all processes complete, check the working directory for 6 PNGs and 6 MP4s.

Let me know if you need adjustments, such as different truncation points, faster/slower animations, or exploration of Pygame or multiprocessing alternatives! If you encounter errors (e.g., `ffmpeg` issues or JSON parsing), I can help debug or modify the approach.
"""