from utils.load_testcases import load_testcases
from utils.run_experiment import run_experiment

from algorithms.quick_sort import quick_sort_first_pivot, quick_sort_median_pivot, quick_sort_random_pivot
from algorithms.radix_sort import radix_sort
from algorithms.merge_sort import merge_sort
from algorithms.insert_sort import insertion_sort
from algorithms.heap_sort import heap_sort
from algorithms.bubble_sort import bubble_sort


TESTCASE_FILE='test.txt'
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

print(results)


