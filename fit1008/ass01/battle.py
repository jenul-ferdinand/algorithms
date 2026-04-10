from __future__ import annotations
from enum import Enum
from math import ceil
from typing import Tuple

from fit1008.ass01.battle_mode import BattleMode
from fit1008.ass01.data_structures.sorted_list_adt import ListItem
from fit1008.ass01.poke_team import Trainer, PokeTeam
from fit1008.ass01.pokemon_base import Pokemon

# Placeholder object for indeterminate outcome of a battle
INDETERMINATE = object()

class Battle:
    #! ===================== CLASS: INITIALISE =====================
    def __init__(self, trainer_1: Trainer, trainer_2: Trainer, battle_mode: BattleMode, criterion = "speed") -> None:
        # First trainer
        self.trainer1       = trainer_1
        # Second trainer
        self.trainer2       = trainer_2
        # The type of battle
        self.battle_mode    = battle_mode
        # The criterion for sorting
        self.criterion      = criterion
    
    
    
    #? ===================== INTERNAL: BATTLE ROUND =====================
    def _battle(self, pokemon1: Pokemon, pokemon2: Pokemon) -> Pokemon | None:
        """
        One round of battle between two Pokemon
        
        :return: The winning Pokemon of that round or None if it is a draw or 
                 INDETERMINATE
        :post: 
        :comp best: O(1) assuming a quick resolution based on speed and damage dealt
        :comp worst: O(R) where R represents the rounds needed to find a winner or conclude a draw
        """
        p1 = pokemon1
        p2 = pokemon2
        
        while p1.health > 0 and p2.health > 0:
            # Calculate and store the speed difference
            speed_difference = (p1.speed > p2.speed) - (p1.speed < p2.speed)
            
            # The damage from each pokemon with pokedex completion multiplier
            p1_attack_damage = self._attack(p1, p2, self.trainer1, self.trainer2)
            p2_attack_damage = self._attack(p2, p1, self.trainer2, self.trainer1)
            
            match speed_difference:
                case 1: # Pokemon 1 IS FASTER
                    p2.defend(p1_attack_damage)
                    if p2.health <= 0: 
                        break 

                    p1.defend(p2_attack_damage)
                    if p1.health <= 0:
                        break 
                case -1: # Pokemon 1 IS SLOWER
                    p1.defend(p2_attack_damage)
                    if p1.health <= 0:
                        break

                    p2.defend(p1_attack_damage)
                    if p2.health <= 0:
                        break 
                case 0: # SPEED SAME
                    p1.defend(p2_attack_damage)
                    p2.defend(p1_attack_damage)
                    if p1.health <= 0 or p2.health <= 0:
                        break
            
            if p1.health > 0 and p2.health > 0:
                print(f'🖤 {p1.get_name()} and {p2.get_name()} both lose 1 HP')
                
                p1.health -= 1
                p2.health -= 1
            
            if p1.health > 0 and p2.health > 0:
                print(f'\nINDETERMINATE\n')
                
                return INDETERMINATE
            
        if p1.health > 0:
            print(f'\n🏆 {p1.get_name()} wins!\n')
            
            p1.level_up()
            
            return p1
        
        elif p2.health > 0:
            print(f'\n🏆 {p2.get_name()} wins!\n')
            
            p2.level_up()
            return p2
        
        elif p2.health <= 0 and p1.health <= 0:
            print(f"\n💢 It's a draw!\n")
            
            return None
    
    #? ===================== INTERNAL: ATTACK ===================== 
    def _attack(self, attacker: Pokemon, defender: Pokemon, attacker_trainer: Trainer, defender_trainer: Trainer) -> float:
        """
        Computes the damage based on the attacker and defender's pokedex completion
        
        :param attacker: The attacking pokemon
        :param defender: the defending pokemon
        :param attacker_trainer: The attacking pokemon's trainer
        :param defender_trainer: The defending pokemon's trainer
        :return float: The upper damage multiplied by multiplier
        :comp best: O(1)
        :comp worst: O(E^2) when get_effectiveness' EFFECT_TABLE has NOT been populated, where E is the number of types. This originates from the attack() method
        """
        damage = attacker.attack(defender)
        attack_damage_multiplier = \
            attacker_trainer.get_pokedex_completion() / defender_trainer.get_pokedex_completion()
        return ceil(damage * attack_damage_multiplier)
    
    #? ===================== INTERNAL: CHOOSE WINNING TEAM =====================
    def _choose_winning_team(self, team1, team2) -> PokeTeam:
        """
        Chooses the winning team based on emptyness

        :return PokeTeam: The winning team or None if draw
        :comp best: O(1) 
        :comp worst: O(1)
        """
        if team1.is_empty() and team2.is_empty():
            return None
        elif team2.is_empty():
            return self.trainer1.get_team()
        elif team1.is_empty():
            return self.trainer2.get_team()

    #? ===================== INTERNAL: CREATE TEAMS =====================
    def _create_teams(self) -> None:
        """
        Initialises both trainers' teams for the battle by picking teams randomly and then organising the teams according to the selected battle mode.
        
        If the battle mode is OPTIMISE, the teams are sorted based on a specified criterion (e.g., 'health', 'speed'). For other battle modes (SET or ROTATE), teams are assembled using the approapriate data structure to fit the mode's requirements without sorting.
        
        :return: None
        :post: Trainer's teams are initialised and organised based on the battle mode. For OPTIMISE mode, teams are sorted by the specified criterion. For SET and ROTATE modes, teams are prepared using stacks and queues, respectively.
        :comp best: O(T) for SET and ROTATE modes where T is the TEAM_LIMIT, as it involves simple team assembly. For OPTIMISE mode, it's O(T * log(T)) due to sorting operations.
        :comp worst: O(T * log(T)) for OPTIMISE mode, due to the sorting of teams. For SET and ROTATE modes, complexity remains O(T), as the operation does not depend on the sorting but on the team assembly process.
        """
        self.trainer1.pick_team('random')
        self.trainer2.pick_team('random')
        
        match self.battle_mode:
            case BattleMode.OPTIMISE:
                self.trainer1.team.assign_team(self.criterion)
                self.trainer2.team.assign_team(self.criterion)
            case BattleMode.SET | BattleMode.ROTATE:
                self.trainer1.team.assemble_team(self.battle_mode)
                self.trainer2.team.assemble_team(self.battle_mode)
            case _:
                raise ValueError(f'Unsupported battle mode: {self.battle_mode}')

    #? ===================== INTERNAL: TRADE POKEDEX ENTRIES BETWEEN TRAINERS ===================== 
    def _trade_pokedex_entries_between_trainers(self, pokemon1: Pokemon, pokemon2: Pokemon) -> None:
        """
        Updates each trainer's Pokedex with the type of the Pokemon encountered during the battle. This method ensures that both trainer's Pokedex are updated by adding the encountered Pokemon type, facilitating the tracking of Pokemon types each trainer has come across.
        
        :param p1: The Pokemon instance from the first trainer involved in the exchange.
        :param p2: The Pokemon instance from the second trainer involved in the exchange.
        :return: None
        :raises TypeError: If either `pokemon1` or `pokemon2` is not an instance of a Pokemon
        :raises AttributeError: If either `pokemon1` or `pokemon2` lacks a required attribute
        :post: The Pokedex of each trainer is updated with the Pokemon types encountered.
        :comp best: O(1) as updating the Pokedex involves a constant time operation for adding the Pokemon type to each trainer's Pokedex.
        :comp worst: O(1) same as the best case, given the constant time complexity of the `register pokemon` method.
        
        Considering that isinstance is assumed to be O(1) for all future methods
        """
        if not isinstance(pokemon1, Pokemon) or not isinstance(pokemon2, Pokemon):
            raise TypeError('pokemon1 and pokemon2 must be instances of Pokemon')
        
        if not hasattr(pokemon1, 'get_poketype') and hasattr(pokemon2, 'get_poketype'):
            raise AttributeError('Both pokemon1 and pokemon2 must have a `get_poketype` method')
        
        try:
            self.trainer2.register_pokemon(pokemon1)
            self.trainer1.register_pokemon(pokemon2)
        except Exception as e:
            print(f'❌ Error: _trade_pokedex_entries_between_trainers could not register Pokemon to Trainers Pokedex ({e})')
    
    #? ===================== INTERNAL: PRINT BATTLE HEADER =====================
    def _print_battle_header(self, battle_round: int) -> int:
        """
        Prints the battle round header
        
        :return: The battle round integer
        :comp best: O(1)
        :comp worst: O(1)
        """
        battle_round += 1
        print(f"=== BATTLE ROUND {battle_round} ({self.trainer1.get_name()} vs {self.trainer2.get_name()}) ===")
        return battle_round
    
    
    
    #* ===================== COMMENCH BATTLE =====================
    def commence_battle(self) -> Trainer | None:
        """
        Initiates the battle between two trainers' teams based on the battle mode selected. The method delegates
        to the specific battle method (`set_battle`, `rotate_battle`, or `optimise_battle`) based on the battle mode,
        and determines the winning trainer or a draw if applicable.

        :return: The winning trainer, or None if the battle ends in a draw.
        :comp best: Corresponds to the best case complexity of the invoked battle mode method. O(T) for SET and ROTATE modes, where T is the TEAM_LIMIT, and O(T * log(T)) for OPTIMISE mode due to sorting operations.
        :comp worst: Aligns with the worst case complexity of the specific battle mode method invoked. O(N * log(T)) for OPTIMISE mode, where N is the total number of Pokemon across both teams and T is the TEAM_LIMIT, considering sorting operations. O(R) for SET and ROTATE modes, where R is the number of rounds, due to the linear progression of battles.
        """
        # Determine the battle's outcome based on the battle mode
        outcome = None
        match self.battle_mode:
            case BattleMode.SET: outcome = self.set_battle()
            case BattleMode.ROTATE: outcome = self.rotate_battle()
            case BattleMode.OPTIMISE: outcome = self.optimise_battle()
            case _: raise ValueError("I need sleep")
        
        # Identify and return the winning trainer
        if outcome == self.trainer1.get_team(): victor = self.trainer1
        elif outcome == self.trainer2.get_team(): victor = self.trainer2
        else: victor = None
        
        # Printing winner
        if victor is not None: 
            print(f"=============================================== {victor.get_name()} won the battle! =============================================== \n")
        else: 
            print(f"=============================================== It's a draw! =============================================== \n")

        # Return the winning Trainer
        return victor  
    
    #* ===================== SET BATTLE =====================
    def set_battle(self) -> PokeTeam | None:
        """
        Conducts a 'King of the hill' style battle between two teams where each team competes in successive ruonds until one team is left without any Pokemon.
        
        Each round involves:
        - Popping one Pokemon from each team for a battle round.
        - Trading Pokedex entries between trainers based on the encountered Pokemon.
        - Determining the round's winner and pushing the winning Pokemon back onto its team.
        
        The battle continues until one or both teams have no more Pokemon, at which point the winning team is determined or a draw is declared.
        
        :return: The winning PokeTeam or None in case of a draw.
        :comp best: O(B) where B is the minimum number of battle rounds needed for a team to run out of Pokemon, assuming quick resolutions in `_battle_round`.
        :comp worst: O(N) where N is the total number of Pokemon across both teams, representing the scenario where each round conclusivey eliminates one Pokemon until one team is depleted.
        """
        
        # Get the teams
        team1 = self.trainer1.get_team().team; team2 = self.trainer2.get_team().team
        
        # Battle round for printing
        battle_round = 0
        
        # Loop while both teams are not empty
        while not team1.is_empty() and not team2.is_empty():
            # Print battle round header
            battle_round = self._print_battle_header(battle_round)
            
            # Pop the two pokemon and register them
            p1 = team1.pop(); p2 = team2.pop(); self._trade_pokedex_entries_between_trainers(p1, p2)
            
            # Get the winner of the battle
            victor = self._battle(p1, p2)
            
            # Push the winners back to the team
            if victor == p1: team1.push(p1)
            elif victor == p2: team2.push(p2)
            elif victor == INDETERMINATE: team1.push(p1); team2.push(p2)
        
        # Return teh winning team
        return self._choose_winning_team(team1, team2)
                
    #* ===================== ROTATE BATTLE =====================
    def rotate_battle(self) -> PokeTeam | None:
        """
        Conducts a battle between two teams in ROTATE mode, where each team's front Pokemon face off in each round, and the victor is rotated back to the end of the team. This process repeats until one team runs out of Pokemon.
        
        Each round involves:
        - Serving the front Pokemon from each team for a battle round
        - Trading Pokedex entries between trainers based on the encountered Pokemon.
        - Determining the round's winner and appending the winning Pokemon back to the end of its team.
        
        The battle continues until one or both teams have no more Pokemon, at which point the winning team is declared or a draw is declared.
        
        :return: The winning PokeTeam or None in case of a draw.
        :comp best: O(B), where B is the minimum number of battle rounds needed for a team to run out of Pokemon, assuming quick resolutions in `_battle_round`.
        :comp worst: O(N), where N is the total number of Pokemon across both teams, representing the scenario where each round conclusively eliminates one Pokemon until one team is depleted.
        """
        
        # Get both trainers teams
        team1 = self.trainer1.get_team().team; team2 = self.trainer2.get_team().team
        
        # Battle round for printing
        battle_round = 0
        
        # Loop while both teams are not empty
        while not team1.is_empty() and not team2.is_empty():
            # Print battle round header
            battle_round = self._print_battle_header(battle_round)
            
            # Serve each trainers pokemon and register them between trainers
            p1 = team1.serve(); p2 = team2.serve(); self._trade_pokedex_entries_between_trainers(p1, p2)
            
            # Get the winner of the battle
            victor = self._battle(p1, p2)
            
            # Append the winners back to the team
            if victor == p1: team1.append(p1)
            elif victor == p2: team2.append(p2)
            elif victor == INDETERMINATE: team1.append(p1); team2.append(p2)
        
        # Return the winning team
        return self._choose_winning_team(team1, team2)
    
    #* ===================== OPTIMISE BATTLE ===================== 
    def optimise_battle(self) -> PokeTeam | None:
        """
        Conducts a battle between two teams in OPTIMISE mode, where teams are initially sorted
        based on a specified criterion (e.g., 'health', 'speed'). Each round, the top Pokemon
        from each team (based on the sorting criterion) face off until one team is depleted.

        Each round involves:
        - Removing the top Pokemon from each team for a battle round based on the sorting criterion.
        - Trading Pokedex entries between trainers based on the encountered Pokemon.
        - Determining the round's winner and adding the winning Pokemon back into its team in a sorted manner.

        The battle continues until one or both teams have no more Pokemon, at which point the winning team is determined or a draw is declared.
        
        :return: The winning PokeTeam or None in case of a draw.
        :comp best: O(B * log(T)) where B is the number of battle rounds and T is the TEAM_LIMIT. The logarithmic factor arises from the sorting requirement when adding Pokemon back into the team.
        :comp worst: O(N * log(T)), where N is the total number of Pokemon across both teams and T is the TEAM_LIMIT. This represents the scenario where every battle round results in sorting operations due to Pokemon being added back to their respective teams.
        """
        # Get the teams bruh
        team1 = self.trainer1.get_team().team; team2 = self.trainer2.get_team().team
        
        battle_round = 0
        # Loop while both teams are not empty
        while not team1.is_empty() and not team2.is_empty():
            battle_round = self._print_battle_header(battle_round)
            
            # Delete and get the Pokemon from the first index
            p1 = team1.delete_at_index(0).value; p2 = team2.delete_at_index(0).value
            
            # Register the new Pokemon for both the trainers
            self._trade_pokedex_entries_between_trainers(p1, p2)
            
            # Get the winner of the battle
            victor = self._battle(p1, p2)

            # Add the winner back to the team
            if victor == p1: team1.add(ListItem(p1, (getattr(p1, self.criterion))))
            elif victor == p2: team2.add(ListItem(p2, (getattr(p2, self.criterion))))
            elif victor == INDETERMINATE:
                team1.add(ListItem(p1, (getattr(p1, self.criterion))))
                team2.add(ListItem(p2, (getattr(p2, self.criterion))))
                
        return self._choose_winning_team(team1, team2)



if __name__ == '__main__':
    t1 = Trainer('Ash')
    t2 = Trainer('Gary')
    b = Battle(t1, t2, BattleMode.SET)
    b._create_teams()
    winner = b.commence_battle()

    if winner is None:
        print("Its a draw")
    else:
        print(f"The winner is {winner.get_name()}")
