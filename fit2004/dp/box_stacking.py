from typing import List, Tuple

"""
Given `n` boxes [(L1, W1, H1), (L2, W2, H2), ... , (Ln, Wn, Hn)] .
Where box `i` has length Li, width Wi, and height Hi.
Find the height of the tallest possible stack.

Box (Li, Wi, Hi) can be on top of box (Lj, Wj, Hj) if Li < Lj & Wi < Wj.

? Overlapping Sub-Problems
- We can say to get the height of a box we should look at the boxes that can be
stacked on top of the current box.

? Optimal Substructure
- Let S be the set of all boxes that CAN be stacked on top of (Li, Wi, Hi)
- height((Li, Wi, Hi)) = Hi + max(height(Lk, Wk, Hk) : (Lk, Wk, Hk) is in S)

"""

Length = int
Width = int
Height = int
Box = Tuple[int, int, int]

def can_stack(bottom_box: Box, top_box: Box) -> bool:
        """Helper method to check if you can stack a box on another box"""
        bottom_length, bottom_width, _ = bottom_box
        top_length, top_width, _ = top_box
        return top_length < bottom_length and top_width < bottom_width

def tallest_stack(boxes: List[Box]) -> int:
    """
    Finds the tallest stack height of boxes
    """
    N = len(boxes)
    
    # Sort the boxes by length and width
    boxes.sort(key = lambda box: (box[0], box[1]))
    
    # Create a dictionary mapping each box to their startings heights
    heights: List[Height] = [None] * N
    for box_index, (length, width, height) in enumerate(boxes):
        heights[box_index] = height
    
    for i, (length, width, height) in enumerate(boxes):
        # Store the boxes that are stackable to the current box i
        stackable: List[Box] = []
        for j in range(len(boxes)):
            if can_stack((length, width, height), boxes[j]):
                stackable.append(boxes[j])
        
        # Store the heights of the subproblems
        subproblems: List[Height] = []
        for k in range(len(stackable)):
            subproblems.append(heights[k])
        
        # Calculate the height of the current box i
        heights[i] = height + max(subproblems, default=0)
        
    return max(heights)

def tallest_stack(boxes: List[Box]) -> int:
    boxes.sort(key = lambda box: (box[0], box[1]))
    heights = [height for (_, _, height) in boxes]
    
    for i, bottom in enumerate(boxes):
        valid_tops = [j for j in range(i) if can_stack(bottom, boxes[j])]
        best_above = max([heights[j] for j in valid_tops], default=0)
        heights[i] = bottom[2] + best_above
        
    return max(heights)
        
    

if __name__ == '__main__':
    boxes = [
        (1,1,1),
        (2,2,2),
        (1,2,2)
    ]
    height = tallest_stack(boxes)
    assert height == 3, f'Expected 3, got {height}'
    
    # Example from https://youtu.be/aPQY__2H3tE
    boxes = [
        (1,5,4),
        (1,2,2),
        (2,3,2),
        (2,4,1),
        (3,6,2),
        (4,5,3)
    ]
    height = tallest_stack(boxes)
    assert height == 7, f'Expected 7, got {height}'
    
    print('All test cases passed')