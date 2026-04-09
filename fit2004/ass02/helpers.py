from typing import List
import random

def make_full_prefs(top_five: List):
    remaining_slots = [t for t in range(20) if t not in top_five] 
    return top_five + remaining_slots

def make_full_prefs_random(top_five: List):
    remaining_slots = [t for t in range(20) if t not in top_five]
    random.shuffle(remaining_slots)
    return top_five + remaining_slots

