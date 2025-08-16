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