import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algorithms_sorting.quick_select import quick_select

def prob9(A: list, B: list, k: int):
    """
    * Union double array k-th order statistic
    
    Time Complexity: O(A + B), where A and B is the length of arrays A and B
    Space Complexity: O(n)
    """
    U = list(set(A).union(B))
    
    return quick_select(U, 0, len(U)-1, k)

if __name__ == '__main__':
    A = [1,2,3]
    B = [9,3,2]
    print(prob9(A, B, 2))