from __future__ import annotations

import math
from dataclasses import dataclass, field


@dataclass(eq=False)
class Node:
    key: int = None
    payload: int = None
    degree: int = 0
    mark: bool = False
    parent: Node | None = None
    child: Node | None = None

    left: Node = field(init=False)
    right: Node = field(init=False)

    def __post_init__(self):
        self.left = self
        self.right = self


class FibonacciHeap:
    """A forest of min-heap-ordered trees tracking a single minimum element"""

    def __init__(self):
        self.min: Node = None
        self.n = 0

    def minimum(self):
        return self.min.key

    def insert(self, key: int):
        # Merge the singleton heap into ours
        u = Node(key=key)
        h = FibonacciHeap()
        h.min = u
        h.n = 1
        self.merge(h)
        return u

    def merge(self, h: FibonacciHeap):
        if not h or not h.min:
            return

        if not self.min:
            self.min = h.min
            self.n = h.n
            return

        # save references to the nodes right next to the minimums
        self_next = self.min.right
        other_next = h.min.right

        # connect this min node to other heap's next node
        self.min.right = other_next
        other_next.left = self.min

        # connect other heap's min node to this heap's next node
        h.min.right = self_next
        self_next.left = h.min

        # update min pointer
        if h.min.key < self.min.key:
            self.min = h.min

        self.n += h.n

        h.min = None
        h.n = 0

    def _link_as_child(self, x: Node, y: Node) -> None:
        """Links node x as child of y"""
        # remove x from the root list
        x.left.right = x.right
        x.right.left = x.left

        # make x and child of y
        x.parent = y
        if y.child is None:
            y.child = x
            x.left = x
            x.right = x
        else:
            # splice x into y's circular child list
            x_next = y.child.right
            y.child.right = x
            x.left = y.child
            x.right = x_next
            x_next.left = x

        y.degree += 1
        x.mark = False

    def _consolidate(self):
        """Consolidates the root list by joining trees of equal degree"""
        if self.n == 0:
            return

        # determine the size bound using golden ratio log_phi(n)
        phi = (1 + 5**0.5) / 2
        max_degree = int(math.log(self.n, phi)) + 1
        degree_array: list[Node] = [None] * (max_degree + 1)

        # extract all roots into an array to avoid circular loop pointer error
        roots: list[Node] = []
        x = self.min
        if x is not None:
            start = x
            while True:
                roots.append(x)
                x = x.right
                if x == start:
                    break

        # process each root node
        for y in roots:
            d = y.degree
            while degree_array[d] is not None:
                x = degree_array[d]
                if y.key > x.key:
                    y, x = x, y

                # x becomes a child of y
                self._link_as_child(x, y)
                degree_array[d] = None
                d += 1

            degree_array[d] = y

        # rebuild the root list entirely from the unique trees in degree_array
        self.min = None
        for root in degree_array:
            if root is not None:
                if self.min is None:
                    self.min = root
                    root.left = root
                    root.right = root
                else:
                    # splice into the new root list
                    current_next = self.min.right
                    self.min.right = root
                    root.left = self.min
                    root.right = current_next
                    current_next.left = root

                    # track minimum node
                    if root.key < self.min.key:
                        self.min = root

    def extract_min(self):
        """Removes and returns the minimum node's key from the heap"""
        z = self.min

        # if the heap is already empty, return None
        if z is None:
            return None

        # elevate all children of z to the root list
        if z.child is not None:
            # gather all children into a list to avoid pointer corruption
            # during loop
            children: list[Node] = []
            x = z.child
            while True:
                children.append(x)
                x = x.right
                if x == z.child:
                    break

            # insert each child into the root list (right of z)
            for child in children:
                # remove child's parent reference
                child.parent = None

                # splice the child into the root list
                z_next = z.right
                z.right = child
                child.left = z
                child.right = z_next
                z_next.left = child

        # remove z from root list
        z.left.right = z.right
        z.right.left = z.left

        # handle cleanup and trigger consolidation
        if z == z.right:
            # case A: z was the only node left in the heap
            self.min = None
        else:
            # case B: there are other nodes remaining.
            # temporarily point min node to any remaining root node,
            # then consolidate to find the true minimum and fix degrees.
            self.min = z.right
            self._consolidate()

        self.n -= 1
        return z.key

    def decrease_key(self, x: Node, new_key: int) -> None:
        """Decreases the key of a node to a lower value"""
        if new_key > x.key:
            raise ValueError("New key is greater than current key")

        x.key = new_key
        y = x.parent

        # if heap-order is violated, cut the node from its parent
        if y is not None and x.key < y.key:
            self._cut(x, y)
            self._cascading_cut(y)

        # update the pointer to the minimum node if necessary
        if x.key < self.min.key:
            self.min = x

    def _cut(self, x: Node, y: Node) -> None:
        """Cuts node x from its parent y and places it in the root list"""
        # 1. remove x from y's child ring
        if x.right == x:
            # x was the only child
            y.child = None
        else:
            # splice x out of the linked child list
            x.left.right = x.right
            x.right.left = x.left
            if y.child == x:
                # update y's child pointer to a remaining sibling
                y.child = x.right

        y.degree -= 1

        # 2. add x into the top root list (right of min)
        current_right = self.min.right
        self.min.right = x
        x.left = self.min
        x.right = current_right
        current_right.left = x

        # 3. clean up node metadata
        x.parent = None
        x.mark = False

    def _cascading_cut(self, y: Node) -> None:
        """Recursively cuts parent nodes up the tree if they are marked"""
        z = y.parent
        if z is not None:
            if not y.mark:
                # if y is unmarked, mark it since it just lost its first child
                y.mark = True
            else:
                # if y is already marked, it has lost two children. Cut it.
                self._cut(y, z)
                self._cascading_cut(z)

    def delete(self, x: Node) -> None:
        """Removes node x from the heap"""
        self.decrease_key(x, float("-inf"))
        self.extract_min()