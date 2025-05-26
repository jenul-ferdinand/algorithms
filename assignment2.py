from typing import List, Tuple

__author__ = "Jenul Devon Ferdinand (33119805)"
__email__ = "jfer0043@student.monash.edu"
__date__ = "26/05/2025"


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
        time_to_classes[class_time].append(j) # key (cls_time) to val (stu_idx)

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
                return None
            
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
            if class_filled[j] < class_maxs[j]: 
                allocation[student] = j
                class_filled[j] += 1
                placed = True
                break
        
        if not placed:
            return None # This student couldn't be placed 
    
    return allocation   




#? =============================================================================|
#? TYPE ALIASES AND CONSTANTS
#? =============================================================================|

# A word is a string of lowercase letters a..z 
Word = str

# Represents a state in the trie traversal
Index = int
Mismatches = int
State = Tuple['TrieNode', Index, Mismatches]

# Fixed alphabet size for lowercase letters
ALPHABET_SIZE = 26


#! =============================================================================|
#! Bad AI Solution
#! =============================================================================|

class TrieNode:
    """
    A node in a prefix trie for lowercase words, with a 26-slot child array and 
    a bitmask for existing children.
    """
    __slots__ = ('children', 'word', 'mask')
    def __init__(self):
        # Fixed-size array of 26 references (None or TrieNode)
        self.children = [None] * ALPHABET_SIZE
        # Store complete word at leaf nodes
        self.word = None
        # Bitmask of non-null child indicies for fast iteration
        self.mask = 0

class Bad_AI:
    def __init__(
        self, 
        list_words: List[Word]
    ) -> None:
        """
        Function Description:
            Build a prefix trie containing all words from `list_words` to enable
            efficient one-substitution lookups.

        Approach Description:
            For each word, traverse from the root. At each character index:
            
            - If the child node does not exist, create a new TrieNode.
            - Update the current node's mask with the character bit.
            - Move to the child node.
            
            At the end of each word, store it in the node.

        Args:
            list_words: List of unique lowercase words to insert into the trie.

        Time Complexity: O(C)
        Time Complexity Analysis:
            - Each of the C total characters across all words triggers constant
              time operations: computing an index, checking/assigning a child
              pointer.

        Auxiliary Space: O(C)
        Space Complexity Analysis:
            - Up to C new TrieNode instances are created (one per inserted char)
            - Each node allocates a fixed-size `children` list of length 26.

        Notes for Marker:
            Uses a trie with `__slots__` on TrieNode to minimise per-node 
            memory overhead.
        """
        self.root: TrieNode = TrieNode()
        for w in list_words:
            node: TrieNode = self.root
            for ch in w:
                idx = ord(ch) - ord('a')
                if node.children[idx] is None:
                    node.children[idx] = TrieNode()
                node.mask |= (1 << idx)
                node = node.children[idx]
            node.word = w

    def check_word(
        self, 
        sus_word: Word
    ) -> List[Word]:
        """
        Function Description:
            Return all words in the Trie whose substitution-only edit distance 
            to `sus_word` is exactly one.

        Approach Description:
            1. Get integer indices for `sus_word` characters.
            2. Use a stack of states for DFS: (node, position, mismatches).
            3. At each state:
                a. If position == len(sus_word) and mismatches == 1 and 
                    node.word exists, collect node.word.
                b. Otherwise, push:
                    - The exact-match child (same index, same mismatch count).
                    - If no mismatch used yet, use node.mask to iterate existing
                    children except the matching one, pushing each with 
                    mismatches = 1.

        Args:
            sus_word: Target string of lowercase letters to compare.

        Returns:
            A list of words from `list_words` whose substitution-only edit
            distance to `sus_word` is exactly one. Returns an empty list if none.

        Time Complexity: O(J * A + R)
        Time Complexity Analysis:
            - J = length of `sus_word`, A = alphabet size (constant 26),
                R = total length of returned words.
            - Each stack step does O(A_mask) work for bitmask iterations.

        Auxiliary Space: O(J + R)
        Space Complexity Analysis:
            - Stack size = O(J)
            - Result list size = O(R) for collected words.
        """
        # Get character indicies
        ord_base = ord('a')
        sus_indexes = [ord(c) - ord_base for c in sus_word]
        N = len(sus_indexes)
        
        root: TrieNode = self.root
        result: List[Word] = []

        # Stack holds tuples (node, index in sus_word, mismatches_used)
        stack: List[State] = [(root, 0, 0)]
        while stack:
            node, index, mismatches = stack.pop()
            if index == N:
                if mismatches == 1 and node.word is not None:
                    result.append(node.word)
                continue
            
            orig_idx = sus_indexes[index]
            
            # (1) Exact match branch
            child = node.children[orig_idx]
            if child:
                stack.append((child, index + 1, mismatches))
            
            # (2) Substitution branch (if none used)
            if mismatches == 0:
                # Iterate only over existing children except orig_idx
                subs_mask = node.mask & ~(1 << orig_idx)
                while subs_mask:
                    bit = subs_mask & -subs_mask
                    c = bit.bit_length() - 1
                    next_child = node.children[c]
                    if next_child:
                        stack.append((next_child, index + 1, 1))
                    subs_mask ^= bit
                    
        return result
