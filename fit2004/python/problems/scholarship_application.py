"""
? Name
Scholarship Application

? Description
You have N students, each with a GPA. 

You want to allocate scholarships as follows:
    - Full scholarship: top 20% highest GPAs
    - Partial scholarship: next 30% of GPAs
    - No scholarship: remaining 50%
    
Design an O(N) expected-time algorithm using QuickSelect to find the two GPA
thresholds and partition the students into three groups.
"""

from typing import List, Tuple
import math
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algorithms_sorting.quick_select import quick_select

def scholarship_allocation(
    students: List[Tuple[str, float]]
) -> Tuple[
    List[Tuple[str, float]],
    List[Tuple[str, float]],
    List[Tuple[str, float]]
]:
    N = len(students)
    
    gpas = [gpa for name, gpa in students]
    
    full_count = math.ceil(0.2 * N)
    partial_count = math.ceil(0.3 * N)
    
    thr_full = quick_select(gpas[:], 0, N-1, N - full_count)
    thr_partial = quick_select(gpas[:], 0, N-1, N - (full_count + partial_count))
    
    full = [(n,g) for n,g in students if g >= thr_full]
    partial = [(n,g) for n,g in students if thr_partial <= g < thr_full]
    none = [(n,g) for n,g in students if g < thr_partial]
    
    return full, partial, none
    

if __name__ == '__main__':
    # Test case: 10 students
    students = [
        ('Alice', 3.9), ('Bob', 2.5), ('Charlie', 3.0), ('Diana', 3.7),
        ('Eve', 3.2),   ('Frank', 2.8), ('Grace', 3.5),   ('Hank', 2.9),
        ('Ivy', 3.8),   ('John', 2.6)
    ]
    full, partial, none = scholarship_allocation(students)

    # Expected grouping:
    # Full (20% of 10 = 2 students): Alice, Ivy
    # Partial (30% of 10 = 3 students): Diana, Grace, Eve
    # None (remaining 5): Charlie, Frank, Hank, Bob, John
    full_exp = {'Alice', 'Ivy'}
    partial_exp = {'Grace', 'Eve', 'Diana'}
    none_exp = {'Charlie', 'Frank', 'Hank', 'Bob', 'John'}
    assert set(name for name,_ in full) == full_exp, f'Expected {full_exp}, got {set(full)}'
    assert set(name for name,_ in partial) == partial_exp, f'Expected {partial_exp}, got {set(full)}'
    assert set(name for name,_ in none) == none_exp, f'Expected {none_exp}, got {set(none)}'
    print("All tests passed!")