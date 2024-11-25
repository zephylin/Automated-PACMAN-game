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
        
    def calculate_danger(self, pos: Tuple[int, int]) -> float:
        """Calculate danger level at a position based on ghost positions."""
        danger = 0
        for ghost in self.game_state.ghosts:
            distance = abs(pos[0] - ghost.position[0]) + abs(pos[1] - ghost.position[1])
            # Reduced danger values to prevent getting stuck
            if distance < 2:
                danger += 1.0
            elif distance < 3:
                danger += 0.5
        return danger
        
    def get_next_move(self) -> Tuple[int, int]:
        """Determine next move considering both food and ghost positions."""
        current_pos = tuple(self.game_state.pacman_pos)
        
        # If we need a new path
        if not self.current_path or current_pos == self.current_target:
            food_positions = self.get_food_positions()
            if not food_positions:
                return (0, 0)  # No food left
                
            # Find best target considering both distance and safety
            best_target = None
            best_score = float('inf')
            best_path = []
            
            for food in food_positions:
                dist = self.search_algorithms.manhattan_distance(current_pos, food)
                danger = self.calculate_danger(food)
                
                # Balance between distance and danger
                score = dist + danger
                
                if score < best_score:
                    path = self.search_algorithms.a_star(current_pos, food)
                    if path:
                        best_score = score
                        best_path = path
                        best_target = food
            
            if best_path:
                self.current_path = best_path
                self.current_target = best_target
        
        # Get next move from current path
        if self.current_path:
            next_pos = self.current_path[0]
            self.current_path = self.current_path[1:]
            return (next_pos[0] - current_pos[0], next_pos[1] - current_pos[1])
            
        return (0, 0)  # No valid move found