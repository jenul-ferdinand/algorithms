""" Stack ADT based on linked nodes. """

__author__ = 'Maria Garcia de la Banda, modified by Brendon Taylor and Alexey Ignatiev'
__docformat__ = 'reStructuredText'

from data_structures.stack_adt import *

class Node(Generic[T]):
    """ Implementation of a generic Node class.

        Attributes:
            item (T): the data to be stored by the node
            link (Node[T]): reference to the next node
    """

    def __init__(self, item: T = None) -> None:
        """ Object initializer. """
        self.item = item
        self.link = None


class LinkedStack(Stack[T]):
    """ Implementation of a stack with linked nodes.

        Attributes:
            length (int): number of elements in the stack (inherited)
    """

    def __init__(self, _=None) -> None:
        """ Object initializer. """
        Stack.__init__(self)
        self.top = None

    def clear(self) -> None:
        """" Resets the stack
        :complexity: O(1)
        """
        super().clear()
        self.top = None

    def is_empty(self) -> bool:
        """ Returns whether the stack is empty
            :complexity: O(1)
        """
        return self.top is None

    def is_full(self) -> bool:
        """ Returns whether the stack is full
            :complexity: O(1)
        """
        return False

    def push(self, item: T) -> None:
        """ Pushes an element to the top of the stack.
            :complexity: O(1)
        """
        new_node = Node(item)
        new_node.link = self.top
        self.top = new_node
        self.length += 1

    def pop(self) -> T:
        """ Pops the element at the top of the stack.
            :pre: stack is not empty
            :complexity: O(1)
            :raises Exception: if the stack is empty
        """
        if self.is_empty():
            raise Exception('Stack is empty')

        item = self.top.item
        self.top = self.top.link
        self.length -= 1
        return item

    def peek(self) -> T:
        """ Returns the element at the top, without popping it from stack.
            :pre: stack is not empty
            :complexity: O(1)
            :raises Exception: if the stack is empty
        """
        if self.is_empty():
            raise Exception('Stack is empty')
        return self.top.item
