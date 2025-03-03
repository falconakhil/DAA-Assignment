def merge_sort(arr):
    def _merge(arr, left, mid, right):
        # Merge two subarrays arr[left...mid] and arr[mid+1...right]
        n1 = mid - left + 1
        n2 = right - mid
        
        # Create temporary arrays
        L = arr[left:left+n1]
        R = arr[mid+1:mid+1+n2]
        
        # Merge the temp arrays back into arr[left...right]
        i = j = 0
        k = left
        
        while i < n1 and j < n2:
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        
        # Copy remaining elements of L[]
        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1
        
        # Copy remaining elements of R[]
        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1
    
    def _merge_sort(arr, left, right):
        if left < right:
            mid = (left + right) // 2
            
            # Sort first and second halves
            _merge_sort(arr, left, mid)
            _merge_sort(arr, mid + 1, right)
            _merge(arr, left, mid, right)
    
    # Sorting the input array
    _merge_sort(arr, 0, len(arr) - 1)
