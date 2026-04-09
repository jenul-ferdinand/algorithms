def insertion_sort(arr: list) -> list:
    '''
    Sorts an array using the insertion sort algorithm
    
    - Insertion sort works by building a sorted array one element at a time.
    - It takes each element and inserts it into its correct position among the
    previously sorted elements.
    
    Time Complexity: O(n^2) - where n is the length of the array.
    Space Complexity: O(1) - sorts in-place
    
    Args:
        arr: The list to be sorted
    
    Returns:
        The sorted list
    '''
    n = len(arr)
    
    # Start from the second element (index 1)
    # The first element is considered already sorted.
    for i in range(1, n):
        # * Store the current element we need to insert in the right position
        target = arr[i]
        
        # Start comparing with the previous elements
        j = i - 1
        
        # * Move elements greater than target one position ahead
        # This creates space to insert the target 
        while j >= 0 and arr[j] > target:
            arr[j + 1] = arr[j] # Shift element to the right
            j -= 1              # Move to the previous element
        
        # * Insert the target element in its correct position
        # j+1 is the correct position because j was decremented one time too many
        # in the while loop (or j is -1 if target belongs at the start)
        arr[j + 1] = target
    
    return arr

def reversed_insertion_sort(arr: list) -> list:
    '''
    Insertion sort but sorts in descending order
    
    Changed arr[j] > target to arr[j] < target
    '''
    n = len(arr)
    
    for i in range(1, n):
        target = arr[i]
        j = i - 1
        
        while j >= 0 and arr[j] < target:
            arr[j + 1] = arr[j]
            j -= 1
            
        arr[j+1] = target
        
    return arr

if __name__ == '__main__':
    test = [7, 12, 9, 11, 3]
    print(insertion_sort(test))
    print(reversed_insertion_sort(test))