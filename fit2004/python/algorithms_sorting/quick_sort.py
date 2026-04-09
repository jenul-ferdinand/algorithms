from random import randrange, randint
from typing import List
import time

import sys
sys.setrecursionlimit(10000)

__author__ = 'Jenul Ferdinand'

def quick_sort(arr: list, low: int, high: int, partition_method: str = 'naive', pivot_choice: str = 'random') -> list:
    '''
    QuickSort
    
    Args:
        arr (list): the array to be sorted
        low (int): the lower bound index
        high (int): the upper bound index
        partition_method (str): The method of partitioning ('naive', 'hoares')
        pivot_choice (str): The method of choosing the pivot ('random', 'median-of-3', 'first', 'last')
    
    Return:
        The sorted array
        
    Time Complexity: Θ(n log n)
    Space Complexity: O(log n)
    '''
    # Base Case
    if low >= high:
        return
    
    # Choosing pivot
    match pivot_choice:
        
        case 'random':
            """
            * Random Pivot Selection:
            *    1. Choose a random index between low and high
            *    2. Swap the element at random index with the high element
            *    3. Use the high element as pivot
            
            & Pros:
            &    - Avoids worst-case O(n²) for sorted/nearly-sorted arrays
            &    - Makes algorithm performance less dependent on input patterns
            &    - Simple probabilistic approach with good practical results
            
            ! Cons:
            !    - Introduces non-deterministic behavior
            !    - Not cache-friendly (unpredictable memory access pattern)
            !    - Requires random number generation overhead
            """
            rand_index = randrange(low, high+1)
            arr[rand_index], arr[high] = arr[high], arr[rand_index]
            pivot = arr[high]
            
        case 'median-of-3':
            """
            * Median-of-3 Pivot Selection:
            *    1. Consider first, middle, and last elements
            *    2. Choose the median value among these three
            *    3. Swap median element with high element
            *    4. Use high element as pivot
            
            & Pros:
            &    - Better defense against worst-case inputs than single element selection
            &    - Deterministic (unlike random selection)
            &    - Particularly effective on partially sorted arrays
            
            ! Cons:
            !    - Slightly more complex than simple pivot selection
            !    - Small additional overhead for computing median
            !    - Still vulnerable to specially crafted adversarial inputs
            """
            mid = low + (high - low) // 2
            candidates = [(arr[low], low), (arr[mid], mid), (arr[high], high)]
            candidates.sort(key=lambda x: x[0])
            median_index = candidates[1][1]
            arr[median_index], arr[high] = arr[high], arr[median_index]
            pivot = arr[high]
            
        case 'median-of-median':
            """
            
            """
            pass
              
        case 'first':
            """
            * First Element Pivot:
            *    1. Simply use the element at the low index as pivot
            
            & Pros:
            &    - Extremely simple implementation
            &    - No additional swaps required
            &    - Low overhead
            
            ! Cons:
            !    - Degrades to O(n²) on sorted or reverse-sorted arrays
            !    - Highly sensitive to input data patterns
            !    - Poor performance on common real-world datasets
            """
            pivot = arr[low]
            
        case 'last':
            """
            * Last Element Pivot:
            *    1. Simply use the element at the high index as pivot
            
            & Pros:
            &    - Extremely simple implementation
            &    - Commonly used in textbook implementations
            &    - Compatible with partitioning schemes expecting pivot at high
            
            ! Cons:
            !    - Degrades to O(n²) on sorted arrays
            !    - Highly sensitive to input data patterns
            !    - Poor choice for already sorted or nearly sorted data
            """
            pivot = arr[high]
            
        case 'min':
            """
            * Minimum Element Pivot Selection:
            
            ! Cons:
            !    - O(n) time overhead for finding the minimum element
            !    - Creates highly unbalanced partitions (all elements > pivot)
            !    - Degrades QuickSort to O(n^2) complexity in all cases
            !    - Essentially performs SelectionSort when used in QuickSort
            """
            pivot = min(arr[low:high+1])
            
        case _:
            raise ValueError('Unknown pivot selection method')
    
    # Partitioning
    match partition_method:

        case 'naive':
            """
            * Naive Partitioning Scheme Overview:
            *    1. Choose the rightmost element as pivot
            *    2. Initialise j at the leftmost position
            *    3. For each element from left to right:
            *        - If element <= pivot, swap it with element at j and increment j
            *    4. Place pivot at its final position j by swapping
            *    5. Pivot is now at its sorted position with smaller elements to left and larger to the right
            
            & Pros: 
            &    - Simple implementation with fewer moving parts
            &    - Works well with random or median-of-three pivot selection
            &    - Stable memory usage
                
            ! Cons:
            !    - Less efficient than Hoare's when many duplicate elements exist
            !    - Not in-place for the pivot element (requires a final swap)
            !    - Can be slow on already sorted arrays if using last element as pivot
            """
            j = low
            for i in range(low, high):
                if arr[i] <= pivot:
                    arr[i], arr[j] = arr[j], arr[i]
                    j = j + 1
                    
            arr[high], arr[j] = arr[j], arr[high]
            
            left_high = j - 1
            right_low = j + 1
    
        case 'hoares':
            """
            * Hoare's Partitioning Scheme Overview:
            *    1. Choose the rightmost element as pivot value
            *    2. Initialise two pointers i at left and j at right
            *    3. Move i rightward until finding element >= pivot
            *    4. Move j leftward until finding element <= pivot
            *    5. Swap elements at i and j
            *    6. Continue until pointers cross
            *    7. The partitioning doesn't put pivot in its final sorted position

            & Pros:
            &    - Generally more efficient than naive partitioning
            &    - Makes fewer swaps on average (about N/3 vs N/2 for naive)
            &    - Better performance with many duplicate elements
                
            ! Cons:
            !    - More complex implementation
            !    - Not stable (equal elements may change order)
            !    - Requires careful handling of recursive calls as pivot's final position isn't guaranteed
            """
            i = low
            j = high
            pivot_value = pivot
            
            while True:
                while i < high and arr[i] < pivot_value:
                    i += 1
                
                while j > low and arr[j] > pivot_value:
                    j -= 1
                
                if i >= j:
                    left_high = j
                    right_low = j + 1
                    break
                
                arr[i], arr[j] = arr[j], arr[i]
                
                i += 1
                j -= 1
                    
        case 'dutch-national-flag':
            """
            * Dutch National Flag Partitioning:
            *    1. Partition array into three regions: < pivot, = pivot, > pivot
            *    2. Use three pointers: red (border of < region), mid (current element), blue (border of > region)
            *    3. Compare current element with pivot:
            *        - If less than pivot: Swap with red border, increment red and mid
            *        - If equal to pivot: Just increment mid
            *        - If greater than pivot: Swap with blue border, decrement blue
            *    4. Continue until mid exceeds blue
                
            & Pros:
            &    - Efficiently handles arrays with many duplicate elements
            &    - Solves the "Dutch national flag" problem (three-way partitioning)
            &    - Better performance when duplicate pivot values are common
        
            ! Cons:
            !    - More complex implementation than basic partitioning
            !    - Slightly more overhead for arrays with few duplicates
            !    - Additional pointer tracking increases congnitive complexity
            """
            def partition_dnf(arr, low_idx, high_idx, pivot_val):
                red = low_idx
                mid = low_idx
                blue = high_idx
                while mid <= blue:
                    if arr[mid] < pivot_val:
                        arr[red], arr[mid] = arr[mid], arr[red]
                        red += 1
                        mid += 1
                    elif arr[mid] == pivot_val:
                        mid += 1
                    elif arr[mid] > pivot_val:
                        arr[mid], arr[blue] = arr[blue], arr[mid]
                        blue -= 1
                return red, mid
                
            red, mid = partition_dnf(arr, low, high, pivot)
            
            left_high = red - 1
            right_low = mid
            
        case _:
            raise ValueError('Unknown partitioning method')
            
            
    # Recursive Step (sort left and right partitions)
    quick_sort(arr, low, left_high, partition_method, pivot_choice)
    quick_sort(arr, right_low, high, partition_method, pivot_choice)              
    
    return arr



