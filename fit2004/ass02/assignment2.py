from typing import List, Optional, Tuple

__author__ = "Jenul Devon Ferdinand (33119805)"
__email__ = "jfer0043@student.monash.edu"
__date__ = "27/05/2025"

#? =============================================================================|
#? TYPE ALIASES AND CONSTANTS
#? =============================================================================|

# Satisfaction level for a student
Satisfaction = int

# Represents a class which is a list of integers (max 3 elements)
# [class_time, min_students, max_students]
Class = List[int]
ClassTime = int
MinStudents = int
MaxStudents = int

# A preference is a list of class times permutation {0..19}
Preference = List[ClassTime]

# An allocation is a list of class times where each index is a student,
# indexed in order based on the order of students from time_prefs.
Allocation = List[int]

# Allocation value for unassigned students
UNASSIGNED = -1

#! =============================================================================|
#! Crowded Campus Algorithm with Elastic Swap Repair
#! =============================================================================|

def crowdedCampus(
    num_students: int,
    num_classes: int,
    time_prefs: List[Preference],
    classes: List[Class],
    min_satis: Satisfaction
) -> Optional[Allocation]:
    """
    Function Description:
        Verifies whether a valid allocation of students into proposed classes 
        exists that satisfies each class's capacity constraints, and ensures at 
        least `min_satis` students are placed in a class whose time-slot is 
        within their top-5 preferences.

    Approach Description:
        1. Greedy top-5 assignment: For each student, assign to the first 
        available class among their top-5 where capacity remains.
        
        2. Fill minimums also with swapping: For each class, fulfill its minimum
        occupancy by assigning from the pool of unassigned students; if that pool
        is empty, reassign students from classes currently above their min,
        even if it reduces satisfaction, tracking final satisfaction later.
        
        3. Dump leftovers: Assign any still-unassigned students to any class
        with remaining capacity.
           
        4. Check satisfaction: Calculate the number of students in their top-5
        slots; if it's below `min_satis`, return None.
        
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

    Time Complexity: O(N * M) = O(N^2) worst-case when M is on average O(N).
    Time Complexity Analysis:
        - Building `time_to_classes`: O(M)
        - Step 1 (greedy top-5): Each of the N students examines up to 5 slots
            and scans classes in that slot -> O(N * 5 * (M/20)) = O(M * N)
        - Step 2a (fills mins with swaps): At most N fills/steals, each may 
            scan O(M + N) in worst case -> O(N * (M + N)) = O(N * M).
        - Step 2b (dumping leftovers): Scans remaining students (<= N) and up
            to M classes each -> O(N * M).
        - Satisfaction counting: O(N * 5) = O(N).
        Total: O(N * M) -> O(N^2) in the worst case.
    
    Auxiliary Space Complexity: O(N + M) = O(N) worst-case when M = O(N).
    Auxiliary Space Complexity Analysis:
        - `time_to_classes`: O(M).
        - `class_mins`, `class_maxs`: O(M).
        - `allocation`, `class_filled`: O(N + M).
        - `remaining` list and swap indicies: O(N).
        - Constant extra variables and counters.
        Total: O(N + M) -> O(N) in the worst case.
        
    Terms:
        - N = Number of students (`num_students`)
        - M = Number of classes (`num_classes`)
        
    Notes for Marker:
    - This algorithm uses a greedy approach, I went with this approach to more 
    easily to adhere to the time and space constraints of the problem, compared 
    to using a more complex max flow solution.
    
    Thank you!
    """
    # Build time-slot -> class indices mapping
    time_to_classes: List[List[int]] = [[] for _ in range(20)]
    for j, c in enumerate(classes):
        time_to_classes[c[0]].append(j)
    
    # Get class mins and maxs
    class_mins = [c[1] for c in classes]
    class_maxs = [c[2] for c in classes]

    # Allocation state
    allocation: Allocation = [UNASSIGNED] * num_students
    class_filled = [0] * num_classes

    # * (1) Greedily allocate top-5 preferences
    for i in range(num_students):
        for r in range(5):
            slot = time_prefs[i][r]
            for j in time_to_classes[slot]:
                if class_filled[j] < class_maxs[j]:
                    allocation[i] = j
                    class_filled[j] += 1
                    break
            if allocation[i] != UNASSIGNED:
                break

    # * (2) Fill minimums with swap if needed
    remaining = [i for i, a in enumerate(allocation) if a == UNASSIGNED]
    for j in range(num_classes):
        needed = max(0, class_mins[j] - class_filled[j])
        while needed > 0:
            if remaining:
                i = remaining.pop()
                prev = UNASSIGNED
            else:
                # Find any overfull class k to steal from
                prev = None
                for k in range(num_classes):
                    if class_filled[k] > class_mins[k]:
                        # Steal a student from class k 
                        for ii in range(num_students):
                            if allocation[ii] == k:
                                i = ii
                                prev = k
                                break
                    if prev is not None:
                        break
                if prev is None:
                    return None
                class_filled[prev] -= 1
            # Assign student i into class j
            allocation[i] = j
            class_filled[j] += 1
            needed -= 1

    # * (3) Dump any truly leftover students
    # * (those still UNASSIGNED after step 2)
    for i, a in enumerate(allocation):
        if a == UNASSIGNED:
            placed = False
            for j in range(num_classes):
                if class_filled[j] < class_maxs[j]:
                    allocation[i] = j
                    class_filled[j] += 1
                    placed = True
                    break
            if not placed:
                return None

    # Sanity check: occupanccy within [min, max]
    for j in range(num_classes):
        if not (class_mins[j] <= class_filled[j] <= class_maxs[j]):
            return None

    # * (4) Calculate final satisfaction
    satisfied = 0
    for i in range(num_students):
        slot_i = classes[allocation[i]][0]
        for r in range(5):
            if time_prefs[i][r] == slot_i:
                satisfied += 1
                break
    if satisfied < min_satis:
        return None

    # Output proposed allocation
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
