def heap_sort(arr):
    
    n = len(arr)
    
    # Build a maxheap
    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        # Check if left child exists and is greater than root
        if left < n and arr[left] > arr[largest]:
            largest = left
        
        # Check if right child exists and is greater than largest so far
        if right < n and arr[right] > arr[largest]:
            largest = right
        
        # Change root if needed
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]  # Swap
            heapify(arr, n, largest)
    
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # Swap
        heapify(arr, i, 0)
