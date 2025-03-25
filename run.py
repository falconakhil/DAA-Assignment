from utils.load_testcases import load_testcases
from utils.run_experiment import run_experiment
from utils.plot_graph import plot_algorithm_comparison,plot_comparative_performance,plot_testcase_comparison,plot_arrangement_comparison,plot_overall_comparison

from algorithms.quick_sort import quick_sort_first_pivot, quick_sort_median_pivot, quick_sort_random_pivot
from algorithms.radix_sort import radix_sort
from algorithms.merge_sort import merge_sort
from algorithms.insert_sort import insertion_sort
from algorithms.heap_sort import heap_sort
from algorithms.bubble_sort import bubble_sort

import platform
from prettytable import PrettyTable
import numpy as np

ITERATIONS_PER_TESTCASE=3
WARMUP_PER_TESTCASE=0

FUNCTIONS=[
    bubble_sort,
    heap_sort,
    insertion_sort,
    merge_sort,
    radix_sort,
    quick_sort_first_pivot,
    quick_sort_median_pivot,
    quick_sort_random_pivot,
]

TESTCASE_FILES = {
    'ascending': 'testcases/ascending.txt',
    'descending': 'testcases/descending.txt',
    'bst': 'testcases/bst.txt',
    'bst_reverse': 'testcases/bst_reverse.txt',
    'random': 'testcases/random.txt',
    'all': 'testcases/complete_dataset.txt',
}


def analyze_all_results(results):
    """
    Print a detailed analysis of the sorting algorithm results focusing on execution times.
    
    Args:
        results: Dictionary mapping each arrangement to its performance results
                Format: {arrangement: {function_name: [list of stats dictionaries]}}
    """
    for arrangement, all_results in results.items():
        print("\n" + "="*80)
        print(f"SORTING ALGORITHM PERFORMANCE ANALYSIS - {arrangement.upper()}".center(80))
        print("="*80)

        # Process the raw results into a more usable format
        processed_all_results = {}
        for func_name, test_cases in all_results.items():
            processed_all_results[func_name] = {}
            for case in test_cases:
                input_size = case['input_size']
                if input_size not in processed_all_results[func_name]:
                    processed_all_results[func_name][input_size] = []
                processed_all_results[func_name][input_size].append((case['avg'], case['min'], case['max']))
        
        # Calculate aggregate statistics for each algorithm and input size
        final_all_results = {}
        for func_name, size_data in processed_all_results.items():
            final_all_results[func_name] = {}
            for size, times_list in size_data.items():
                avg_time = np.mean([t[0] for t in times_list])
                std_dev = np.std([t[0] for t in times_list]) if len(times_list) > 1 else 0
                final_all_results[func_name][size] = (avg_time, std_dev)
        
        # Extract all input sizes
        all_input_sizes = set()
        for func_result in final_all_results.values():
            all_input_sizes.update(func_result.keys())
        input_sizes = sorted(all_input_sizes)
        
        if not input_sizes:
            print("\nNo data available for analysis.")
            continue
        
        # Create a table for performance comparison
        table = PrettyTable()
        table.field_names = ["Algorithm", "Avg Time (s)", "Best Time (s)", "Worst Time (s)"]
        
        # Calculate metrics for each algorithm
        for func_name, size_all_results in final_all_results.items():
            # Calculate average time across all input sizes
            avg_time = np.mean([time for time, _ in size_all_results.values()])
            
            # Find best and worst times
            best_time = float('inf')
            worst_time = 0
            
            for size, (time, _) in size_all_results.items():
                if time < best_time:
                    best_time = time
                if time > worst_time:
                    worst_time = time
            
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
                # f"{best_size}",
                # f"{worst_size}"
            ])
        
        # Sort the table by average time for better readability
        table.sortby = "Avg Time (s)"
        
        print(f"\nPerformance Summary for {arrangement.upper()} arrangement:")
        print(table)
        
        # Find the fastest and slowest algorithms for the largest input size
        if input_sizes:
            largest_input = max(input_sizes)
            print(f"\nPerformance Comparison for Largest Input Size ({largest_input}):")
            
            comparison_table = PrettyTable()
            comparison_table.field_names = ["Algorithm", "Execution Time (s)"]
            
            algorithms_at_largest = []
            for func_name, size_all_results in final_all_results.items():
                if largest_input in size_all_results:
                    algo_name = func_name.replace('_', ' ').title()
                    time = size_all_results[largest_input][0]
                    algorithms_at_largest.append((algo_name, time))
                    comparison_table.add_row([algo_name, f"{time:.6f}"])
            
            # Sort by execution time
            comparison_table.sortby = "Execution Time (s)"
            print(comparison_table)
            
        print("\n" + "="*80 + "\n")



def display_machine_specs(testcases):
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
    print(f"   - Number of different test cases: {len(testcases)}")
    if testcases:
        print(f"   - Input sizes range from {min(len(tc) for tc in testcases)} to {max(len(tc) for tc in testcases)}")

    print(f"\n6. Input Consistency:")
    print(f"   - Same inputs were used for all sorting algorithms")
    print(f"   - Each algorithm was tested on identical data for fair comparison")

    print("\n" + "="*80 + "\n")

if __name__=='__main__':

    testcases={}
    for arrangement,file in TESTCASE_FILES.items():
        testcases[arrangement]=load_testcases(file)

    results={}
    for arrangement,testcase in testcases.items():
        print(f"Running experiment on {arrangement}")
        results[arrangement]=run_experiment(FUNCTIONS, testcase, iterations=ITERATIONS_PER_TESTCASE, warmup=WARMUP_PER_TESTCASE)
        print()

    display_machine_specs(testcases['all'])

    analyze_all_results(results)

    plot_algorithm_comparison(results['all'],save_plots=True)
    plot_comparative_performance(results['all'],save_plots=True)
    plot_testcase_comparison(results,save_plots=True)
    plot_arrangement_comparison(results,save_plots=True)
    plot_overall_comparison(results,save_plots=True)
