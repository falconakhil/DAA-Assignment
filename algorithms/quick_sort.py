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

def quick_sort_first_pivot(arr):
    """
    Sort an array using iterative QuickSort with first element as pivot.
    
    Args:
        arr: The array to sort
    """
    if not arr or len(arr) <= 1:
        return
    
    # Create an auxiliary stack
    stack = []
    
    # Push initial values of low and high to stack
    stack.append((0, len(arr) - 1))
    
    # Keep popping from stack while it's not empty
    while stack:
        # Pop low and high
        low, high = stack.pop()
        
        if low < high:
            # Choose the first element as pivot
            pivot_index = low
            
            # Find the partition index
            pi = _partition(arr, low, high, pivot_index)
            
            # Push subarrays to stack
            stack.append((low, pi - 1))   # Elements before partition
            stack.append((pi + 1, high))  # Elements after partition

def quick_sort_random_pivot(arr):
    """
    Sort an array using iterative QuickSort with a random element as pivot.
    
    Args:
        arr: The array to sort
    """
    if not arr or len(arr) <= 1:
        return
    
    # Create an auxiliary stack
    stack = []
    
    # Push initial values of low and high to stack
    stack.append((0, len(arr) - 1))
    
    # Keep popping from stack while it's not empty
    while stack:
        # Pop low and high
        low, high = stack.pop()
        
        if low < high:
            # Choose a random element as pivot
            pivot_index = random.randint(low, high)
            
            # Find the partition index
            pi = _partition(arr, low, high, pivot_index)
            
            # Push subarrays to stack
            stack.append((low, pi - 1))   # Elements before partition
            stack.append((pi + 1, high))  # Elements after partition

def quick_sort_median_pivot(arr):
    """
    Sort an array using iterative QuickSort with median of three elements as pivot.
    
    Args:
        arr: The array to sort
    """
    if not arr or len(arr) <= 1:
        return
    
    def _median_of_three(low, high):
        mid = low + (high - low) // 2
        # Find median of first, middle, and last element
        if arr[low] <= arr[mid] <= arr[high] or arr[high] <= arr[mid] <= arr[low]:
            return mid
        elif arr[mid] <= arr[low] <= arr[high] or arr[high] <= arr[low] <= arr[mid]:
            return low
        else:
            return high
    
    # Create an auxiliary stack
    stack = []
    
    # Push initial values of low and high to stack
    stack.append((0, len(arr) - 1))
    
    # Keep popping from stack while it's not empty
    while stack:
        # Pop low and high
        low, high = stack.pop()
        
        if low < high:
            # Choose the median of three elements as pivot
            pivot_index = _median_of_three(low, high)
            
            # Find the partition index
            pi = _partition(arr, low, high, pivot_index)
            
            # Push subarrays to stack
            stack.append((low, pi - 1))   # Elements before partition
            stack.append((pi + 1, high))  # Elements after partition

# Example usage
if __name__ == "__main__":
    # Test with different pivot selection strategies
    test_array = [10, 7, 8, 9, 1, 5]
    
    arr1 = test_array.copy()
    print(f"Unsorted array: {arr1}")
    quick_sort_first_pivot(arr1)
    print(f"Sorted array (first pivot): {arr1}")
    print()
    
    arr2 = test_array.copy()
    print(f"Unsorted array: {arr2}")
    quick_sort_random_pivot(arr2)
    print(f"Sorted array (random pivot): {arr2}")
    print()
    
    arr3 = test_array.copy()
    print(f"Unsorted array: {arr3}")
    quick_sort_median_pivot(arr3)
    print(f"Sorted array (median pivot): {arr3}")