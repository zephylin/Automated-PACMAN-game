from typing import Tuple, List
from .search import SearchAlgorithms
from .constants import *

class PacmanAgent:
    def __init__(self, game_state):
        self.game_state = game_state
        self.search_algorithms = SearchAlgorithms(game_state.maze)
        self.current_path = []
        self.current_target = None
        
    def get_food_positions(self) -> List[Tuple[int, int]]:
        """Get positions of all food pellets and power pellets."""
        food_positions = []
        for i in range(len(self.game_state.maze)):
            for j in range(len(self.game_state.maze[0])):
                if self.game_state.maze[i][j] in [FOOD, POWER_PELLET]:
                    food_positions.append((i, j))
        return food_positions
        
    def get_next_move(self) -> Tuple[int, int]:
        """
        Determine the next move for Pacman using A* search.
        Returns: Direction vector (dx, dy)
        """
        current_pos = tuple(self.game_state.pacman_pos)
        
        # If we have no current path or reached our target, find a new target
        if not self.current_path or current_pos == self.current_target:
            food_positions = self.get_food_positions()
            if not food_positions:
                return (0, 0)  # No food left
                
            # Find nearest food using A* search
            self.current_path, self.current_target = (
                self.search_algorithms.find_nearest_target(current_pos, food_positions)
            )
            
        # If we have a path, get the next move
        if self.current_path:
            next_pos = self.current_path[0]
            self.current_path = self.current_path[1:]
            return (next_pos[0] - current_pos[0], next_pos[1] - current_pos[1])
            
        return (0, 0)  # No valid move found