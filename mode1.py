from data_structures.bst import BinarySearchTree
from data_structures.linked_stack import LinkedStack
from landsites import Land


class Mode1Navigator:
    """
    Student-TODO: short paragraph as per
    https://edstem.org/au/courses/14293/lessons/46720/slides/318306
    """

    def __init__(self, sites: list[Land], adventurers: int) -> None:
        """
        Initialises the Mode1Navigator with a list of land sites and the number
        of adventurers.
        
        :param sites: A list of land sites to plunder.
        :param adventurers: The number of adventurers available. 
        
        :complexity best & worst: O(N), we must get all sites from the sites 
        list and insert them into the sites_bst.
        """
        self.sites_bst = BinarySearchTree()
        for site in sites:
            if site.guardians > 0:
                ratio = site.gold / site.guardians
                self.sites_bst[ratio] = site
        
        self.adventurers = adventurers

    def select_sites(self) -> list[tuple[Land, int]]:
        """
        Selects the land sites to attack to maximise reward
        
        We iterate through the sites, and for each iteration, it selects the site
        with the best ratio (gold / guardians). The BinarySearchTree is used
        efficiently to find the site with the best ratio, and the operation is
        O(log(N)) in the worst case. The loop iterates at most N times, leading
        to a worst-case complexity of O(N * log(N)) or less. The best-case
        complexity is O(log(N)) or less.
        
        :return list[tuple[Land, int]]: A list containing the tuple pairs with
        Land and adventurers. 
        
        :complexity best: O(N * log(N)) or less, where N is the number of sites.
        :complexity worst: O(N) or less 
        """
        selected_sites = []
        current_adventurers = self.adventurers
        
        # Initialise the stack and iterator 
        site_stack = LinkedStack()
        site_iter = iter(self.sites_bst)
        
        # Push all nodes onto the stack
        for _ in range(len(self.sites_bst)):
            site_stack.push(next(site_iter).item)
        
        # Pop from the stack and select sites
        while current_adventurers > 0 and not site_stack.is_empty():
            current_site = site_stack.pop()
            c_i = min(current_adventurers, current_site.guardians)
            selected_sites.append((current_site, c_i))
            current_adventurers -= c_i

        return selected_sites

    def select_sites_from_adventure_numbers(self, adventure_numbers: list[int]) -> list[float]:
        """
        Calculates maximum amount of reward for different adventurer 
        configurations.
        
        We calculate the reward with different adventurers configs, and for each
        config size, it iterates through the islands using a loop. For C 
        different adventurers sizes and N sites, it results in a complexity of
        O(A * N).
        
        :param adventure_numbers: A list indicating the number of adventurers.
        
        :return list[float]: A list containing the amount of reward for each
        configuration.
        
        :complexity best: O(N), where N is the number of land sites.
        :complexity worst: O(A * N), where A is the length of adventure_numbers
        and N is the number of land sites.
        """
        results = []
        
        for adventurers in adventure_numbers:
            self.adventurers = adventurers
            selected_sites = self.select_sites()
            total_reward = 0.0
            
            for site, c_i in selected_sites:
                total_reward += min((c_i * site.gold)/site.guardians, site.gold)
            
            results.append(total_reward)
        
        return results

    def update_site(self, land: Land, new_reward: float, new_guardians: int) -> None:
        """
        Updates the state of the given land object with new reward and guardians.
        
        We update the gold and guardians for the specified land, and it involves
        no searching or iteration. Therefore, it has a complexity of O(1).
        
        :param land: The land site to be updated.
        :param new_reward: The new amount of gold for the land site.
        :parma new_guardians: The new number of guardians for the land site.
        
        :complexity best & worst: O(1)
        """
        land.gold = new_reward
        land.guardians = new_guardians

if __name__ == '__main__':
    sites = [
        Land('A', 40, 200),
        Land("B", 80, 300),
        Land("C", 20, 5),
        Land("D", 150, 250),
        Land("E", 10, 200)
    ]
    
    # Testing `update_site`
    navigator = Mode1Navigator(sites, 500)
    print('Before update:', navigator.select_sites())
    navigator.update_site(sites[1], 50, 100)
    print('After update:', navigator.select_sites())
    
    # Testing `select_sites_from_adventure_numbers`
    adventure_numbers = [0, 200, 500, 300, 40]
    rewards = navigator.select_sites_from_adventure_numbers(adventure_numbers)
    print(f'Best rewards for adventure_numbers ({adventure_numbers}): {rewards}')
    
    
    
    
    