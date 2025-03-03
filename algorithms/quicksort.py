import random

def _partition(arr, low, high, pivot_index):
    # Move pivot to the end temporarily
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
    pivot = arr[high]
    
    # Index of smaller element
    i = low - 1
    
    for j in range(low, high):
        # If current element is smaller than or equal to the pivot
        if arr[j] <= pivot:
            # Increment index of smaller element
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    # Place pivot in its correct position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def _choose_pivot(arr, low, high, mode):
    if mode == 1:
        # Mode 1: First element as pivot
        return low
    elif mode == 2:
        # Mode 2: Random element as pivot
        return random.randint(low, high)
    elif mode == 3:
        # Mode 3: Median of three
        mid = low + (high - low) // 2
        # Find median of first, middle, and last element
        if arr[low] <= arr[mid] <= arr[high] or arr[high] <= arr[mid] <= arr[low]:
            return mid
        elif arr[mid] <= arr[low] <= arr[high] or arr[high] <= arr[low] <= arr[mid]:
            return low
        else:
            return high
    else:
        # Default: last element as pivot
        return high

def _quick_sort_helper(arr, low, high, mode):
    if low < high:
        # Choose pivot based on mode
        pivot_index = _choose_pivot(arr, low, high, mode)
        
        # Find the partition index
        pi = _partition(arr, low, high, pivot_index)
        
        # Recursively sort elements before and after the partition
        _quick_sort_helper(arr, low, pi - 1, mode)
        _quick_sort_helper(arr, pi + 1, high, mode)

def quick_sort(arr, mode=0):
    """
    Sort an array using the QuickSort algorithm.
    
    Args:
        arr: The array to sort
        mode: Pivot selection strategy:
              0 - last element (default)
              1 - first element
              2 - random element
              3 - median of first, middle, and last elements
    """
    if not arr:
        return
    
    _quick_sort_helper(arr, 0, len(arr) - 1, mode)

# Example usage
if __name__ == "__main__":
    # Test with different pivot selection modes
    test_array = [10, 7, 8, 9, 1, 5]
    
    for mode in range(1, 4):
        arr = test_array.copy()
        print(f"Unsorted array: {arr}")
        quick_sort(arr, mode)
        print(f"Sorted array (mode {mode}): {arr}")
        print()