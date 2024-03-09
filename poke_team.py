from pokemon import *
import random
from typing import List
from data_structures.bset import BSet

class PokeTeam:
    random.seed(20)
    TEAM_LIMIT = 6
    POKE_LIST = get_all_pokemon_types()

    def __init__(self):
        self.team = ArrayR(self.TEAM_LIMIT)
        self.team_size = 0

    def choose_manually(self):
        raise NotImplementedError

    def choose_randomly(self) -> None:
        # Print message
        print('Creating a random team of 6 pokemon')
        
        # Get all the pokemon types
        available_pokemon = get_all_pokemon_types()
        
        # Loop in range team limit (6)
        for i in range(PokeTeam.TEAM_LIMIT):
            # Get a random pokemon class 
            pokemon_cls = random.choice(available_pokemon)
            
            # Add the pokemon to the team
            self.team[i] = pokemon_cls()
            
            # Print out the pokemon that was added
            print(f'Pokemon {i}: {self.team[i].get_name()}')
            
        # Update the team size
        self.team_size = PokeTeam.TEAM_LIMIT
        
        # Print message
        print('Random team Created!')

    def regenerate_team(self) -> None:
        raise NotImplementedError

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
        if method.lower() == 'manual':
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
    t.pick_team("Random")
    print(t)
    print(t.get_team())