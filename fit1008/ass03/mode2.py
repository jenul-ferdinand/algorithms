from fit1008.ass03.data_structures.heap import MaxHeap
from fit1008.ass03.landsites import Land


class Mode2Navigator:
    """
    This class simulates a game where multiple teams of adventurers compete to
    ransack various land sites for gold. Each team selects a site to attack or 
    decides to skip their turn to maximise their potential score for the day.
    The game rules ensure that the team with the highest score at the end of 
    the day wins.
    """

    def __init__(self, n_teams: int) -> None:
        """
        Initialise the Mode2Navigator with number of teams and init the sites
        BST.
        
        :complexity best & worst: O(1)
        """
        self.n_teams = n_teams
        self.sites = []

    def add_sites(self, sites: list[Land]) -> None:
        """
        Adds a list of land sites to the existing sites.
        
        This method takes a list of `Land` objects and appends them to the
        existing self.sites list. 
        
        :param sites: A list of `Land` objects to be added to the existing list
        of sites.
        
        :complexity best & worst: O(N)
        - Where N is the length of the additional land sites.
        - Occurs when the method completes without any issues, simply appending
        the new sites to the existing list.
        """
        self.sites.extend(sites)

    def compute_reward(self, adventurers, gold, guardians):
        """
        Computes the reward based on the formula given (min((c_i*r)/g,r)).
        
        :param adventurers: The number of adventurers sent.
        :param gold: The amount of gold at the site.
        :param guardians: The number of guardians at the site.
        
        :complexity best & worst: O(1)
        """
        reward = min((adventurers * gold) / guardians, gold)
        #print(f"Computed reward: {reward}")
        return reward
    
    def compute_score(self, remaining_adventurers, reward):
        """
        Computes the score based on the formula given (O=2.5*c+r). 
        
        :param remaining_adventurers: The remaining adventurer numbers.
        :param reward: The gold gained on that day.
        
        :complexity best & worst: O(1)
        """
        score = (2.5 * remaining_adventurers + reward)
        #print(f"Computed score: {score}")
        return score
    
    def simulate_day(self, adventurer_size: int) -> list[tuple[Land | None, int]]:
        """
        Simulates a day of the game. Each team selects a land site to ransack
        or decides to do nothing. Returns the choices made by each team.
        
        Each team will choose the site with the highest potential score,
        computed based on the remaining adventurers adn the gold reward. The
        choices are stored in a MaxHeap to efficiently get the highest score
        site each time.
        
        :param adventurer_size: The size of the adventurer team for each team
        
        :return: A list of tuples, where each tuple contains the land site 
        chosen (or None if no site is chosen) and the number of adventurers
        sent.
        
        :complexity best: O(N + S)
        - Where S is the length of the additional land sites.
        - Where N is the number of existing land sites
        - Occurs when there are no valid sites to ransack (i.e, all sites have
        zero gold or guardians), so the method quickly returns after checking
        all sites.
        
        :complexity worst: O(N + K * log(N))
        - Where N is the number of existing land sites
        - Where K is the number of adventure teams participating in the game.
        - Occurs when the method processes each site and needs to reinsert 
        elements into the heap after updating them.
        """
        # Initialise a list to store the results
        results = []
        
        # If there are no sites, return a list with None for each team
        if not self.sites:
            return [(None, 0)] * self.n_teams 

        # Initalise a MaxHeap with the size of the sites list
        max_heap = MaxHeap(len(self.sites))
        
        # Loop through each site in the sites list
        for site in self.sites:
            # Check if the site has any gold and guardians left
            if site.gold > 0 and site.guardians > 0:
                # Determine the number of adventurers to use
                adventurers_used = min(site.guardians, adventurer_size)
                
                # Compute the reward based on the number of adventurers used
                reward = self.compute_reward(adventurers_used, site.gold, site.guardians)
                
                # Compute the score based on the remaining adventurers and the reward
                score = self.compute_score(adventurer_size - adventurers_used, reward)
                
                # Add the score, site, and adventurers_used as a tuple to the MaxHeap
                max_heap.add((score, site, adventurers_used))

        # Loop through each team
        for _ in range(self.n_teams):
            # If the MaxHeap is empty, append (None, 0) to results and continue to the next iterator
            if len(max_heap) == 0: results.append((None, 0)); continue

            # Extract the site with the highest score from the MaxHeap
            best_score_from_heap, site, adventurers_used = max_heap.get_max()
            
            # If the site has guardians, compute the reward
            if site.guardians > 0: reward = self.compute_reward(adventurers_used, site.gold, site.guardians)
            # If no guardians, no reward is just the site's gold
            else: reward = site.gold

            # Update the site's gold and guardians after the reward has been taken
            site.set_gold(site.gold - reward)
            site.set_guardians(site.guardians - adventurers_used)

            # If the site still has no guardians and gold left, reinsert it to the heap with the new score
            if site.guardians > 0 and site.gold > 0:
                new_adventurers_used = min(site.guardians, adventurer_size)
                new_reward = self.compute_reward(new_adventurers_used, site.gold, site.guardians)
                new_score = self.compute_score(adventurer_size - new_adventurers_used, new_reward)
                max_heap.add((new_score, site, new_adventurers_used))

            # Compute the score for skipping the turn
            remaining_adventurers = adventurer_size
            skip_score = self.compute_score(remaining_adventurers, 0)
            
            # Check if skipping the turn is more beneficial, append (None, 0)
            if skip_score > best_score_from_heap: results.append((None, 0))
            # Otherwise, append the site and adventurers used
            else: results.append((site, adventurers_used))

        # Return the results list
        return results
            