if __name__ == '__main__':
    # Generate an array of random integers
    def generate_random_array(size=20, min_val=1, max_val=100):
        """Generate an array of random integers within the specified range"""
        return [randint(min_val, max_val) for _ in range(size)]
    
    # Generate arrays of different types for testing
    random_array = generate_random_array(size=100000)
    sorted_array = sorted(random_array.copy())
    reverse_sorted_array = sorted(random_array.copy(), reverse=True)
    duplicates_array = random_array[:10] + random_array[:10]  # Create array with many duplicates
    
    print("Testing various QuickSort configurations with different arrays:\n")
    
    # Define configuration to test
    configurations = [
        ('naive', 'random'),
        ('naive', 'median-of-3'),
        ('naive', 'last'),
        ('hoares', 'random'),
        ('dutch-national-flag', 'median-of-3'),
    ]
    
    # Test with random array
    print(f'Random Array (size={len(random_array)})\n{random_array}\n')
    for partition, pivot in configurations:
        # Create a copy to avoid modifying the original
        test_array = random_array.copy()
        
        # Time the sort
        start = time.perf_counter()
        sorted_arr = quick_sort(test_array, 0, len(test_array)-1, partition, pivot)
        end = time.perf_counter()
        elapsed = end - start
        
        # Verify correct sorting
        is_correct = sorted_arr == sorted(random_array)
        
        print(f'Sorted using {partition.upper()} + {pivot.upper()}')
        print(f'Time taken: {elapsed:.6f} seconds. Correctly sorted: {is_correct}\n')
    
    # Test with array containing many duplicates
    print(f'\nArray with Duplicates (size={len(duplicates_array)})\n{duplicates_array}\n')
    for partition, pivot in configurations:
        if partition == 'dutch-national-flag':  # DNF is optimized for duplicates
            test_array = duplicates_array.copy()
            
            start = time.perf_counter()
            sorted_arr = quick_sort(test_array, 0, len(test_array)-1, partition, pivot)
            end = time.perf_counter()
            elapsed = end - start
            
            is_correct = sorted_arr == sorted(duplicates_array)
            
            print(f'Sorted using {partition.upper()} + {pivot.upper()}')
            print(f'Time taken: {elapsed:.6f} seconds. Correctly sorted: {is_correct}\n')
