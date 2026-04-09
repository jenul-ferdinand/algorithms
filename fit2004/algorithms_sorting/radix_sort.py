from typing import List

def radix_sort(arr: List[int], base: int = 10) -> List[int]:
    """
    Radix Sort
    
    1. Find the maximum value in `arr` to determine how many digit positions
       (passes) are needed.
    2. For each digit position (exp = 1, base, base^2, ...):
        a. Build a `count` array of length `base` and initialise to zero.
        b. Count how many times each digit (0..base-1) appears at the current
           place value:
           digit = (num // exp) % base
        c. Convert `count` into prefix sums so that `count[d]` = number of 
           elements <= d.
        d. Build a new `output` array (of the same length as `arr`) by 
           iterating `arr` from right to left:
           - Compute the digit for each element at place `exp`.
           - Decrement `count[digit]` by 1 and place `num` into 
             `output[count[digit]]`.
    3. Replace `arr` with `output` and multiply `exp` by `base`. Repeat until
       `exp > max_val`.
        
    
    Time Complexity: O(k(n + b))
    Time Complexity Analysis:
        Let n = len(arr), k = number of digits of max(arr) in base `base`
        b = base.
        Each pass (per digit) does O(n + b) work:
            - O(n) to count digits,
            - O(b) to form prefix sums,
            - O(n) to build the output array.
        There are k passes -> O(k(n + b)) overall.
        
    Aux Space Complexity: O(n + b)
    Aux Space Complexity Analysis:
        Since each digit-level sort creates a `count` array of size b and an
        `output` array of size n.
    
    """
    # (1) Find the max value to determine the digit positions
    max_val = max(arr)
    exp = 1
    output = arr[:]
    
    # (2) For each digit position from least significant to most significant
    while exp <= max_val:
        n = len(output)
        
        # a) Build and zero-init the count array of length `base`
        count = [0] * base
        
        # b) Count occurrences of each digit at place `exp`
        for num in output:
            digit = (num // exp) % base
            count[digit] += 1
            
        # c) Transform count[] into prefix sums:
        #    count[i] will then represent "number of elements <= i"
        for i in range(1, base):
            count[i] += count[i - 1]
            
        # d) Build the new sorted array for this digit pass
        new_output = [0] * n
        for i in range(n - 1, -1, -1):
            num = output[i]
            digit = (num // exp) % base
            count[digit] -= 1
            new_output[count[digit]] = num
            
        # Prepare for next digit
        output = new_output
        exp *= base
    
    return output

if __name__ == "__main__":
    arr = [170, 45, 75, 90, 802, 24, 2, 66]
    res = radix_sort(arr, base=10)
    exp = sorted(arr)
    assert res == exp, f'Expected {exp}, got {res}'
    
    print('All tests passed!')