# if __name__ == '__main__':
#     # Initialise the sites for testing
#     a = Land("A", 400, 100)
#     b = Land("B", 300, 150)
#     c = Land("C", 100, 5)
#     d = Land("D", 350, 90)
#     e = Land("E", 300, 100)
#     sites = [
#         a, b, c, d, e
#     ]
    
#     # Storing the guardians and gold from the site in dictionary, site name as key.
#     cur_guardians = { site.get_name(): site.get_guardians() for site in sites }
#     cur_gold = { site.get_name(): site.get_gold() for site in sites }
    
#     # Create a Mode2Navigator instance
#     navigator = Mode2Navigator(8)
    
#     # Add sites to the navigator
#     navigator.add_sites(sites)
    
#     # Simulate a day with an adventurer size of 100
#     results = navigator.simulate_day(100)
    
#     # Print the results
#     for result in results:
#         site, adventurers_used = result
#         site_name = site.get_name() if site else "None"
#         print(f'Site: {site_name}, Adventurers Used: {adventurers_used}')
    
#     # Define expected scores provided by test case
#     expected_scores = [400, 375, 337.5, 300, 250, 250, 250, 250]
    
#     # Check if the length of our select_sites results list is the same length as
#     # the expected_scores list
#     assert len(results) == len(expected_scores)
    
#     # Looping through (site, sent_adventurers) from results and expected scores
#     for (site, sent_adventurers), expected in zip(results, expected_scores):
#         # If the site doesn't exist
#         if site is None:
#             # the expected value should be this
#             assert expected == 2.5 * 100
#             continue
        
#         # Get gold and guardians of current site
#         gold = cur_gold[site.get_name()]
#         guardians = cur_guardians[site.get_name()]
        
#         # Calculate received gold based on amount of guardians left at site
#         if guardians == 0: received = gold
#         else: received = min(gold, gold * sent_adventurers / guardians)
            
#         # Update site
#         cur_gold[site.get_name()] = gold - received
#         cur_guardians[site.get_name()] = max(0, guardians - sent_adventurers)
        
#         # Score
#         score = 2.5 * (100 - sent_adventurers) + received
#         print(f"Expected score: {expected}, Calculated score: {score}")
#         assert expected == score # This test case is failing...
