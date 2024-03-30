from pokemon import *
import random
from typing import List
from data_structures.bset import BSet

class PokeTeam:
    random.seed(20)
    TEAM_LIMIT = 6

    def __init__(self):
        self.team = ArrayR(self.TEAM_LIMIT)
        self.team_size = 0

    def choose_manually(self):
        
        # ! There is a bug where if you add the same type of pokemon, the first 
        # ! index will be fine but the rest will be None
        # ! We should be able to have multiple of the same pokemon on the team
        
        pokemon_list = get_all_pokemon_types()
        
        counter = 0
        
        print('Select up to 6 Pokemon by entering their names. Type "done" to finish:')
        
        while self.team_size < PokeTeam.TEAM_LIMIT:
            user_input = input('Enter Pokemon name or "done" to finish: ').strip()
            
            if user_input.lower() == 'done':
                break
            
            found = False
            for pokemon_cls in pokemon_list:
                if user_input.capitalize() == pokemon_cls().get_name():
                    self.team[counter] = pokemon_cls()
                    self.team_size += 1
                    print(f'{pokemon_cls().get_name()} added to the team.')
                    counter += 1
                    found = True
                    break
            if not found:
                print('Invalid Pokemon name, try again.')
        
        for i in range(counter):
            print(f'Pokemon ({i}): {self.team[i]}')
            
        #print(f'Team selection complete, team: {self.team}')
                        
                    

    def choose_randomly(self) -> None:
        """ Chooses a random team of pokemon for the PokeTeam

        :complexity: O(n^2) where n is the 
        """
        
        # Print message
        print('Creating a random team of 6 pokemon')
        
        # Get all the pokemon types
        available_pokemon = get_all_pokemon_types()
        
        # Loop in range team limit (6)
        for i in range(PokeTeam.TEAM_LIMIT):
            # Get a random pokemon class 
            pokemon_cls = random.choice(available_pokemon)
            
            # Add the pokemon to the team -- O(1)
            self.team[i] = pokemon_cls()
            
            # Print out the pokemon that was added -- O(1)
            print(f'Pokemon ({i+1}): {self.team[i].get_name()}')
            
        # Update the team size
        self.team_size = PokeTeam.TEAM_LIMIT
        
        # Print message
        print('Random team Created!')

    def regenerate_team(self) -> None:
        raise NotImplementedError
    
    # ! assemble_team() will be done after task 3
    
    # ! special() will be done after task 3

    def __getitem__(self, index: int):
        if index >= self.team_size:
            raise IndexError("Team index out of range")
        return self.team[index]

    def __len__(self):
        return self.team_size

    def __str__(self):
        team_str = '\n'.join(str(self.team[i]) for i in range(self.size))
        return f'Current Team ({self.size}):\n{team_str}'

class Trainer:

    def __init__(self, name) -> None:
        self.name = name
        self.team = PokeTeam()
        self.pokedex = BSet()

    def pick_team(self, method: str) -> None:
        if method.lower() == 'random':
            self.team.choose_randomly()
        elif method.lower() == 'manual':
            self.team.choose_manually()
        else:
            raise ValueError('Method does not exist, choose "random" or "manual"')

    def get_team(self) -> PokeTeam:
        return self.team

    def get_name(self) -> str:
        return self.name

    def register_pokemon(self, pokemon: Pokemon) -> None:
        self.pokedex.add(pokemon.get_poketype().value)

    def get_pokedex_completion(self) -> float:
        total_types = len(PokeType)
        seen_types = len(self.pokedex)
        completion_ratio = round((seen_types / total_types), 2)
        return completion_ratio

    def __str__(self) -> str:
        completion_percentage = self.get_pokedex_completion() * 100
        return f'Trainer {self.name} Pokedex Completion: {int(completion_percentage)}%'

if __name__ == '__main__':
    t = Trainer('Ash')
    print(t)
    t.pick_team("manual")
    print(t)
    #print(t.get_team())