import matplotlib.pyplot as plt
import math
from collections import defaultdict

def plot_algorithm_comparison_subplots(results, title_prefix="Algorithm Performance: ", log_scale=False, save_plots=False):
    """
    Creates a figure with subplots - one for each algorithm. Each subplot shows the average of
    minimum, average, and maximum runtimes for that algorithm across different input sizes,
    grouping test cases with the same input size.
    
    Args:
        results (dict): Dictionary with function names as keys and lists of runtime statistics as values.
                        Expected format is the output from run_experiment().
        title_prefix (str): Prefix for the main figure title.
        log_scale (bool): Whether to use logarithmic scale for the y-axis.
        save_plots (bool): Whether to save the plot as an image file.
    """
    # Extract function names
    func_names = list(results.keys())
    num_funcs = len(func_names)
    
    # Group test cases by input size and calculate averages for each metric
    grouped_results = {}
    for func_name in func_names:
        grouped_results[func_name] = defaultdict(lambda: {'min_sum': 0, 'avg_sum': 0, 'max_sum': 0, 'count': 0})
        
        for test_case in results[func_name]:
            input_size = test_case['input_size']
            grouped_results[func_name][input_size]['min_sum'] += test_case['min']
            grouped_results[func_name][input_size]['avg_sum'] += test_case['avg']
            grouped_results[func_name][input_size]['max_sum'] += test_case['max']
            grouped_results[func_name][input_size]['count'] += 1
    
    # Calculate averages and prepare data for plotting
    for func_name in func_names:
        for input_size in grouped_results[func_name]:
            count = grouped_results[func_name][input_size]['count']
            grouped_results[func_name][input_size]['min'] = grouped_results[func_name][input_size]['min_sum'] / count
            grouped_results[func_name][input_size]['avg'] = grouped_results[func_name][input_size]['avg_sum'] / count
            grouped_results[func_name][input_size]['max'] = grouped_results[func_name][input_size]['max_sum'] / count
    
    # Extract unique sorted input sizes across all functions
    all_input_sizes = set()
    for func_name in func_names:
        all_input_sizes.update(grouped_results[func_name].keys())
    input_sizes = sorted(list(all_input_sizes))
    
    # Determine subplot layout - try to make it as square as possible
    cols = math.ceil(math.sqrt(num_funcs))
    rows = math.ceil(num_funcs / cols)
    
    # Create figure
    fig, axes = plt.subplots(rows, cols, figsize=(5*cols, 4*rows), squeeze=False)
    fig.suptitle(f"{title_prefix}Algorithm Performance Comparison (Grouped by Input Size)", fontsize=16)
    
    # Metrics to plot with their properties
    metrics = ['min', 'avg', 'max']
    metric_labels = ['Minimum', 'Average', 'Maximum']
    colors = ['green', 'blue', 'red']
    markers = ['o', 's', '^']
    marker_sizes = [60, 50, 70]
    
    # Plot each algorithm in a separate subplot
    for idx, func_name in enumerate(func_names):
        # Get the current subplot
        row, col = idx // cols, idx % cols
        ax = axes[row, col]
        
        # Prepare data for this function
        func_data = grouped_results[func_name]
        
        # Plot min, avg, max for this algorithm
        for i, (metric, label) in enumerate(zip(metrics, metric_labels)):
            x_values = []
            y_values = []
            
            for size in input_sizes:
                if size in func_data:
                    x_values.append(size)
                    y_values.append(func_data[size][metric])
            
            # Use both scatter and line
            ax.scatter(x_values, y_values, 
                    label=label,
                    color=colors[i],
                    marker=markers[i],
                    s=marker_sizes[i],
                    alpha=0.8,
                    edgecolors='black',
                    linewidths=0.8)
            
            # Add connecting lines to help visualize the trend
            ax.plot(x_values, y_values, 
                   color=colors[i],
                   linestyle='-',
                   alpha=0.5)
        
        # Set title and labels for subplot
        ax.set_title(func_name, fontsize=12)
        ax.set_xlabel('Input Size', fontsize=10)
        ax.set_ylabel('Time (seconds)', fontsize=10)
        
        # Set x-axis tick labels only at intervals
        ax.set_xticks(input_sizes)
        if len(input_sizes) > 10:
            interval = len(input_sizes) // 5  # Show about 5 labels
            x_labels = [str(size) if i % interval == 0 else '' for i, size in enumerate(input_sizes)]
            ax.set_xticklabels(x_labels)
        
        # Set logarithmic scale if requested
        if log_scale:
            ax.set_yscale('log')
        
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(fontsize=8)
    
    # Hide empty subplots if any
    for idx in range(num_funcs, rows * cols):
        row, col = idx // cols, idx % cols
        axes[row, col].set_visible(False)
    
    # Adjust spacing between subplots
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Make room for the figure title
    
    # Save if requested
    if save_plots:
        plt.savefig("algorithm_comparison_grouped.png", dpi=300, bbox_inches='tight')
    
    plt.show()
    return fig