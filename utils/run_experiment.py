import time
from tqdm import tqdm


def _calculate_runtime(func, iterations=1, warmup=0, *args, **kwargs):
    """
    Calculates the runtime statistics of a function with warmup and multiple iterations.

    Args:
        func: The function to be timed.
        iterations: Number of iterations to run for gathering statistics (default: 1).
        warmup: Number of warmup runs to perform before timing (default: 0).
        *args: Positional arguments for the function.
        **kwargs: Keyword arguments for the function.

    Returns:
        A dictionary containing the function's return value and runtime statistics in seconds
        (min, max, avg, total, individual runs).
    """
    # Perform warmup runs (results discarded)
    for _ in range(warmup):
        func(*args, **kwargs)
    
    # Perform timed iterations
    times = []
    result = None
    
    for i in range(iterations):
        start_time = time.perf_counter()
        current_result = func(*args, **kwargs)
        end_time = time.perf_counter()
        runtime = end_time - start_time
        times.append(runtime)
        
        # Save the last result (or first if you prefer)
        if i == 0:
            result = current_result
    
    # Calculate statistics
    stats = {
        'result': result,
        'times': times,
        'min': min(times) if times else 0,
        'max': max(times) if times else 0,
        'avg': sum(times) / len(times) if times else 0,
        'total': sum(times) if times else 0,
        'iterations': iterations
    }
    
    return stats


def run_experiment(functions, test_cases, iterations=1, warmup=0):
    """
    Run an experiment on multiple functions using a list of test cases.
    
    Args:
        functions (list or callable): A single function or a list of functions to test.
        test_cases (list): A list of test cases, where each test case is a list of arguments to pass to the function.
        iterations (int): Number of iterations to run for each test case (default: 1).
        warmup (int): Number of warmup runs before timing starts (default: 0).
    
    Returns:
        dict: A dictionary where keys are function names and values are lists of dictionaries
              containing the function's return value, test case length, and detailed runtime statistics for each test case.
    """
    # Convert single function to list for uniform handling
    if callable(functions) and not isinstance(functions, list):
        functions = [functions]
    
    results = {}
    
    for func in functions:
        func_name = func.__name__
        results[func_name] = []
        
        for i, case in enumerate(tqdm(test_cases, desc=f"{func_name}: ")):
            # Add iterations and warmup as the first arguments
            stats = _calculate_runtime(func, iterations, warmup, case.copy())
            
            # Add test case length to the statistics
            # If case is a list, tuple, string or other sequence type
            try:
                stats['input_size'] = len(case)
            except (TypeError, AttributeError):
                # If the case doesn't have a length (like an integer)
                stats['input_size'] = 1
            
            results[func_name].append(stats)
            
    return results