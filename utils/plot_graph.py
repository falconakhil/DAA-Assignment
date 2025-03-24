import matplotlib.pyplot as plt
import math
from collections import defaultdict
import os

def _ensure_directory_exists(directory_path):
    """
    Create the directory if it doesn't exist.
    
    Args:
        directory_path (str): Path to the directory to be created
    
    Returns:
        bool: True if directory was created, False if it already existed
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        return True
    return False

def plot_algorithm_comparison(results, title_prefix="Algorithm Performance: ", log_scale=False, save_plots=False,save_dir='outputs/individual_function_plots/'):
    """
    Creates separate figures - one for each algorithm. Each figure shows the 
    minimum, average, and maximum runtimes for that algorithm across different input sizes,
    grouping test cases with the same input size.
    
    Args:
        results (dict): Dictionary with function names as keys and lists of runtime statistics as values.
                        Expected format is the output from run_experiment().
        title_prefix (str): Prefix for the plot titles.
        log_scale (bool): Whether to use logarithmic scale for the y-axis.
        save_plots (bool): Whether to save the plots as image files.
    """
    # Extract function names
    func_names = list(results.keys())
    
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
    
    # Metrics to plot with their properties
    metrics = ['min', 'avg', 'max']
    metric_labels = ['Minimum', 'Average', 'Maximum']
    colors = ['green', 'blue', 'red']
    markers = ['o', 's', '^']
    marker_sizes = [60, 50, 70]
    
    figures = []
    
    # Create a separate plot for each algorithm
    for func_name in func_names:
        # Create a new figure
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        
        # Prepare data for this function
        func_data = grouped_results[func_name]
        
        # Extract and sort input sizes for this function
        input_sizes = sorted(func_data.keys())
        
        # Plot min, avg, max for this algorithm
        for i, (metric, label) in enumerate(zip(metrics, metric_labels)):
            x_values = []
            y_values = []
            
            for size in input_sizes:
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
        
        # Set title and labels for plot
        ax.set_title(f"{title_prefix}{func_name}", fontsize=14)
        ax.set_xlabel('Input Size', fontsize=12)
        ax.set_ylabel('Time (seconds)', fontsize=12)
        
        # Set x-axis tick labels
        ax.set_xticks(input_sizes)
        if len(input_sizes) > 10:
            interval = max(1, len(input_sizes) // 5)  # Show about 5 labels
            x_labels = [str(size) if i % interval == 0 else '' for i, size in enumerate(input_sizes)]
            ax.set_xticklabels(x_labels)
        
        # Set logarithmic scale if requested
        if log_scale:
            ax.set_yscale('log')
        
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(fontsize=10)
        
        plt.tight_layout()
        
        # Save if requested
        if save_plots:
            _ensure_directory_exists(save_dir)
            filename = os.path.join(save_dir,func_name.replace(' ', '_').lower()+'_performance.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Plot saved as '{filename}'")
        
        figures.append(fig)
    
    if not save_plots:
        plt.show()
    
    return figures


def plot_comparative_performance(results, title_prefix="Algorithm Comparison: ", 
                               log_scale=False, save_plots=False, 
                               save_dir='outputs/comparative_plots/'):
    """
    Creates three separate plots comparing all algorithms:
    1. Best times (minimum execution time)
    2. Average times
    3. Worst times (maximum execution time)
    
    Args:
        results (dict): Dictionary with function names as keys and lists of runtime statistics as values.
                        Expected format is the output from run_experiment().
        title_prefix (str): Prefix for the plot titles.
        log_scale (bool): Whether to use logarithmic scale for the y-axis.
        save_plots (bool): Whether to save the plots as image files.
        save_dir (str): Directory to save the plots if save_plots is True.
    
    Returns:
        list: List of the three figure objects created.
    """
    # Extract function names and create nice display names
    func_names = list(results.keys())
    display_names = [name.replace('_', ' ').title() for name in func_names]
    
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
    
    # Calculate averages
    for func_name in func_names:
        for input_size in grouped_results[func_name]:
            count = grouped_results[func_name][input_size]['count']
            grouped_results[func_name][input_size]['min'] = grouped_results[func_name][input_size]['min_sum'] / count
            grouped_results[func_name][input_size]['avg'] = grouped_results[func_name][input_size]['avg_sum'] / count
            grouped_results[func_name][input_size]['max'] = grouped_results[func_name][input_size]['max_sum'] / count
    
    # Get all unique input sizes across all functions
    all_input_sizes = set()
    for func_name in func_names:
        all_input_sizes.update(grouped_results[func_name].keys())
    input_sizes = sorted(all_input_sizes)
    
    # Create a color map for the algorithms
    colors = plt.cm.tab10(range(len(func_names)))
    markers = ['o', 's', '^', 'D', 'x', '*', '+', 'v', '<', '>']
    
    # Create three separate plots for min, avg, and max times
    metrics = ['min', 'avg', 'max']
    metric_titles = ['Best Case', 'Average Case', 'Worst Case']
    figures = []
    
    for metric, metric_title in zip(metrics, metric_titles):
        # Create a new figure
        fig = plt.figure(figsize=(12, 7))
        ax = fig.add_subplot(111)
        
        # Plot each algorithm
        for i, (func_name, display_name) in enumerate(zip(func_names, display_names)):
            x_values = []
            y_values = []
            
            for size in input_sizes:
                # Only add points if the function has data for this input size
                if size in grouped_results[func_name]:
                    x_values.append(size)
                    y_values.append(grouped_results[func_name][size][metric])
            
            # Plot with both scatter points and lines
            marker_idx = i % len(markers)
            ax.scatter(x_values, y_values, 
                     label=display_name,
                     color=colors[i],
                     marker=markers[marker_idx],
                     s=60,
                     alpha=0.7,
                     edgecolors='black',
                     linewidths=0.5)
            
            ax.plot(x_values, y_values, 
                   color=colors[i],
                   linestyle='-',
                   alpha=0.6)
        
        # Set title and labels
        ax.set_title(f"{title_prefix}{metric_title} Performance", fontsize=16)
        ax.set_xlabel('Input Size', fontsize=14)
        ax.set_ylabel('Time (seconds)', fontsize=14)
        
        # Set x-axis tick labels
        ax.set_xticks(input_sizes)
        if len(input_sizes) > 10:
            interval = max(1, len(input_sizes) // 8)  # Show about 8 labels
            x_labels = [str(size) if i % interval == 0 else '' for i, size in enumerate(input_sizes)]
            ax.set_xticklabels(x_labels, rotation=45)
        
        # Set logarithmic scale if requested
        if log_scale:
            ax.set_yscale('log')
        
        ax.grid(True, linestyle='--', alpha=0.6)
        
        # Add legend with better placement
        ax.legend(fontsize=10, loc='upper left', bbox_to_anchor=(1, 1))
        
        plt.tight_layout()
        
        # Save if requested
        if save_plots:
            _ensure_directory_exists(save_dir)
            filename = os.path.join(save_dir, f"{metric}_case_comparison.png")
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Comparative plot saved as '{filename}'")
        
        figures.append(fig)
    
    if not save_plots:
        plt.show()
    
    return figures


def plot_testcase_comparison(results_by_testcase, title_prefix="Performance by Test Case: ", 
                           log_scale=False, save_plots=False, 
                           save_dir='outputs/testcase_plots/'):
    """
    Creates separate plots for each testcase type (ascending, descending, BST, etc.),
    with each plot containing subplots for the different sorting algorithms.
    
    Args:
        results_by_testcase (dict): Dictionary with testcase names as keys and experiment results as values.
                                  Expected format: {'ascending': {func_name: [test_results]}, 'descending': {...}}
        title_prefix (str): Prefix for the plot titles.
        log_scale (bool): Whether to use logarithmic scale for the y-axis.
        save_plots (bool): Whether to save the plots as image files.
        save_dir (str): Directory to save the plots if save_plots is True.
    
    Returns:
        list: List of figure objects created.
    """
    # Colors and markers
    colors = plt.cm.tab10(range(10))
    markers = ['o', 's', '^', 'D', 'x', '*', '+', 'v', '<', '>']
    
    # Metrics to plot with their properties
    metrics = ['avg']  # We'll just use average for these plots to keep them simpler
    metric_titles = ['Average']
    
    figures = []
    
    # For each testcase type
    for testcase_name, testcase_results in results_by_testcase.items():
        # Get all function names for this testcase
        func_names = list(testcase_results.keys())
        display_names = [name.replace('_', ' ').title() for name in func_names]
        
        # Group test cases by input size and calculate averages
        grouped_results = {}
        for func_name in func_names:
            grouped_results[func_name] = defaultdict(lambda: {'avg_sum': 0, 'count': 0})
            
            for test_case in testcase_results[func_name]:
                input_size = test_case['input_size']
                grouped_results[func_name][input_size]['avg_sum'] += test_case['avg']
                grouped_results[func_name][input_size]['count'] += 1
        
        # Calculate averages
        for func_name in func_names:
            for input_size in grouped_results[func_name]:
                count = grouped_results[func_name][input_size]['count']
                grouped_results[func_name][input_size]['avg'] = grouped_results[func_name][input_size]['avg_sum'] / count
        
        # Get all unique input sizes across all functions
        all_input_sizes = set()
        for func_name in func_names:
            all_input_sizes.update(grouped_results[func_name].keys())
        input_sizes = sorted(all_input_sizes)
        
        # Create figure with subplot for each algorithm
        n_funcs = len(func_names)
        n_cols = min(3, n_funcs)  # Max 3 columns
        n_rows = (n_funcs + n_cols - 1) // n_cols  # Ceiling division
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4 * n_rows), sharex=True)
        fig.suptitle(f"{title_prefix}{testcase_name.capitalize()}", fontsize=18)
        
        # Flatten axes for easier indexing if there's only one row
        if n_rows == 1:
            axes = [axes] if n_cols == 1 else axes
        elif n_cols == 1:
            axes = [[ax] for ax in axes]  # Make 2D if only one column
        
        # Plot each algorithm in its own subplot
        for i, func_name in enumerate(func_names):
            row = i // n_cols
            col = i % n_cols
            ax = axes[row][col] if n_rows > 1 else axes[col]
            
            x_values = []
            y_values = []
            
            for size in input_sizes:
                if size in grouped_results[func_name]:
                    x_values.append(size)
                    y_values.append(grouped_results[func_name][size]['avg'])
            
            # Plot with both scatter points and lines
            ax.scatter(x_values, y_values, 
                      color=colors[i % len(colors)], 
                      marker=markers[i % len(markers)],
                      s=60, alpha=0.7, 
                      edgecolors='black', linewidths=0.5)
            
            ax.plot(x_values, y_values, 
                   color=colors[i % len(colors)],
                   linestyle='-', alpha=0.6)
            
            # Set title and labels for subplot
            ax.set_title(display_names[i], fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.6)
            
            # Set y-axis label only for leftmost plots
            if col == 0:
                ax.set_ylabel('Time (seconds)', fontsize=10)
            
            # Set x-axis label only for bottom plots
            if row == n_rows - 1 or (row * n_cols + col) >= len(func_names) - n_cols:
                ax.set_xlabel('Input Size', fontsize=10)
            
            # Set x-axis tick labels
            ax.set_xticks(input_sizes)
            if len(input_sizes) > 10:
                interval = max(1, len(input_sizes) // 5)
                x_labels = [str(size) if i % interval == 0 else '' for i, size in enumerate(input_sizes)]
                ax.set_xticklabels(x_labels, rotation=45)
            
            # Set log scale if requested
            if log_scale:
                ax.set_yscale('log')
        
        # Remove any empty subplots
        for i in range(len(func_names), n_rows * n_cols):
            row = i // n_cols
            col = i % n_cols
            fig.delaxes(axes[row][col] if n_rows > 1 else axes[col])
        
        plt.tight_layout(rect=[0, 0, 1, 0.95])  # Make room for suptitle
        
        # Save if requested
        if save_plots:
            _ensure_directory_exists(save_dir)
            filename = os.path.join(save_dir, f"{testcase_name}_comparison.png")
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Testcase plot saved as '{filename}'")
        
        figures.append(fig)
    
    if not save_plots:
        plt.show()
    
    return figures