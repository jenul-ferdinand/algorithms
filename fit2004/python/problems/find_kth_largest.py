def find_kth_largest(nums: list[int], k: int) -> int:
    k = len(nums) - k
    
    def quick_select(l, r):
        pivot, p = nums[r], l
        for i in range(l, r):
            if nums[i] <= pivot:
                nums[p], nums[i] = nums[i], nums[p]
                p += 1
        
        nums[p], nums[r] = nums[r], nums[p]
        
        if p > k: return quick_select(l, p - 1)
        if p < k: return quick_select(p + 1, r)
        if p == k: return nums[p]
        
    return quick_select(0, len(nums) - 1)
            

if __name__ == '__main__':
    nums = [3,2,1,5,6,4]
    print(find_kth_largest(nums, 2))
    
    nums = [3,2,3,1,2,4,5,5,6]
    print(find_kth_largest(nums, 4))
    