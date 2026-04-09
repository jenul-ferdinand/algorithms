"""
Devise an algorithm that given a sorted sequence of distinct integers
[a_1, a_2, ... , a_n] determines whether there exists an element such that
a_i = i. Your algorithm should run in O(log n) time.

Devise an algorithm that given a sorted sequence of distinct integers a1, a2, ..., an determines
whether there exists an element such that ai = i . Your algorithm should run in O (log(n)) time.

- We know that the elements are sorted and distinct.
So no need to check or sort them

- We need to figure out if element matches it's index.
i.e. if there is [-1, 1, 32], we have 1 matching it's index

- We can use a binary search concept to meet the log(n) time constraint.

- We know that to prove that a_i = i, then a_i - i = 0
So if a_i - i is equal to 0 then we know that the element matches it's index.
"""

def is_there_element_matching_index(arr: list[int]) -> bool:
    """
    Element with matching index?
    
    Checks if there is an element that has the same index as it's value
    using binary search on the difference arr[i] - i.
    
    Time Complexity: O(log n)
    Space Complexity (aux): O(1)
    """
    lo = 0
    hi = len(arr) - 1
    
    while lo <= hi: 
        mid = (lo + hi) // 2 
        diff = arr[mid] - mid
        
        if diff == 0:
            # Found an element where arr[mid] == mid;
            return True
        elif diff < 0:
            # arr[mid] < mid. Since arr[i] - i is non-decreasing,
            # any potential match must be in the right half.
            lo = mid + 1
        elif diff > 0:
            # arr[mid] > mid. Since arr[i] - i is non-decreasing,
            # any potential match must be in the left half.
            hi = mid - 1
    
    # If the loop finishes, no element matching its index was found
    return False



if __name__ == '__main__':
    # Test Case 1: Match exists
    arr1 = [-1, 1, 10, 12]
    result1 = is_there_element_matching_index(arr1)
    print(f'Array: {arr1}')
    print(f'Result: {result1}')
    assert result1 == True, f'Test Case 1 Failed: Expected True, got {result1}'
    print("Test Case 1 Passed!")
    print("-" * 20)

    # Test Case 2: No match exists
    arr2 = [-5, -3, 0, 4, 5] # arr[3] = 4, but index is 3. arr[4] = 5, index is 4. Match at index 3.
    result2 = is_there_element_matching_index(arr2)
    print(f'Array: {arr2}')
    print(f'Result: {result2}')
    assert result2 == True, f'Test Case 2 Failed: Expected True, got {result2}' # Corrected assertion
    print("Test Case 2 Passed!")
    print("-" * 20)

    # Test Case 3: Match at the beginning
    arr3 = [0, 2, 3, 5]
    result3 = is_there_element_matching_index(arr3)
    print(f'Array: {arr3}')
    print(f'Result: {result3}')
    assert result3 == True, f'Test Case 3 Failed: Expected True, got {result3}'
    print("Test Case 3 Passed!")
    print("-" * 20)

    # Test Case 4: Match at the end
    arr4 = [-2, 0, 1, 3]
    result4 = is_there_element_matching_index(arr4)
    print(f'Array: {arr4}')
    print(f'Result: {result4}')
    assert result4 == True, f'Test Case 4 Failed: Expected True, got {result4}'
    print("Test Case 4 Passed!")
    print("-" * 20)

    # Test Case 5: All elements smaller than index
    arr5 = [-5, -4, -3, -2]
    result5 = is_there_element_matching_index(arr5)
    print(f'Array: {arr5}')
    print(f'Result: {result5}')
    assert result5 == False, f'Test Case 5 Failed: Expected False, got {result5}'
    print("Test Case 5 Passed!")
    print("-" * 20)

    # Test Case 6: All elements larger than index
    arr6 = [1, 2, 3, 4]
    result6 = is_there_element_matching_index(arr6)
    print(f'Array: {arr6}')
    print(f'Result: {result6}')
    assert result6 == False, f'Test Case 6 Failed: Expected False, got {result6}'
    print("Test Case 6 Passed!")
    print("-" * 20)

    # Test Case 7: Empty array
    arr7 = []
    result7 = is_there_element_matching_index(arr7)
    print(f'Array: {arr7}')
    print(f'Result: {result7}')
    assert result7 == False, f'Test Case 7 Failed: Expected False, got {result7}'
    print("Test Case 7 Passed!")
    print("-" * 20)