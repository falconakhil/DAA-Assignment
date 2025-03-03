import matplotlib.pyplot as plt

def plot_algorithm_scaling(results, title_prefix="Algorithm Scaling: ", log_scale=False, save_plots=False):
    """
    Creates separate scatter plots for each algorithm, each showing how min, avg, and max runtimes 
    scale with input size for that specific algorithm.
    
    Args:
        results (dict): Dictionary with function names as keys and lists of runtime statistics as values.
                        Expected format is the output from run_experiment().
        title_prefix (str): Prefix for plot titles, algorithm name will be appended.
        log_scale (bool): Whether to use logarithmic scale for the y-axis.
        save_plots (bool): Whether to save the plots as image files.
    """
    # Extract function names
    func_names = list(results.keys())
    num_test_cases = len(results[func_names[0]])
    
    # Extract input sizes (assuming they're the same for all functions)
    input_sizes = [results[func_names[0]][k]['input_size'] for k in range(num_test_cases)]
    
    # Metrics to plot
    metrics = ['min', 'avg', 'max']
    metric_labels = ['Minimum', 'Average', 'Maximum']
    
    # Colors for different metrics
    colors = ['green', 'blue', 'red']
    
    # Markers for different metrics
    markers = ['o', 's', '^']
    
    # Marker sizes
    marker_sizes = [80, 60, 100]
    
    figures = []
    
    # Create a separate plot for each algorithm
    for func_name in func_names:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot min, avg, max for this algorithm
        for i, (metric, label) in enumerate(zip(metrics, metric_labels)):
            values = [results[func_name][k][metric] for k in range(num_test_cases)]
            
            # Create scatter plot
            ax.scatter(input_sizes, values, 
                    label=f'{label} Runtime',
                    color=colors[i],
                    marker=markers[i],
                    s=marker_sizes[i],
                    alpha=0.7,
                    edgecolors='black',
                    linewidths=1)
        
        # Set title and labels
        ax.set_title(f"{title_prefix}{func_name}", fontsize=14)
        ax.set_xlabel('Input Size', fontsize=12)
        ax.set_ylabel('Time (seconds)', fontsize=12)
        
        # Set x-axis ticks to show all input sizes
        ax.set_xticks(input_sizes)
        
        # Set logarithmic scale if requested
        if log_scale:
            ax.set_yscale('log')
        
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(fontsize=10)
        
        # Tight layout
        plt.tight_layout()
        
        # Save if requested
        if save_plots:
            safe_name = func_name.replace(" ", "_").lower()
            plt.savefig(f"{safe_name}_scaling.png", dpi=300, bbox_inches='tight')
        
        plt.show()
        figures.append(fig)
    
    return figures