def recursive_pow(value, power):
    '''
    Recursive power
    
    Time Complexity: O()
    Space Complexity: O(n)
    '''
    
    if power == 0: return 1
    if power == 1: return value
    
    if power % 2 == 0:
        return recursive_pow(value, power // 2) * recursive_pow(value, power // 2)
    else:
        return recursive_pow(value, power // 2) * recursive_pow(value, power // 2) * value
    
if __name__ == '__main__':
    print(recursive_pow(2, 10))