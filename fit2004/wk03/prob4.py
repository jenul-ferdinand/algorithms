import math as Math
import heapq

def remove_dupes1(arr):
    heapq.heapify(arr)
    print(arr)

    val = -1
    i = 0
    while i < len(arr):
        heapq.heappop(arr, val)
        
        if val == peek(arr):
            continue

        heapq.heappush(arr, val)
        i += 1
            
    return arr

def peek(arr):
    if arr == []:
        return None
    else:
        return arr[-1]
    

def remove_dupes2(arr):
    '''
    Removes duplicates from an array by converting to a set and then array.
    
    Time Complexity: O(n^2)
    Space Complexity: O(n)
    '''
    return list(set(arr))
    
        
if __name__ == '__main__':
    remove_dupes1([2,12,12,4,4,4,3,10])
    #print(remove_duplicates([1,2,2,2,3,5,5]))