def counting_sort(arr, exp):
    """
    Counting sort implementation used as a subroutine in radix sort.
    Sorts the array based on the digit at position exp.
    
    Args:
        arr: The array to sort
        exp: The current digit position (1s, 10s, 100s, etc.)
    """
    n = len(arr)
    
    # Initialize output array and count array
    output = [0] * n
    count = [0] * 10
    
    # Store count of occurrences of each digit
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1
    
    # Change count[i] so that it contains the position of this digit in output
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    # Build the output array
    # Process array in reverse to maintain stability
    i = n - 1
    while i >= 0:
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
        i -= 1
    
    # Copy the output array to arr
    for i in range(n):
        arr[i] = output[i]

def radix_sort(arr):
    """
    Sort an array using the Radix Sort algorithm.
    
    Args:
        arr: The array to sort (must contain non-negative integers)
    """
    # Find the maximum number to know the number of digits
    if not arr:
        return
        
    max_num = max(arr)
    
    # Do counting sort for every digit
    # exp is 10^i where i is the current digit position
    exp = 1
    while max_num // exp > 0:
        counting_sort(arr, exp)
        exp *= 10

# Example usage
if __name__ == "__main__":
    arr = [170, 45, 75, 90, 802, 24, 2, 66]
    print("Unsorted array:", arr)
    radix_sort(arr)
    print("Sorted array:", arr)