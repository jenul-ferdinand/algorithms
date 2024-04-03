import random
from battle import Battle
from battle_mode import BattleMode
from poke_team import Trainer, PokeTeam
from enum import Enum
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
from typing import Tuple

class BattleTower:
    MIN_LIVES = 1
    MAX_LIVES = 3
    BATTLE_MODE = BattleMode.ROTATE
    
    #! ===================== CLASS: INIT ===================== 
    def __init__(self) -> None:
        # The queue with all the enemy trainer teams
        self.enemy_trainer_queue    = None
        # The player trainer
        self.player_trainer         = None
        # How many enemies the player has defeated
        self.defeated_enemies_count = 0



    #* ===================== SET MY TRAINER ===================== 
    def set_my_trainer(self, trainer: Trainer) -> None:
        """ Sets the main trainer of the BattleTower
        
        :param trainer: The player's trainer to be set for the battle tower.
        :type trainer: Trainer
        :raises TypeErrror: If the provided 'trainer' is not an instance of Trainer.
        :comp best: O(1) as the method performs a constant number of operations regardless of input size.
        :comp worst: O(1) identical to the best case since the complexity does not depend on any input size or condition.
        
        Considering that isinstance is assumed to be O(1) for all future methods
        """
        if not isinstance(trainer, Trainer):
            raise TypeError(f'Expected a Trainer instance, got {type(trainer)} instead.')
        
        self.player_trainer = trainer
        self.player_trainer.set_lives(random.randint(self.MIN_LIVES, self.MAX_LIVES))

    #* ===================== GENERATE ENEMY TRAINERS ===================== 
    def generate_enemy_trainers(self, num_teams: int) -> None:
        """ 
        Generates random enemy trainers for the battle tower
        
        :param num_teams: The number of enemy trainers to generate.
        :type num_teams: int
        :raises ValueError: If 'num_teams' is not a positive integer.
        :comp best: O(N) where N is the number of teams to be generated. This scenario assumes constant time operations within each iteration of creating a team, setting lives, and assembling the team.
        :comp worst: O(N * M) where N is the number of teams and M represents the complexity of the most complex operation within the loop for a single team creation. M encapsulates the complexities of choosing a random team, setting lives, and assembling the team for battle, assuming the worst-case scenario for these operations.
        """
        if not isinstance(num_teams, int) or num_teams <= 0:
            raise ValueError('Number of teams must be a postive integer.')
        
        self.enemy_trainer_queue = CircularQueue(num_teams)
        for i in range(num_teams):
            print(f"\n=== Enemy Trainer {i+1} ===")
            enemy = Trainer(f"Enemy {i + 1}")
            enemy.pick_team('random')
            enemy.set_lives(random.randint(self.MIN_LIVES, self.MAX_LIVES))
            enemy.get_team().assemble_team(BattleMode.ROTATE)
            self.enemy_trainer_queue.append(enemy)

    #* ===================== GENERATE ENEMY TRAINERS ===================== 
    def battles_remaining(self) -> bool:
        """
        Determines if there are more battles left in the Battle Tower by checking the enemy trainers queue and the player trainer's remaining lives.

        This method checks if there are still enemy trainers waiting in the queue to battle the player and if the player's trainer still has lives left. A battle is possible only if both conditions are met.

        :return: A boolean value indicating if more battles are possible. True if battles can continue, False otherwise.
        :comp best: O(1), as checking the length of the enemy trainers queue and retrieving the player's trainer lives are direct operations.
        :comp worst: O(1), identical to the best case because the operations do not depend on the size of the queue or any other variable factors.
        """
        return len(self.enemy_trainer_queue) != 0 and self.player_trainer.get_lives() != 0

    #* ===================== GENERATE ENEMY TRAINERS =====================
    def next_battle(self) -> Tuple[Trainer, Trainer, Trainer, int, int]:
        """
        Simulates the next battle in the tower, handling the battle outcome to adjust lives accordingly.
        
        :return: The battle result, the player trainer, the enemy trainer, the player lives remaining, and the enemy lives remaining.
        :rtype: Tuple[Trainer, Trainer, Trainer, int, int]
        :comp best: O(1), assuming direct operations for serving the next enemy, regenerating teams, and appending back to the queue if the enemy still has lives.
        :comp worst: O(N * log(T) + B), where N is the number of operations involved in regenerating the team for both the player and enemy (in the worst case, this involves sorting in OPTIMISE mode, hence N * log(T)), and B is the complexity of the battle operation. The complexity of B is derived from the `commence_battle` method, which can vary based on the specific battle logic implemented (considering O(R) for rounds in SET and ROTATE modes and O(T * log(T)) for OPTIMISE mode).
        """
        
        try: 
            if self.enemy_trainer_queue.is_empty():
                raise RuntimeError("No enemy trainers left to battle.")
            
            next_enemy = self.enemy_trainer_queue.serve()
            
            player_team = self.player_trainer.get_team()
            enemy_team = next_enemy.get_team()
            
            player_team.regenerate_team(self.BATTLE_MODE)
            enemy_team.regenerate_team(self.BATTLE_MODE)
            
            battle = Battle(self.player_trainer, next_enemy, self.BATTLE_MODE)
            winner = battle.commence_battle()
            
            match winner:
                case self.player_trainer: next_enemy.lose_life(); self.defeated_enemies_count += 1
                case next_enemy: self.player_trainer.lose_life()
                
            if next_enemy.get_lives() > 0: self.enemy_trainer_queue.append(next_enemy)
                
            return (winner, self.player_trainer, next_enemy, self.player_trainer.get_lives(), next_enemy.get_lives())
        except Exception as e:
            raise RuntimeError(f"❌ Error: An error occurred during battle in tower.py: {e}")

    #* ===================== ENEMIES DEFEATES ===================== 
    def enemies_defeated(self) -> int:  
        """
        Returns the total number of enemy lives taken by the player's team.

        This method keeps track of the number of enemy trainers defeated (i.e., the total number of times an enemy trainer has lost a life to the player's team) throughout the course of the battle tower.

        :return: The total count of defeated enemy lives.
        :rtype: int
        :comp best: O(1), as it directly returns the value of a pre-calculated variable, `defeated_enemies_count`, which is incremented after each battle outcome.
        :comp worst: O(1), identical to the best case since the operation does not depend on the size of the data or any iterative computation. It simply returns the current count of defeated enemy lives.
        """
        return self.defeated_enemies_count
    
if __name__ == "__main__":
    print(f"\n=== Player Trainer ===")
    player_trainer = Trainer('Ash')
    player_trainer.pick_team("Random")
    player_trainer.get_team().assemble_team(BattleMode.ROTATE)

    bt = BattleTower()
    bt.set_my_trainer(player_trainer)
    bt.generate_enemy_trainers(4)
    bt.next_battle()
