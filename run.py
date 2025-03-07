from utils.load_testcases import load_testcases
from utils.run_experiment import run_experiment
from utils.plot_graph import plot_algorithm_comparison_subplots

from algorithms.quick_sort import quick_sort_first_pivot, quick_sort_median_pivot, quick_sort_random_pivot
from algorithms.radix_sort import radix_sort
from algorithms.merge_sort import merge_sort
from algorithms.insert_sort import insertion_sort
from algorithms.heap_sort import heap_sort
from algorithms.bubble_sort import bubble_sort
import platform
import time


TESTCASE_FILE='test_data.txt'
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

plot_algorithm_comparison_subplots(results,save_plots=True)