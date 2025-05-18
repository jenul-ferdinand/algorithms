from typing import List, Tuple
from collections import deque
from helpers import make_full_prefs, make_full_prefs_random
import sys

# ! Less Restrictive Type for List
_List = Tuple # Don't mind the tuple.

# ! Type Aliases for Algorithm
# Satisfaction level for a student
Satisfaction = int

# A class is a list [class_time, min_students, max_students]
ClassTime = int
MinStudents = int
MaxStudents = int
Class = _List[ClassTime, MinStudents, MaxStudents]

# A preference is a list of class times
Preference = List[ClassTime]

# An allocation is a list of class times where each index is a student, 
# indexed in order based on the order of students from time_prefs.
Allocation = List[ClassTime]

# ! Constants
UNASSIGNED = -1 # Allocation value for unassigned students

# ! Algorithm - Crowded Campus
def crowdedCampus(
    num_students: int,
    num_classes: int,
    time_prefs: List[Preference],
    classes: List[Class],
    min_satis: Satisfaction
) -> Allocation:
    time_to_classes: List[ClassTime] = [[] for _ in range(20)]
    class_mins: List[MinStudents] = [c[1] for c in classes]
    class_maxs: List[MaxStudents] = [c[2] for c in classes]
    
    for j, c in enumerate(classes):
        class_time: ClassTime = c[0] # Get the class time
        time_to_classes[class_time].append(j) # key (class_time) to value (student index)

    allocation: Allocation = [UNASSIGNED] * num_students
    class_filled: List[int] = [0] * num_classes
    satisfied = 0

    # * Phase 1: greedily assign as many students as we can into a class
    # where the class time is in their top-5, up to each class's max.
    for student in range(num_students):
        for preference in range(5):
            class_time: ClassTime = time_prefs[student][preference]
            
            for j in time_to_classes[class_time]:
                if class_filled[j] < class_maxs[j]:
                    allocation[student] = j
                    
                    class_filled[j] += 1
                    satisfied += 1
                    break
            
            if allocation[student] is not UNASSIGNED:
                break

    if satisfied < min_satis:
        return None
    
    print('After phase 1 allocation:', allocation)

    # compute how many more each class must still take (min)
    # and how many at most (max)
    rem_mins = [max(class_mins[j] - class_filled[j], 0) for j in range(num_classes)]
    rem_maxs = [class_maxs[j] - class_filled[j] for j in range(num_classes)]

    # collect all students not yet assigned
    remaining = [i for i in range(num_students) if allocation[i] == -1]
    
    print('After phase 1 remaining:', remaining) 
    
    # * Phase 2a: fulfill every class's remaining minimum by popping students
    for j in range(num_classes):
        needed_for_min = max(0, class_mins[j] - class_filled[j])
        while needed_for_min > 0:
            if not remaining:
                return None # Not enough students overall
            
            # Check if class j can even take another student
            if class_filled[j] >= class_maxs[j]:
                return None 
            
            student = remaining.pop()
            allocation[student] = j
            class_filled[j] += 1
            needed_for_min -= 1
            
    for j in range(num_classes):
        if class_filled[j] < class_mins[j]:
            return None
        
    print('After phase 2a allocation:', allocation) # Outptting: [0,1,2]

    # * Phase 2b: assign any leftover students to classes with remaining capacity
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
        
    for j in range(num_classes):
        if not class_mins[j] <= class_filled[j] <= class_maxs[j]:
            print("Logic flaw")
            return None 
        
    print('After phase 2b allocation:', allocation)

    return allocation

if __name__ == '__main__':
    pass

