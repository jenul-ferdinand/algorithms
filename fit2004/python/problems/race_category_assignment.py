"""
Race Category Assignment

A race organiser wants to assign runners into three categories based on their
finish times (in seconds). Specifically:
    - The slowest 10% of runners are labeled "Novice".
    - The fastest 10% of runners are labeled "Elite".
    - The remaining 80% are labeled "Intermediate".
    
There are N runners and each finish time is a float. You may assume all finish
times are distinct. Design an O(N) expected-time algorithm using QuickSelect
to compute the cut-off times and partition the list into the three categories.

Approach:
- Calculate the order statistics for top 10 and bottom 10 percent
- Use quick select to find the thresholds for top 10 and bottom 10 percent
- Single pass over the times to append to either the novices, intermediates, or
    elites lists.
- Output the three lists in a tuple.
"""

import sys
import os
import math
from typing import List, Tuple

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algorithms_sorting.quick_select import quick_select

def race_category_assignment(
    times: List[float]
) -> Tuple[List[float], List[float], List[float]]:
    """
    Race Category Assignment    
    
    - Calculate the order statistics for top 10 and bottom 10 percent
    - Use quick select to find the thresholds for top 10 and bottom 10 percent
    - Single pass over the times to append to either the novices, intermediates, or
        elites lists.
    - Output the three lists in a tuple.
    
    Time Complexity: O(N)
    Auxiliary Space Complexity: O(N)
    
    Terms:
    - N: The length of the input times list
    """
    N = len(times)
    
    # Order statistics
    SLOWEST_10_IDX = math.ceil(N - (N * 0.1))
    FASTEST_10_IDX = math.ceil(N * 0.1)
    
    # Thresholds using QuickSelect
    THRESHOLD_SLOWEST_10 = quick_select(times[:], 0, N-1, SLOWEST_10_IDX-1)
    THRESHOLD_FASTEST_10 = quick_select(times[:], 0, N-1, FASTEST_10_IDX-1)
    
    # Single pass over times to assign to categories
    novices = []
    elites = []
    intermediates = []
    
    for time in times:
        # Novices
        if time >= THRESHOLD_SLOWEST_10:
            novices.append(time)
            
        # Elites
        elif time <= THRESHOLD_FASTEST_10:
            elites.append(time)
            
        # Intermediates
        elif THRESHOLD_FASTEST_10 <= time <= THRESHOLD_SLOWEST_10:
            intermediates.append(time)
            
    return (novices, intermediates, elites)
    

if __name__ == '__main__':
    # (1) Simple test with 10 runners
    sample_times = [9.5, 8.2, 12.1, 7.8, 10.0, 11.4, 6.3, 13.7, 5.9, 14.2]
    novices, intermediates, elites = race_category_assignment(sample_times)
    
    min_runner = min(sample_times)
    assert novices == [13.7, 14.2], f'Expected novices {[13.7, 14.2]}, got {novices}'
    assert elites == [min_runner], f'Expected elites {[min_runner]}, got {elites}'
    
    out_set = set(sample_times) - {13.7, 14.2, min_runner}
    assert set(intermediates) == out_set, \
        f'Expected intermediates {list(out_set)}, got {intermediates}'
        
    print('All tests passed')