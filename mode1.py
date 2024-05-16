from data_structures.bst import BinarySearchTree
from data_structures.linked_stack import LinkedStack
from landsites import Land

class Mode1Navigator:
    """
    The Mode1Navigator class is made to manage how many adventurers should go
    to various land sites in order to maximise the reward based on the 
    gold-to-guardian ratio. The class supports initialising with a list of land
    sites to attack and a number of adventurers, choosing the optimal sites to 
    attack, calculating the rewards for different configs of adventurer numbers,
    and updating the properties of land sites.
    """

    def __init__(self, sites: list[Land], adventurers: int) -> None:
        """
        Initialises the Mode1Navigator with a list of land sites and the number
        of adventurers.
        
        :param sites: A list of land sites to plunder.
        :param adventurers: The number of adventurers available. 
        
        :complexity best & worst: O(N * log(N)), we must get all sites from the 
        sites list and insert them into the sites_bst. Insertion into the BST
        takes O(log(N)) time on average, leading to a total complexity of 
        O(N * log(N)) for N sites.
        """
        self.sites_bst = BinarySearchTree()
        {self.sites_bst.__setitem__(site.gold / site.guardians, site) 
            for site in sites if site.guardians > 0}
        self.adventurers = adventurers

    def select_sites(self) -> list[tuple[Land, int]]:
        """
        Selects the land sites to attack to maximise reward
        
        This method iterates through the land sites stored in the self.sites_bst.
        Then it chooses the sites to attack for the best reward (based on the
        gold-to-guardian ratio), this makes sure that the sites that give the
        highest gold for the lowest amount of guardians are prioritised. This
        method initialises a Linked Stack. Then all the sites are pushed to the
        stack, and then the sites are popped from the stack until all the
        adventurers are allocated or the stack is empty. For every site, this
        method determines the no. of adventurers to send (up until the amount
        of guardians at thee site) and appends the tuple (site, c_i) to the
        sites list (which is returned). 
        
        It doesn't modify the state of the orignal 'Land' objects or the no. of 
        adventurers. Each call to the method will get the same result as long as
        the state of `self.sites_bst` and `adventurers` remains unchanged.
        
        :return list[tuple[Land, int]]: A list containing the tuple pairs with
        Land and adventurers. 
        
        :complexity best & worst: O(N)
        - Where N is the number of sites.
        - Occurs when each site is processed exactly once, regardless of the
        structure of the BST.
        """
        sites = []
        adventurers = self.adventurers
        
        # Push all nodes onto the stack
        site_stack = LinkedStack()
        [site_stack.push(site.item) for site in self.sites_bst]
        
        # Pop from the stack and select sites
        while not site_stack.is_empty() and adventurers > 0:
            site = site_stack.pop()
            c_i = min(adventurers, site.guardians)
            sites.append((site, c_i))
            adventurers = adventurers - c_i

        return sites

    def select_sites_from_adventure_numbers(self, adventure_numbers: list[int]) -> list[float]:
        """
        Calculates maximum amount of reward for different adventurer number
        configurations.
        
        This method calculates the reward for each number of adventurers in 
        the `adventure_numbers` list. For each list, it sets the number 
        of adventurers and calls the `select_sites` method to choose the best 
        land sites to attack. It then calculates the total reward based on the
        number of adventurers sent using the formula given.
        
        :param adventure_numbers: A list indicating the number of adventurers.
        
        :return list[float]: A list containing the amount of reward for each
        configuration.
        
        :complexity best: O(A * N)
        - where N is the number of land sites.
        - Occurs when the number of adventurers is a lot less than the number
        of guardians at each site.
        
        :complexity worst: O(A * N * log(N))
        - Where A is the length of adventure_numbers, and N is the number 
        of land sites.
        - Occurs when the number of adventurers is high compared to the number
        of guardians, requiring detailed allocating and processing. 
        """
        results = []
        
        for adventurers in adventure_numbers:
            self.adventurers = adventurers
            selected_sites = self.select_sites()
            total_reward = sum(min((c_i * site.gold) / site.guardians, site.gold) for site, c_i in selected_sites)
            results.append(total_reward)
        
        return results

    def update_site(self, land: Land, new_reward: float, new_guardians: int) -> None:
        """
        Updates the state of the given land object with new reward and guardians.
        
        This method updates the properties of a given `Land` object to reflect
        new values for its gold and number of guardians. The method directly 
        modifies the `gold` and `guardians` attributes of the land object.
        
        :param land: The land site to be updated.
        :param new_reward: The new amount of gold for the land site.
        :param new_guardians: The new number of guardians for the land site.
        
        :complexity best & worst: O(1)
        - Just assigning new values which is constant time.
        """
        land.gold = new_reward
        land.guardians = new_guardians

if __name__ == '__main__':
    # Initalise the sites for testing
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
    
    
    
    
    