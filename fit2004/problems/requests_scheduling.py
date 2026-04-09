"""
? Past Exam 1: Q20

You are the manager of a super computer and receive a set of requests for 
allocating time frames in that computer.

- The i-th request specifies the desired starting time s_i, and desired
finishing time f_i.

- A subset of requests is compatible if there is no time overlap between any
requests in that subset.

For a set of N requests, give a high-level description of an algorithm with 
time complexity O(N log N) to choose a compatible subset of maximal size 

(i.e., you want to accept as many requests as feasible, but you cannot select
incompatible requests).

? Approach

- Sort the requests by finishing time.

- Start by selecting the first request, then for each subsequent request:
    - Check if its starting time is >= to the last selected requests finishing
    time.
        - If it is >= then, add the current selected request to the subset.
        - If not, ignore.
        
- By the end we'll have a maximal subset of non-overlapping requests.
"""

from typing import List, Tuple

def requests_scheduling(requests: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Schedules Requests for NO OVERLAP
    
    Approach Description:
    - Sort the requests by finish time.
    - Create empty results list to store valid requests.
    - Initialise last_finish as -1 to store the last finish time of the previous
      request.
    - Iterate through each request comparing the start time with the last_finish
      time. If valid, then append to result list and update last_finish to 
      current finish.
    - Return result list for non overlapping requests subset.
    
    Input:
    - requests: List of tuples [(start_time, finish_time), ..., ...]
    
    Output:
    The non overlapping requests.
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Terms:
    - n: The number of requests
    """
    requests = sorted(requests, key = lambda x: x[1])
    
    last_finish = -1
    output = []
    
    for start, finish in requests:
        if start > last_finish:
            output.append((start, finish))
            last_finish = finish
            
    return output

if __name__ == '__main__':
    # (start, finish)
    requests = [
        (1, 4),
        (3, 5),
        (0, 6),
        (5, 7),
        (3, 8),
        (5, 9),
        (6, 10),
        (8, 11),
        (8, 12),
        (2, 13),
        (12, 14)
    ]

    expected = [(1, 4), (5, 7), (8, 11), (12, 14)]
    actual = requests_scheduling(requests)
    print("Output:", actual)
    assert actual == expected, f"Expected {expected}, but got {actual}"