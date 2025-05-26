from typing import List

__author__ = "Jenul Devon Ferdinand (33119805)"
__email__ = "jfer0043@student.monash.edu"
__date__ = "24/05/2025"


#? =============================================================================|
#? TYPE ALIASES AND CONSTANTS
#? =============================================================================|

# Satisfaction level for a student
Satisfaction = int

# Represents a class which is a list of integers (max 3 elements)
# i.e., [class_time, min_students, max_students]
Class = List[int] 
ClassTime = int
MinStudents = int
MaxStudents = int

# A preference is a list of class times
Preference = List[ClassTime]

# An allocation is a list of class times where each index is a student, 
# indexed in order based on the order of students from time_prefs.
Allocation = List[ClassTime]

# Allocation value for unassigned students
UNASSIGNED = -1 


#! =============================================================================|
#! Crowded Campus Algorithm
#! =============================================================================|

def crowdedCampus(
    num_students: int,
    num_classes: int,
    time_prefs: List[Preference],
    classes: List[Class],
    min_satis: Satisfaction
) -> Allocation | None:
    """
    Function Description:
        Verifies whether a valid allocation of students into proposed classes exists
        that satisfies each class's capacity constraints and ensures at least
        `min_satis` students get put in a class in their top-5 preferred time slots.

    Approach Description:
        Two step greedy algorithm:
        1. Step 1 - Greedy Top-5 Assignment:
           Iterate through each student and attempt to assign them to one of their
           top-5 preferred time slots by selecting the first available class with
           remaining capacity.
           
        2. Step 2 - Fill to Meet Minimums and Dump Remaining:
           a. Collect all unassigned students and fulfill each class's minimum
              occupancy by assigning from this pool.
           b. Assign any leftover students to classes with remaining capacity.

    Args:
        - num_students: Number of students (n).
        - num_classes: Number of proposed classes (m).
        - time_prefs: List of length n; each element is a permutation of 0..19
        indicating a student's ranked time-slot preferences.
        - classes: List of length m; each entry is another list with 3 integers
        [class_time, min_students, max_students].
        - min_satis: Minimum number of students that must be assigned within 
        their top-5 preferences.

    Returns:
        An allocation list of length n where allocation[i] is the class index
        assigned to student i, or None if no valid allocation exists.

    Time Complexity: O(n * m)=O(n^2) worst-case when m is on average O(n).
    Time Complexity Analysis:
        - Constructing time_to_classes: O(m).
        - Step 1 (top-5 greedy): Each of the n students checks up to 5 
        preferences, scanning classes in that slot -> O(n*5*(m/20))=O(n*m).
        - Step 2a/2b remaining dump: linear scans over students and 
        classes -> O(n + m).
        
        Total: O(n * m) -> O(n^2) if m is on average O(n).

    Auxiliary Space: O(n + m) = O(n) worst-case when m = O(n).
    Space Complexity Analysis:
        - `time_to_classes`: O(m + 20).
        - `allocation`, `class_filled`: O(n + m).
        - `remaining` list: O(n).
        - Constant extra variables.
        
    Notes for Marker:
    - This algorithm uses a greedy approach that has two main steps, I 
    went with this approach to more easily to adhere to the time and space 
    constraints of the problem, compared to using a more complex max flow 
    solution.
    
    Thank you!
    """
    # Build mapping from timeslot to class indices
    time_to_classes: List[List[ClassTime]] = [[] for _ in range(20)]
    for j, c in enumerate(classes):
        class_time: ClassTime = c[0] # Get the class time
        time_to_classes[class_time].append(j) # key (class_time) to value (student index)

    # Get class mins and maxs
    class_mins: List[MinStudents] = [c[1] for c in classes]
    class_maxs: List[MaxStudents] = [c[2] for c in classes]
    
    # Allocation state
    allocation: Allocation = [UNASSIGNED] * num_students
    class_filled: List[int] = [0] * num_classes
    satisfied = 0

    # * (1) Greedily assign as many students as we can into a class.
    # * where the class time is in their top-5, up to each class's max.
    for student in range(num_students):
        for pref_rank in range(5):
            class_time: ClassTime = time_prefs[student][pref_rank]
            
            for j in time_to_classes[class_time]:
                if class_filled[j] < class_maxs[j]:
                    allocation[student] = j
                    class_filled[j] += 1
                    satisfied += 1
                    break
            
            if allocation[student] != UNASSIGNED:
                break

    if satisfied < min_satis:
        return None

    # Collect unassigned students
    remaining = [i for i in range(num_students) if allocation[i] == -1]
    
    # * (2a) Fulfill every class's remaining minimum by popping students
    for j in range(num_classes):
        needed_for_min = max(0, class_mins[j] - class_filled[j])
        while needed_for_min > 0:
            if not remaining:
                return None # Not enough students overall
            
            student = remaining.pop()
            
            # Check if class j can even take another student
            if class_filled[j] >= class_maxs[j]:
                return None 
            
            allocation[student] = j
            class_filled[j] += 1
            needed_for_min -= 1

    # * (2b) Assign any leftover students to classes with remaining capacity
    for student in remaining:
        placed = False
        for j in range(num_classes):
            if class_filled[j] < class_maxs[j]: # Check current filled against original max
                allocation[student] = j
                class_filled[j] += 1
                placed = True
                break
        
        if not placed:
            return None # This student couldn't be placed 
    
    return allocation   