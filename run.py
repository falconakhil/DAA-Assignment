from utils.load_testcases import load_testcases
from utils.run_experiment import run_experiment
from utils.plot_graph import plot_algorithm_comparison_subplots,plot_algorithm_comparison_separate

from algorithms.quick_sort import quick_sort_first_pivot, quick_sort_median_pivot, quick_sort_random_pivot
from algorithms.radix_sort import radix_sort
from algorithms.merge_sort import merge_sort
from algorithms.insert_sort import insertion_sort
from algorithms.heap_sort import heap_sort
from algorithms.bubble_sort import bubble_sort

import platform
from prettytable import PrettyTable
import numpy as np


TESTCASE_FILE='test_data.txt'
ITERATIONS_PER_TESTCASE=3
WARMUP_PER_TESTCASE=0
FUNCTIONS=[
    # bubble_sort,
    # heap_sort,
    # insertion_sort,
    # merge_sort,
    # radix_sort,
    # quick_sort_first_pivot,
    quick_sort_median_pivot,
    quick_sort_random_pivot,
]


def analyze_results(results):
    """
    Print a detailed analysis of the sorting algorithm results focusing on execution times.
    
    Args:
        results: Dictionary mapping each sorting function name to its performance results
                Format from run_experiment: {function_name: [list of stats dictionaries]}
    """
    print("\n" + "="*80)
    print("SORTING ALGORITHM PERFORMANCE ANALYSIS".center(80))
    print("="*80)

    # Process the raw results into a more usable format
    processed_results = {}
    for func_name, test_cases in results.items():
        processed_results[func_name] = {}
        for case in test_cases:
            input_size = case['input_size']
            if input_size not in processed_results[func_name]:
                processed_results[func_name][input_size] = []
            processed_results[func_name][input_size].append((case['avg'], case['min'], case['max']))
    
    # Calculate aggregate statistics for each algorithm and input size
    final_results = {}
    for func_name, size_data in processed_results.items():
        final_results[func_name] = {}
        for size, times_list in size_data.items():
            avg_time = np.mean([t[0] for t in times_list])
            std_dev = np.std([t[0] for t in times_list]) if len(times_list) > 1 else 0
            final_results[func_name][size] = (avg_time, std_dev)
    
    # Extract all input sizes
    all_input_sizes = set()
    for func_result in final_results.values():
        all_input_sizes.update(func_result.keys())
    input_sizes = sorted(all_input_sizes)
    
    if not input_sizes:
        print("\nNo data available for analysis.")
        return
    
    # Create a table for performance comparison
    table = PrettyTable()
    table.field_names = ["Algorithm", "Avg Time (s)", "Best Time (s)", "Worst Time (s)", 
                         "Best Time Input Size", "Worst Time Input Size"]
    
    # Calculate metrics for each algorithm
    for func_name, size_results in final_results.items():
        # Calculate average time across all input sizes
        avg_time = np.mean([time for time, _ in size_results.values()])
        
        # Find best and worst times
        best_time = float('inf')
        worst_time = 0
        best_size = None
        worst_size = None
        
        for size, (time, _) in size_results.items():
            if time < best_time:
                best_time = time
                best_size = size
            if time > worst_time:
                worst_time = time
                worst_size = size
        
        # Handle case where no data is available
        if best_time == float('inf'):
            best_time = 0
            best_size = "N/A"
        if worst_time == 0:
            worst_size = "N/A"
        
        # Extract algorithm name from function
        algo_name = func_name.replace('_', ' ').title()
        
        table.add_row([
            algo_name, 
            f"{avg_time:.6f}", 
            f"{best_time:.6f}", 
            f"{worst_time:.6f}",
            f"{best_size}",
            f"{worst_size}"
        ])
    
    # Sort the table by average time for better readability
    table.sortby = "Avg Time (s)"
    
    print("\nPerformance Summary:")
    print(table)
    
    # Find the fastest and slowest algorithms for the largest input size
    if input_sizes:
        largest_input = max(input_sizes)
        print(f"\nPerformance Comparison for Largest Input Size ({largest_input}):")
        
        comparison_table = PrettyTable()
        comparison_table.field_names = ["Algorithm", "Execution Time (s)"]
        
        algorithms_at_largest = []
        for func_name, size_results in final_results.items():
            if largest_input in size_results:
                algo_name = func_name.replace('_', ' ').title()
                time = size_results[largest_input][0]
                algorithms_at_largest.append((algo_name, time))
                comparison_table.add_row([algo_name, f"{time:.6f}"])
        
        # Sort by execution time
        comparison_table.sortby = "Execution Time (s)"
        print(comparison_table)
        
    print("\n" + "="*80 + "\n")


testcases=load_testcases(TESTCASE_FILE)
results=run_experiment(FUNCTIONS, testcases, iterations=ITERATIONS_PER_TESTCASE, warmup=WARMUP_PER_TESTCASE)

# Print experimental setup information
print("\n" + "="*80)
print("EXPERIMENTAL SETUP INFORMATION".center(80))
print("="*80)

print(f"\n1. Machine Information:")
print(f"   - System: {platform.system()} {platform.release()}")
print(f"   - Processor: {platform.processor()}")
print(f"   - Python Version: {platform.python_version()}")

print(f"\n2. Timing Mechanism:")
print(f"   - Using Python's time.perf_counter() for high-precision timing")
print(f"   - All times reported in seconds")

print(f"\n3. Experiment Repetition:")
print(f"   - Each sorting algorithm was run {ITERATIONS_PER_TESTCASE} times per input")
print(f"   - Warmup iterations per test case: {WARMUP_PER_TESTCASE}")

print(f"\n4. Time Reporting:")
print(f"   - Average execution time across {ITERATIONS_PER_TESTCASE} iterations is reported")
print(f"   - Standard deviation is calculated to measure consistency")

print(f"\n5. Input Selection:")
print(f"   - Test data loaded from file: '{TESTCASE_FILE}'")
print(f"   - Number of different test cases: {len(testcases)}")
if testcases:
    print(f"   - Input sizes range from {min(len(tc) for tc in testcases)} to {max(len(tc) for tc in testcases)}")

print(f"\n6. Input Consistency:")
print(f"   - Same inputs were used for all sorting algorithms")
print(f"   - Each algorithm was tested on identical data for fair comparison")

print("\n" + "="*80 + "\n")

analyze_results(results)
plot_algorithm_comparison_separate(results,save_plots=True)