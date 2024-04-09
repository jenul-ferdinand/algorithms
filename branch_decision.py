from enum import auto, Enum


class BranchDecision(Enum):
    TOP = auto()
    BOTTOM = auto()
    STOP = auto()
