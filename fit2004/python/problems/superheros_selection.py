"""
? Description
You are selecting a team of superheros to save the world. Unfortunately, you
can only bring a fixed amount of them through the portal.

You are given an unsorted list of N superheros where each item is in a tuple of 
(name, power level). You would want to send:

- The 1st team: The top-10% best superheros by power-level from that list.
- The 2nd team: the top-10% best superheros by power-level from the remainder
of that list.

You would however not send in the 2nd team until everyone in the 2nd team has
a power level greater than or equivalent to the median of the power level of 
the 1st team. The 2nd team would need to train until they reach that power 
level.

Describe an efficient algorithm using QuickSelect to determine the total power
level needed to be gained during training before the 2nd team can be sent out.
Your algorithm should run in O(N) time; and you can assume that you have
access to a QuickSelect algorithm which runs in O(N) time.
"""
from typing import List, Tuple
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algorithms_sorting.quick_select import quick_select

def pick_superheros(heros: List[Tuple[str, int]]):
    N = len(heros)
    
    # Find first team (top 10%) order statistic index
    idx = N - (N // 10)
    
    # Find the power level threshold for the first team
    name, top_10_power = quick_select(heros[:], 0, N-1, idx-1)
    
    # Do a single pass over heros to allocate the first team
    team1 = []
    for hero, power in heros:
        if power >= top_10_power:
            team1.append((hero, power))
    
    # Find the median of the first teams power level
    M = len(team1)
    name, first_team_median_power = quick_select(team1[:], 0, M-1, (M-1)//2)
    
    # Using the median power find the 2nd team and promotion ready heros (if any)
    team2 = []
    promotion = []
    for hero, power in heros:
        # 2nd team additions
        if power < first_team_median_power and power < top_10_power:
            team2.append((hero, power))
        
        # Ready for promotion (no training simulation prior so none here)
        if power >= first_team_median_power and power < top_10_power:
            promotion.append((hero, power))
        
    print('1st Team:', team1)
    print('2nd Team:', team2)
    print('Ready for promotion', promotion)
    
    
if __name__ == '__main__':
    heros = [
        ('Batman', 100),
        ('Superman', 90),
        ('Darkseid', 93),
        ('Dr Fate', 80),
        ('Blue Beetle', 78),
        ('Miss Martain', 74),
        ('The Flash', 60),
        ('Super Boy', 43),
        ('Kid Flash', 37),
        ('Beast Boy', 30),
    ]
    res = pick_superheros(heros)