"""
You are given an n x n grid of distinct numbers (represented as a matrix). 

You want to find a local maximum. 

For each number, its neighbuors are the numbers immediately above it, below it,
to its left, and to its right.

Note that while most numbers have 4 neighbours, the ones on the edge of the 
matrix only have 3 neighbours, and the ones in the corners only have 2 
neighbours.

We will consider a number to be a local maximum if all its neighbours are 
smaller than it.

Given the matrix M your algorithm for finding a local maximum should have a
worst case time complexity of O(n)

it should output a single pair of coordinates i and j such that M[i][j] is a 
local maximum. If there are multiple local maxima, your algorithm should output
the coordinates of exactly one local maximum, and this can be any of the 
existing local maxima.
"""

from typing import List, Tuple
import math

INF = math.inf

def find_matrix_local_max(matrix):
    n = len(matrix)
    
    def matrix_local_max(matrix: List[List[int]], top, bottom, left, right):
        size = bottom - top + 1
        if size == 1: return (top, left)
        
        # 1) Middle row and middle col idxs within [top..bottom] x [left..right]
        mid_row = top + (size // 2)
        mid_col = left + (size // 2)
        
        # 2) Find the maximum in the middle row (scan left..right)
        best_col = left
        best_row_val = matrix[mid_row][left]
        for j in range(left+1, right+1):
            if matrix[mid_row][j] > best_row_val:
                best_row_val = matrix[mid_row][j]
                best_col = j
                
        # 3) Find the maximum in the middle column (scan top..bottom)
        best_row = top
        best_col_val = matrix[top][mid_col]
        for i in range(top+1, bottom+1):
            if matrix[i][mid_col] > best_col_val:
                best_col_val = matrix[i][mid_col]
                best_row = i
        
        # 4) Decide which of matrix[mid_row][best_col] and
        #    matrix[best_row][mid_col] is larger
        if best_row_val >= best_col_val:
            r_star, c_star = mid_row, best_col
        else:
            r_star, c_star = best_row, mid_col
            
        # 5) Compare matrix[r_star][c_star] to its 4 neighbours (if they exist)
        curr = matrix[r_star][c_star]
        up = matrix[r_star-1][c_star] if r_star > top else -INF
        down = matrix[r_star+1][c_star] if r_star < bottom else -INF
        leftv = matrix[r_star][c_star-1] if c_star > left else -INF
        rightv = matrix[r_star][c_star+1] if c_star < right else -INF
        
        # If this is at least as big as all neighbours, we've found a local max
        if curr >= up and curr >= down and curr >= leftv and curr >= rightv:
            return (r_star, c_star)
        
        # Otherwise, exactly one neighbour is larger. Recurse into that quadrant
        if up > curr:
            # The local max lies somewhere in the top-half of this block
            return matrix_local_max(matrix, top, r_star-1, left, right)
        if down > curr:
            # The local max lies somewhere in the bottom-half
            return matrix_local_max(matrix, r_star+1, bottom, left, right)
        if leftv > curr:
            # the local max lies somewhere in the left-half
            return matrix_local_max(matrix, top, bottom, left, c_star-1)
        if rightv > curr:
            # The local max lies somewhere in the right-half
            return matrix_local_max(matrix, top, bottom, c_star+1, right)

    return matrix_local_max(matrix, 0, n-1, 0, n-1)
    

if __name__ == '__main__':
    # Example 1 from applied 2 sheet
    matrix = [
        [1,2,27,28,29,30,49],
        [3,4,25,26,31,32,48],
        [5,6,23,24,33,34,47],
        [7,8,21,22,35,36,46],
        [9,10,19,20,37,38,45],
        [11,12,17,18,39,40,44],
        [13,14,15,16,41,42,43]
    ]
    
    res = find_matrix_local_max(matrix)
    exp = {(0,0),(6,0)}
    assert res in exp, f'Expected {exp}, got {res}'
    
    # Example 2 from applied 2 sheet
    matrix = [
        [  1,   3,   6,  10,  15,  21,  28, 164, 201, 203, 206, 210, 215, 221, 228],
        [  2,   5,   9,  14,  20,  27,  34, 163, 202, 205, 209, 214, 220, 227, 234],
        [  4,   8,  13,  19,  26,  33,  39, 162, 204, 208, 213, 219, 226, 233, 239],
        [  7,  12,  18,  25,  32,  38,  43, 161, 207, 212, 218, 225, 232, 238, 290],
        [ 11,  17,  24,  31,  37,  42,  46, 160, 211, 217, 224, 231, 909, 908, 907],
        [ 16,  23,  30,  36,  41,  45,  48, 159, 216, 223, 230, 260, 906, 904, 902],
        [ 22,  29,  35,  40,  44,  47,  49, 158, 222, 229, 235, 340, 305, 903, 901],
        [ 51,  52,  53,  54,  55,  56,  57, 157, 506, 505, 504, 503, 502, 501, 650],
        [101, 102, 127, 128, 129, 130, 149, 156, 601, 302, 327, 328, 629, 630, 649],
        [103, 104, 125, 126, 131, 132, 148, 155, 603, 604, 625, 626, 631, 632, 648],
        [105, 106, 123, 124, 133, 134, 147, 154, 605, 606, 623, 624, 633, 634, 647],
        [107, 108, 121, 122, 135, 136, 146, 153, 607, 608, 621, 622, 635, 636, 646],
        [109, 110, 119, 120, 137, 138, 145, 152, 609, 610, 619, 620, 637, 638, 645],
        [111, 112, 117, 118, 139, 140, 144, 151, 611, 612, 617, 618, 639, 640, 644],
        [113, 114, 115, 116, 141, 142, 143, 150, 613, 614, 615, 616, 641, 642, 643]
    ]
    
    res = find_matrix_local_max(matrix)
    exp = {(0,0),(14,0),(4,0)}
    assert res in exp, f'Expected {exp}, got {res}'
    
    print('All tests passed!')