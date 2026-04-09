from pokemon import *
import random
from battle_mode import BattleMode
from data_structures.referential_array import ArrayR
from data_structures.bset import BSet
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem



# ===================== POKE TEAM CLASS =====================
class PokeTeam:
    #! ===================== CLASS VARIABLES =====================
    # Maximum number of pokemon in a team
    TEAM_LIMIT      = 6
    
    # The list of all pokemon
    POKE_LIST       = get_all_pokemon_types()
    
    # The list of criterions to sort by
    CRITERION_LIST  = ["health", "defence", "battle_power", "speed", "level"]

    #! ===================== CLASS: INITIALISE =====================
    def __init__(self):
        # The main team
        self.team = ArrayR(self.TEAM_LIMIT)
        # A copy of the team
        self.team_copy = ArrayR(self.TEAM_LIMIT)
        # A counter for how many pokemon are in our team
        self.team_count = 0
        # The current battle mode
        self.battle_mode = None 
        # The criterion for team organisation
        self.criterion = None 
        # This multiplier will determine our sorting order
        self.sort_order_multiplier = 1

    

    #? ===================== INTERNAL: TOGGLE SORT ORDER ===================== DONE
    def _toggle_sort_order(self) -> None:
        """
        Toggles the sorting order multipler between ascending and descending
        
        :post: The sort_order_multiplier is negated, toggling the sorting order.
        
        :comp best: O(1)
            As the operation is a simple multiplication and assignment.
            
        :comp worst: O(1)
            Identical to the best case because the complexity does not depend on any variable factors.
        """
        self.sort_order_multiplier *= -1
    
    #? ===================== INTERNAL: BACKUP CURRENT TEAM ===================== DONE
    def _backup_current_team(self) -> None:
        """ Copies elements from team to team_copy
        
        :post: The current state of the team is copied to team_copy, allowing
               for future restoration if necessary.

        :comp best: O(t) 

        :comp worst: O(t) 
        
        Both the best and worst case occur when the we have to iterate over the team_count, assuming that we can make a larger team than 6.
        
        - Where t is the number of items in the team (self.team_count).

        Considering that isinstance is assumed to be O(1) for all future methods
        """
        if isinstance(self.team, ArrayR):
            for i in range(self.team_count):
                self.team_copy[i] = self.team[i]



    #* ===================== CHOOSE MANUALLY ===================== DONE
    def choose_manually(self) -> None:
        """
        Allows the user to choose their team
        
        :return: None
        :post: The team will contain the Pokemon chosen by the user, up to the team limit or until the user stops the selection.
        
        :comp best: O(1) 
            This best case occurs when/if the user decides to type 'done' immediately
        
        :comp worst: O(N * P) 
            This worst case occurs when the user decides to choose a full team of Pokemon
            
        - N is the number of Pokemon the user decides to choose (up to TEAM_LIMIT)
        - P is the total number of available Pokemon in POKE_LIST.
        """
        print('\n❓ Select up to 6 Pokemon by entering their name. Type "done" to finish:')
        
        a = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣤⣶⣶⣶⣶⣶⣶⣶⣶⣦⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣶⣿⣿⠿⠟⠛⠋⠉⠉⠉⠉⠙⠛⠻⠿⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⡿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⢿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⡿⠋⠀⠀⠀⣀⡖⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⠟⠀⠀⠀⠀⡖⠃⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⠋⠀⠀⠀⠀⡏⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⡏⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⢀⣠⣶⣶⣶⣶⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⠿⠛⠛⠿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣤⣤⣤⣤⣤⣤⣤⣤⣼⣯⡏⠀⠀⠀⠀⠀⠀⠘⣿⣿⣤⣤⣤⣤⣤⣤⣤⣤⣽⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡟⠛⠛⠛⠛⠛⠛⠛⠛⢻⡟⣦⠀⠀⠀⠀⠀⠀⢀⣿⡿⠛⠛⠛⠛⠛⠛⠛⠛⢻⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣦⣤⣤⣴⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⡿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢸⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⢿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣯⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣿⣷⣶⣤⣄⣀⣀⡀⢀⣀⣀⣠⣠⣤⣾⣶⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠻⠿⠿⠿⠿⠿⠿⠿⠿⠿⠻⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            """
        print(a)
        
        self.team_count = 0
        while self.team_count < self.TEAM_LIMIT: 
            user_input = input('💡 Enter Pokemon name or "done" to finish: ').strip().lower()
            
            if user_input == 'done': 
                # if self.team_count == 0: 
                #     raise ValueError('No pokemon chosen, shouldve called choose_randomly() here')
                # else: 
                break 
            
            found = False
            for pokemon_cls in self.POKE_LIST:
                if user_input.capitalize() == pokemon_cls().get_name():
                    self.team[self.team_count] = pokemon_cls()
                    self.team_count += 1
                    print(f'{pokemon_cls().get_name()} added to the team')
                    found = True 
                    break
            if not found:
                print('Invalid Pokemon name, try again.')
            
        print(f'Team selection complete, team: {self.team}') 

    #* ===================== CHOOSE RANDOMLY ===================== DONE
    def choose_randomly(self) -> None:
        """
        Chooses a random team of 6
        
        :return: None
        :post: The team will be filled with random Pokemon up to the team limit.
        
        :comp best: O(T)
        
        :comp worst: O(T)
        
        Both the best and worst case occur no matter what because we must iterate and create a random team of 6.
        
        - Where T is the length of TEAM_LIMIT
        
        Assuming that randint is O(1) for all future functions
        """
        # Print guide message
        print('\n🎲 Creating a random team of 6 pokemon')
        
        # Print art
        a = """
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠄⠒⠒⠒⠠⢄⡀⠀⠀⠀⠀⢀⡠⠔⠊⠱⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠎⠁⠀⠀⠀⠀⠀⠀⠀⠈⠒⢤⠔⠊⠁⢀⣠⣶⡆⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠬⢢⣄⠀⠀⠀⠀⠀⠀⠀⠀
⡤⠀⠤⠤⠤⠤⠀⣀⣀⠀⠀⠀⠀⠀⢀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠳⡀⣴⣿⣿⣿⡇⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡀⠀⠈⢳⡀⠀⠀⠀⠀⠀⠀
⡇⠀⣀⣀⣀⡀⠀⠀⠀⠈⠉⠐⠢⠞⠁⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⡙⠿⣿⣿⡇⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠇⠀⠀⠀⠀⠀⠀
⢃⠀⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢣⠀⠈⠻⢃⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠇⠀⠀⠘⠀⠀⠀⠀⠀⠀⠀
⢸⠀⢿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠘⠦⣀⣀⣀⣀⣀⣤⡀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠘⢆⠀⠀⠀⠀⠀⠀⠀⡠⠔⠀⡀⡂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢇⠸⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⢠⠋⠀⠩⣧⠀⠀⠀⢀⠆⠀⠀⠀⠀⠈⢧⠀⠀⠀⠀⠀⠀⠧⠤⠦⠚⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄
⠀⠘⡄⠻⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⡀⠀⢸⡀⠀⠀⠁⠁⠤⣠⠊⠀⡠⠪⢭⡭⢐⠈⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠊⠅
⠀⠀⠘⢤⠘⠃⠀⠀⠀⠀⠀⠀⢀⠤⠂⠉⠀⢶⣆⡠⢍⡐⢕⠂⠤⠤⠐⠋⠀⠀⡘⡄⠀⠀⢹⣧⠑⡙⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⣀⠀⠀⡰⠁⠀⢰
⠀⠀⠀⠀⢱⠀⠀⠀⠀⠀⠀⠠⠊⠀⠀⠀⠀⠀⢹⡭⢧⡈⢢⠑⡀⠀⠀⠀⠀⠀⡇⣧⣀⣀⡼⣞⡇⢡⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠢⠤⠨⠎⠀⠀⠀⠈
⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⡆⣄⠀⠀⠀⠀⠀⢸⡗⢮⡇⠈⠆⢃⠀⠀⠀⠀⠀⢡⢻⣟⣏⢧⡽⠃⡜⣼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠸⠀⡿⣦⣀⣀⣀⣴⠻⣜⣣⡇⠀⡸⢘⠀⠀⠀⠀⠀⠀⠡⢑⠭⠉⠠⠜⠔⢸⠒⠂⠐⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⡆⠀⠀⠀⠀⠀⢇⠱⡙⢮⣳⣍⣖⣫⡼⠋⠀⢠⠃⠎⠀⠀⠀⠀⠀⠀⢀⠀⠁⠐⠀⠁⠀⡆⠀⢀⠞⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢱⡀⠀⠀⠀⠀⠀⠢⡑⠤⡀⠈⠁⠀⠀⣀⠔⡡⠊⠀⠀⠀⡤⡤⠴⣲⠋⠀⠀⠀⠀⠀⣰⠥⠒⠁⠀⠀⠀⠀⠀⠀⠀⠡⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢻⡄⠀⠀⠀⠀⠀⠈⠐⠠⠭⠉⠭⠥⠐⠈⣠⠤⣄⠀⠰⣇⡶⠳⡏⠀⠀⠀⠀⠀⢠⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠡⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠻⡦⢀⠀⠀⠀⠀⠀⠐⠦⡀⠀⠀⢠⣿⣶⣦⡰⣷⠀⠘⠦⠜⠀⠀⠀⠀⠀⡠⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠙⢦⡁⠢⢀⠀⠀⠀⠀⠈⠳⣴⣿⣿⣿⣿⣷⠟⠀⠀⠀⠀⠀⠀⠀⣠⠜⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠦⡀⠈⣐⣀⣀⣀⣀⣼⣿⠟⠋⠉⠀⠀⠀⠀⠀⠀⠀⣠⠞⠉⠁⠒⠒⠤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡨⠵⠂⠀⠘⡿⠿⠋⠁⠀⠀⠀⠀⠀⢀⣀⠤⠶⠭⠀⣀⣀⠀⠀⠤⠔⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡠⠔⠉⠀⠀⠀⠀⠀⢀⡨⠝⠓⠒⠒⠒⠒⠋⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠺⠤⠀⠤⠤⠤⠄⠒⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        """
        print(a)
        
        # Start the team_count at zero
        self.team_count = 0
        
        # All pokemon
        all_pokemon = get_all_pokemon_types()

        # Loop 6 times
        for i in range(self.TEAM_LIMIT):
            # Choose a random number from the amount of all the pokemon (77)
            rand_int = random.randint(0, len(all_pokemon)-1)
            
            # Initalise and add the random pokemon class to the team
            self.team[i] = all_pokemon[rand_int]()
            
            # Increment the team count
            self.team_count += 1
            
            # Print each new pokemon's name (numbered)
            print(f'Pokemon ({i+1}): {self.team[i].get_name()}')

        # Print that we're done creating the team
        print('\n✅ Random team created!')

    #* ===================== REGENERATE TEAM ===================== DONE
    def regenerate_team(self, battle_mode: BattleMode, criterion: str = None) -> None:
        """
        Regens the HP of the PokeTeam, to their original HP
        
        :param battle_mode: The mode of battle which influences how the team is organized.
        :param criterion: Optional sorting criterion used in the OPTIMISE battle mode.
        :return: None
        :post: The team's health is restored, and its order may be updated based on battle_mode and criterion.
        
        :comp best: O(C)
            This best case occurs when the battle_mode is either SET or ROTATE
            
        :comp worst: O(C * log(T))
            This worst case occurs when the battle_mode is OPTIMISE
        
        - Where C is the length of self.team_copy
        - Where T is the number of elements in self.team
        """
        match battle_mode:
            # SET BATTLE MODE
            case BattleMode.SET:
                # Initialise the team as a stack
                self.team = ArrayStack(self.TEAM_LIMIT)
                
                # For each pokemon in the copy of the team
                for pokemon in self.team_copy:
                    # Set the pokemon's health to the original
                    pokemon.health = pokemon.__class__().health
                    # Push the pokemon to the stack
                    self.team.push(pokemon)  
            
            # ROTATE BATTLE MODE
            case BattleMode.ROTATE:
                # Initialise the team as a circular queue
                self.team = CircularQueue(self.TEAM_LIMIT)
                
                # For each pokemon in the copy of the team
                for pokemon in self.team_copy:
                    # Set the pokemon's health to the original
                    pokemon.health = pokemon.__class__().health
                    # Append the pokemon to the queue
                    self.team.append(pokemon)
            
            # OPTIMISE BATTLE MODE
            case BattleMode.OPTIMISE:
                # Initalise the team as a sorted list array implementation
                self.team = ArraySortedList(self.TEAM_LIMIT)
                
                # For each pokemon in the copy of the team
                for pokemon in self.team_copy:
                    # Set the pokemon's original health to the original
                    pokemon.health = pokemon.__class__().health
                    
                    # Add the pokemon to the sorted list as a ListItem and attribute as the key
                    self.team.add(ListItem(pokemon, (getattr(pokemon, criterion) * self.sort_order_multiplier)))

    #* ===================== ASSIGN TEAM ===================== DONE
    def assign_team(self, criterion: str = None) -> None:
        """
        Assigns the team to a ArraySortedList
        
        :param criterion: The attribute (e.g., 'health', 'speed') to sort the Pokemon by.
        :post: The team is sorted based on the specified criterion.
        
        :comp best: (T + log(U))
            This best case occurs when updated_team does not require resizing
            
        :comp worst: O(T * U)
            This worst case occurs when updated_team required resizing
        
        - Where T is the length of self.team
        - Where U is the length of updated_team
        """
        self._backup_current_team()
        self.criterion = criterion 
        updated_team = ArraySortedList(self.TEAM_LIMIT)
        
        if isinstance(self.team, ArrayR):
            for pokemon in self.team:
                sort_value = getattr(pokemon, self.criterion) * self.sort_order_multiplier
                updated_team.add(ListItem(pokemon, sort_value))
                
        elif isinstance(self.team, ArraySortedList):
            for list_item in self.team:
                pokemon = list_item.value
                sort_value = getattr(pokemon, self.criterion) * self.sort_order_multiplier
                updated_team.add(ListItem(pokemon, sort_value))
                
        self.team = updated_team

    #* ===================== ASSEMBLE TEAM ===================== DONE
    def assemble_team(self, battle_mode: BattleMode) -> None:
        """ 
        Assembles the team to a CiruclarQueue
        
        :param battle_mode: The battle mode determining the structure to organize the team in.
        :post: The team is organized into a data structure (stack, queue, or sorted list) suitable for the battle mode.
        
        :comp best: O(T)
        :comp worst: O(T)
            Both the best and worst case occur when iterating through self.team_count and pushing or appending the Pokemon in to the temp_team.
        
        - Where T is the length of self.team_count
        """
        self._backup_current_team()
        
        if battle_mode == BattleMode.SET:
            temp_team = ArrayStack(self.TEAM_LIMIT)
        elif battle_mode == BattleMode.ROTATE:
            temp_team = CircularQueue(self.TEAM_LIMIT)
        
        for i in range(self.team_count):
            pokemon = self.team[i]
            if isinstance(temp_team, ArrayStack):
                temp_team.push(pokemon)
            elif isinstance(temp_team, CircularQueue):
                temp_team.append(pokemon)
                
        self.team = temp_team

    #* ===================== SPECIAL ===================== DONE
    def special(self, battle_mode: BattleMode) -> None:
        """
        Applies a special arrangement or action to the team based on the battle mode.

        :param battle_mode: The mode of battle which determines the specific action to be taken.
        :return: None
        :post: The team is modified in a special way suitable for the given battle mode.
        
        :comp best: O(T) 
            This best case occurs when the battle_mode is either SET or ROTATE
            
        :comp worst: O(T * U)
            This worst case occurs when the battle_mode is OPTIMISE because assign_team is called (also taking the worst case of assign_team)
        
        - Where T is the length of self.TEAM_LIMIT
        - Where U is the length of the updated_team in assign_team()
        """
        match battle_mode:
            case BattleMode.SET:
                half_stack          = ArrayStack(self.TEAM_LIMIT // 2)
                reverse_half_stack  = ArrayStack(self.TEAM_LIMIT // 2)

                # Push top half of the contents of self.team to the half_stack
                while not len(self.team) == self.TEAM_LIMIT // 2:
                    team_item = self.team.pop()
                    half_stack.push(team_item)
                    
                # Push the contents of half_stack to the reverse_half_stack
                while not half_stack.is_empty():
                    half_stack_item = half_stack.pop()
                    print(half_stack_item)
                    reverse_half_stack.push(half_stack_item)
                    
                # Now push the reversed contents to self.team
                while not reverse_half_stack.is_empty():
                    reverse_half_stack_item = reverse_half_stack.pop()
                    self.team.push(reverse_half_stack_item)

                # Now the top half self.team is reversed
            
            case BattleMode.ROTATE:
                temp_queue          = CircularQueue(self.TEAM_LIMIT)
                second_half_queue   = CircularQueue(self.TEAM_LIMIT)
                midpoint = self.team_count // 2

                # Serve the first half of the team and append it back to ensure order
                serve_count = 0
                while serve_count < midpoint:
                    item = self.team.serve()
                    temp_queue.append(item)
                    serve_count += 1

                # Serve the second half of the team into a separate queue
                while serve_count < self.team_count:
                    item = self.team.serve()
                    second_half_queue.append(item)
                    serve_count += 1

                # Append the first half back to the team from temp_queue
                while not temp_queue.is_empty():
                    item = temp_queue.serve()
                    self.team.append(item)

                # Append the second half back to the team from second_half_queue
                while not second_half_queue.is_empty():
                    item = second_half_queue.serve()
                    self.team.append(item)
                    
                # Now the last half of self.team is reversed
                
            case BattleMode.OPTIMISE:
                # Toggle the sorting order
                self._toggle_sort_order()
                
                # Calling assign team to sort by current criterion
                try: 
                    self.assign_team(self.criterion)
                except ValueError as e:
                    print(f'❌ Error: {e}')


    #! ===================== DUNDER: GET ITEM ===================== DONE
    def __getitem__(self, index: int):
        """
        Retrieves an item from the team at the specified index. This method 
        abstracts the underlying data structure, whether it's an ArrayR, 
        ArrayStack, ArraySortedList, or CircularQueue.

        :param index: The index of the item to retrieve.
        :return: The item at the specified index.
        :raises IndexError: If the index is out of bounds for the team's current size.
        
        :comp best: O(1)
            This best case occurs when self.team is an instance of ArrayR or ArraySortedList, this is constant time when accessing directly. 
            
        :comp worst: O(N) 
            This worst case occurs when self.team is an instance of ArrayStack or CircularQueue, this is linear time to find the target index element in self.team
        
        - Where N is the distance to the index for the length of self.team
        """
        try:
            # ArrayR And ArraySortedList
            if isinstance(self.team, ArrayR) or isinstance(self.team, ArraySortedList):
                return self.team[index] if isinstance(self.team, ArrayR) else self.team[index].value
            
            # ArrayStack
            elif isinstance(self.team, ArrayStack):
                # Create a temporary stack to hold items
                holding_stack = ArrayStack(self.TEAM_LIMIT)
                
                # Pop the first item from the stack
                target_item = self.team.pop()
                # Push the first item to the holding stack for temporary storage
                holding_stack.push(target_item)
                
                # Loop to pop items up to the specified index, storing them in holding stack
                for _ in range(index):
                    # Pop an item from the team stack
                    target_item = self.team.pop()
                    
                    # Push the popped item to the holding stack
                    holding_stack.push(target_item)
                    
                # Restore items from holding stack back to the original stack
                # This ensures the original order is maintained
                while not holding_stack.is_empty():
                    self.team.push(holding_stack.pop())
                    
                # Return the target item after all other items have been restored
                return target_item
            
            # CircularQueue
            elif isinstance(self.team, CircularQueue):
                # Initialise a temporary queue to hold items during the process
                holding_queue = CircularQueue(self.TEAM_LIMIT)
                
                # Serve the first item from the team queue
                target_item = self.team.serve()
                # Append the first item to the holding queue for temporary storage
                holding_queue.append(target_item)
                
                # Loop through the queue up to the specified index, moving items to the holding queue
                for _ in range(index):
                    # Serve an item from the team queue
                    target_item = self.team.serve()
                    
                    # Append the served item to the holding queue
                    holding_queue.append(target_item)
                    
                # Refill the original queue with the remaining items from the holding queue
                # This action also restores the served items back to the original queue
                while not self.team.is_empty():
                    holding_queue.append(self.team.serve())
                    
                # Move all items from the holding queue back to the original queue
                # This ensures that the original order of items in the queue is maintained
                while not holding_queue.is_empty():
                    self.team.append(holding_queue.serve())
                    
                # Return the initially serve target item after restoring the queue
                return target_item
            
            # Any other type
            else:
                raise TypeError("This type is not supported")
        except IndexError:
            print(f'❌ Error: Rquested Index {index} is out of bounds for the team size')
            return None

    #! ===================== DUNDER: LEN ===================== 
    def __len__(self):
        """
        Returns the number of items in the team. This method abstracts the 
        underlying data structure's length property or attribute.

        :return: The number of items in the team.
        :comp best: O(1), as accessing the length of a collection is a direct operation.
        :comp worst: O(1), identical to the best case, because the complexity does not depend on the team size.
        """
        if isinstance(self.team, ArrayR):
            return self.team_count
        else: 
            return len(self.team)

    #! ===================== DUNDER: STR ===================== 
    def __str__(self):
        """
        Provides a string representation of the current team. This method formats 
        the team's contents into a readable string, showing each member and their 
        attributes.

        :return: A string representation of the team.
        :comp best: O(N), where N is self.team_count, as it iterates over each team member to construct the string.
        :comp worst: O(N * +=str), identical to the best case, since constructing the string requires iterating over each team member.
        """
        team_string = ""
        for i in range(self.team_count):
            team_string += str(self.team[i]) + '\n'
    
        return f'\nCurrent Team ({self.team_count}):\n{team_string}'



# ===================== TRAINER CLASS =====================
class Trainer:
    #! ===================== CLASS VARIABLES ===================== 
    def __init__(self, name) -> None:
        """
        Initialises a Trainer instance with a name, an empty team, an empty 
        pokedex, and a default number of lives.

        :param name: The name of the trainer.
        :complexity: O(1) for all cases, as the initialization process involves setting up a few attributes with basic values or empty data structures.
        """
        self.name = name 
        self.team = PokeTeam()
        self.pokedex = BSet()
        self.lives = 0



    #* ===================== PICK TEAM ===================== DONE
    def pick_team(self, method: str) -> None:
        """
        Allows the trainer to pick a team of Pokemon either randomly or manually
        based on the provided method.

        :param method: A string indicating the method of team selection 
            ('random' or 'manual').
        :raises ValueError: If an winvalid method string is provided.
        :comp best:
            O(t) When the method is 'manual' and choose_manually is called
            O(t * T) When the method is 'random' and choose_randomly is called
        :comp worst: 
            O(t * N * T) When the method is 'manual' and choose_manually is called 
            O(t * T) When the method is 'random' and choose_ranomly is called
        
        t for when registering Pokemon
        
        - Where t is the length of self.team
        - Where T is the length of self.TEAM_LIMIT
        - N is the number of Pokemon the user decides to choose (up to TEAM_LIMIT)
        - P is the total number of available Pokemon in POKE_LIST.
        """
        # Choosing team
        if method.lower() == 'random':
            self.team.choose_randomly()
        elif method.lower() == 'manual':
            self.team.choose_manually()
        else:
            raise ValueError('Method does not exist, choose "random" or "manual"')
        
        # Register each pokemon in our new team to the pokedex
        for i in range(len(self.team)):
            self.register_pokemon(self.team[i])

    #* ===================== REGISTER POKEMON =====================
    def register_pokemon(self, pokemon: Pokemon) -> None:
        """
        Registers a Pokemon in the trainer's pokedex. The pokedex tracks the 
        types of Pokemon seen by incrementing their PokéType value by 1 before 
        adding to ensure non-zero integers.

        :param pokemon: The Pokemon instance to register.
        :comp best: O(1), as adding to the BSet is a constant time operation.
        :comp worst: O(1), identical to the best case.
        """
        try:
            self.pokedex.add(pokemon.get_poketype().value + 1)
        except AttributeError:
            print(f'❌ Error: Pokemon type {pokemon.get_poketype()} is not recognised')

    #* ===================== GET POKEDEX COMPLETION =====================
    def get_pokedex_completion(self) -> float:
        """
        Calculates and returns the completion percentage of the pokedex based on the number of Pokemon types seen.

        :return: The completion ratio as a float.
        :comp best: O(log N), where N is the value of the internal integer storing the pokedex set elements, due to computing the length of `self.pokedex`.
        :comp worst: O(log N), indentical to the best case, due to the same reason.
        """
        # Get the total types of pokemon
        total_types = len(PokeType)
        
        # Store the types of pokemon we have seen via pokedex
        seen_types = len(self.pokedex)
        
        # Get the ratio between those two values rounded to two decimal places
        completion_ratio = round((seen_types / total_types), 2)
        
        # Return the ratio
        return completion_ratio

    #* ===================== GET TEAM =====================
    def get_team(self) -> PokeTeam:
        """
        Returns the trainer's current Pokemon team.

        :return: The PokeTeam instance associated with the trainer.
        :comp best: O(1), direct attribute access.
        :comp worst: O(1), identical to the best case.
        """
        return self.team

    #* ===================== GET NAME =====================
    def get_name(self) -> str:
        """ 
        Returns the trainer's name.

        :return: The name of the trainer as a string.
        :comp best: O(1), direct attribute access.
        :comp worst: O(1), identical to the best case.
        """
        return self.name

    #* ===================== GET LIVES =====================    
    def get_lives(self) -> int:
        """
        Returns the number of lives left for the trainer.

        :return: The number of lives as an integer.
        :comp best: O(1), direct attribute access.
        :comp worst: O(1), identical to the best case.
        """
        return self.lives

    #* ===================== SET LIVES =====================
    def set_lives(self, lives) -> None:
        """
        Sets the number of lives for the trainer to the specified value.

        :param lives: The new number of lives.
        :comp best: O(1), as it's a simple assignment operation.
        :comp worst: O(1), identical to the best case.
        """
        self.lives = lives

    #* ===================== LOSE LIFE =====================
    def lose_life(self) -> None:
        """
        Decrements the number of lives by one, indicating the trainer has lost a life.

        :comp best: O(1), as it involves a simple decrement operation.
        :comp worst: O(1), identical to the best case.
        """
        self.lives -= 1



    #! ===================== DUNDER: STR =====================
    def __str__(self) -> str:
        """
        Provides a string representation of the Trainer instance, including the name and pokedex completion percentage.

        :return: A string describing the trainer.
        :comp best: O(1), as it involves retrieving attributes and performing a simple calculation.
        :comp worst: O(1), identical to the best case.
        """
        completion_percentage = self.get_pokedex_completion() * 100
        return f'Trainer {self.name} Pokedex Completion: {int(completion_percentage)}%'



if __name__ == '__main__':
    t = Trainer('Ash')
    print(t)
    t.pick_team("random")
    print(t)
    print(t.get_team())
