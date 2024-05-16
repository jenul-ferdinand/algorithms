from algorithms.mergesort import mergesort
from data_structures.bst import BSTInOrderIterator, BinarySearchTree
from data_structures.heap import MaxHeap
from data_structures.linked_stack import LinkedStack
from landsites import Land


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
        reward = min((adventurers * gold) / guardians, gold)
        #print(f"Computed reward: {reward}")
        return reward
    
    def compute_score(self, remaining_adventurers, reward):
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
        results = []
        if not self.sites:
            return [(None, 0)] * self.n_teams 

        # Initialize a MaxHeap for potential scores
        max_heap = MaxHeap(len(self.sites))
        
        # Loop through every site in self.sites
        for site in self.sites:
            # If the current site has gold and guardians
            if site.get_gold() > 0 and site.get_guardians() > 0:
    
                # Get the adventurers used
                adventurers_used = min(site.get_guardians(), adventurer_size)
                
                # Compute the reward and the score
                reward = self.compute_reward(adventurers_used, site.get_gold(), site.get_guardians())
                score = self.compute_score(adventurer_size - adventurers_used, reward)
                
                # Add the site and adventurers_used to the MaxHeap
                max_heap.add((score, site, adventurers_used))

        # Iterate through each team
        for team in range(self.n_teams):
            if len(max_heap) == 0:
                results.append((None, 0))
                continue

            # Extract the site with the highest score
            _, site, adventurers_used = max_heap.get_max()
            #print(f"Team {team + 1} selects site {site.get_name()} with {adventurers_used} adventurers.")

            if site.get_guardians() > 0:
                reward = self.compute_reward(adventurers_used, site.get_gold(), site.get_guardians())
            else:
                reward = site.get_gold()
                
            #print(f"Reward: {reward}, Remaining gold: {site.get_gold() - reward}, Remaining guardians: {site.get_guardians() - adventurers_used}")

            # Update site's resources
            site.set_gold(site.get_gold() - reward)
            site.set_guardians(site.get_guardians() - adventurers_used)

            # Recompute the score and reinsert the site into the heap if it's still valid
            if site.get_guardians() > 0 and site.get_gold() > 0:
                new_adventurers_used = min(site.get_guardians(), adventurer_size)
                new_reward = self.compute_reward(new_adventurers_used, site.get_gold(), site.get_guardians())
                new_score = self.compute_score(adventurer_size - new_adventurers_used, new_reward)
                max_heap.add((new_score, site, new_adventurers_used))

            results.append((site, adventurers_used))

        return results
            
if __name__ == '__main__':
    # Initialise the sites for testing
    a = Land("A", 400, 100)
    b = Land("B", 300, 150)
    c = Land("C", 100, 5)
    d = Land("D", 350, 90)
    e = Land("E", 300, 100)
    sites = [
        a, b, c, d, e
    ]
    
    cur_guardians = {
        site.get_name(): site.get_guardians()
        for site in sites
    }
    cur_gold = {
        site.get_name(): site.get_gold()
        for site in sites
    }
    
    # Create a Mode2Navigator instance
    navigator = Mode2Navigator(8)
    
    # Add sites to the navigator
    navigator.add_sites(sites)
    
    # Simulate a day with an adventurer size of 100
    results = navigator.simulate_day(100)
    
    # Print the results
    for result in results:
        site, adventurers_used = result
        site_name = site.get_name() if site else "None"
        print(f'Site: {site_name}, Adventurers Used: {adventurers_used}')
        
    expected_scores = [400, 375, 337.5, 300, 250, 250, 250, 250]
    assert len(results) == len(expected_scores)
    
    for (site, sent_adventurers), expected in zip(results, expected_scores):
            
        if site is None:
            assert expected == 2.5 * 100
            continue
        gold = cur_gold[site.get_name()]
        guardians = cur_guardians[site.get_name()]
        if guardians == 0:
            received = gold
        else:
            received = min(gold, gold * sent_adventurers / guardians)
        # Update site
        cur_gold[site.get_name()] = gold - received
        cur_guardians[site.get_name()] = max(0, guardians - sent_adventurers)
        # Score
        score = 2.5 * (100 - sent_adventurers) + received
        print(f"Expected score: {expected}, Calculated score: {score}")
        assert expected == score