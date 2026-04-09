def merge_sort(arr: list) -> list:
    n = len(arr)
    
    if n <= 0:
        return []
    if n == 1:
        return arr
    
    mid = n // 2
    
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    merged = merge(left, right)
    
    return merged

def merge(left: list, right: list) -> list:
    merged = []
    i, j = 0, 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        elif left[i] > right[j]:
            merged.append(right[j])
            j += 1
            
    merged.extend(left[i:])
    merged.extend(right[j:])
            
    return merged