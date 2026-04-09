"""
5) You are interviewing a large number of applicants for a job. There are 
three rounds of interviews, and for the first ruond, each applicant you 
interview is assigned a unique stability ranking. These rankings are represented
as an unsorted list of N items. Each item in this list is of the form 
(name, rank), where name is a string representing the applicant's name, and rank
is a unique floating point value ranging from 0 to 100. Once you've completed 
all the interviews in the first round, you want a quick way of calculating who 
should move on to the second and final rounds of interviews.

- The 50% of applicants who received the lowest suitability rankings will not 
progress any further with the interviews - they will be told they are 
unsuccessful in their application.

- The 20% of applicants who received the highest suitability rankings can skip 
the second round of interviews and instead go straight to the third round.

- The remaining 30% of applicants should progress to the second round of 
interviews.

Describe an efficient algorithm using QuickSelect to determine the names of 
applicants that you know will be proceeding to the second and third round of 
interviews, after completing the first round. Your algorithm should run in O(N) 
time, and you can assume that you have access to a QuickSelect algorithm which 
runs in O(N) time.
"""

import sys
import os
import random
from typing import List, Tuple

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algorithms_sorting.quick_select import quick_select

Name = str
Ranking = float

def interview_selection(applicants: List[Tuple[Name, Ranking]]) -> List[List[Tuple[Name, Ranking]]]:
    """
    Selects applicants for second and third rounds of interviews based on their
    stability rankings using QuickSelect.
    
    Parameters:
    -----------
    applicants : List[Tuple[Name, Ranking]]
        A list of tuples where each tuple contains the applicant's name and their
        stability ranking.
    
    Returns:
    -----------
    List[List[Tuple[Name, Ranking]]]
        A list containing two lists:
        - The first list contains applicants who will proceed to the second round.
        - The second list contains applicants who will proceed to the third round.
    
    Time Complexity: O(N)
    Space Complexity: O(N) for storing rankings and intermediate results.
    """
    N = len(applicants)
    
    # First round of interviews (assign random suitability ranking)
    for i in range(len(applicants)):
        name, ranking = applicants.pop(0)
        ranking = random.randrange(0, 100+1)
        applicants.append((name, ranking))

    # Grab the rankings from applicants and store in list
    ranks = [r for _, r in applicants]
    
    # Compute two order statistic indices (0-based)
    INDEX_50 = N//2 # Bottom 50% cutoff
    INDEX_20 = N - (N * 20 // 100) # Top 20 cutoff 
    
    # Find the two rank thresholds with QuickSelect 
    THRESHOLD_50 = quick_select(ranks[:], 0, N-1, INDEX_50-1)
    THRESHOLD_20 = quick_select(ranks[:], 0, N-1, INDEX_20-1)
    
    # Single pass over applicants to assign into rounds
    second_round = []
    third_round = []
    for applicant in applicants:
        _, ranking = applicant
        
        # 50% who got the lowest rankings WILL NOT progress.
        if ranking < THRESHOLD_50:
            continue
        
        # 20% who got the highest rankings can SKIP the second round.
        if ranking > THRESHOLD_20:
            third_round.append(applicant)
        # The remaining 30% must progress to the second round.
        elif ranking > THRESHOLD_50:
            second_round.append(applicant)
    
    return [second_round, third_round]
    
        

if __name__ == '__main__':
    applicants = [
        ('Jenul', -1), 
        ('Maria', -1), 
        ('John', -1),
        ('Max', -1),
        ('Jeff', -1),
        ('Nice', -1),
        ('Nice Person', -1)
    ]
    interview_selection(applicants)


