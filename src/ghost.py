import random
from typing import Tuple, List
from .search import SearchAlgorithms
from .constants import *

class Ghost:
    def __init__(self, position: Tuple[int, int], personality: str):
        """
        Initialize a ghost with a specific personality:
        - 'chase': Directly chases Pacman using A*
        - 'ambush': Tries to predict where Pacman is going
        - 'patrol': Moves in a semi-random pattern
        """
        self.position = list(position)
        self.personality = personality
        self.direction = random.choice(list(DIRECTIONS.values()))
        self.search = None  # Will be set when game_state is provided
        self.scatter_mode = False
        self.scatter_corner = None
        self.path = []
        
    def set_scatter_corner(self, corner: Tuple[int, int]):
        """Set the corner this ghost will retreat to during scatter mode."""
        self.scatter_corner = corner
        
    def get_next_move(self, game_state, pacman_pos: Tuple[int, int]) -> Tuple[int, int]:
        """Determine the next move based on ghost's personality."""
        if self.search is None:
            self.search = SearchAlgorithms(game_state.maze)
            
        if self.scatter_mode:
            return self._scatter_behavior(game_state)
            
        if self.personality == 'chase':
            return self._chase_behavior(game_state, pacman_pos)
        elif self.personality == 'ambush':
            return self._ambush_behavior(game_state, pacman_pos)
        else:  # patrol
            return self._patrol_behavior(game_state)
            
    def _chase_behavior(self, game_state, pacman_pos: Tuple[int, int]) -> Tuple[int, int]:
        """Direct chase using A* pathfinding."""
        current_pos = tuple(self.position)
        path = self.search.a_star(current_pos, tuple(pacman_pos))
        
        if path:
            next_pos = path[0]
            return (next_pos[0] - current_pos[0], next_pos[1] - current_pos[1])
        return (0, 0)
        
    def _ambush_behavior(self, game_state, pacman_pos: Tuple[int, int]) -> Tuple[int, int]:
        """Try to predict and intercept Pacman's path."""
        # Predict Pacman's direction based on recent movements
        pacman_direction = game_state.get_pacman_direction()
        if pacman_direction:
            # Aim for a point 4 cells ahead of Pacman
            target_x = pacman_pos[0] + pacman_direction[0] * 4
            target_y = pacman_pos[1] + pacman_direction[1] * 4
            
            # Keep target within maze bounds
            target_x = max(0, min(target_x, len(game_state.maze) - 1))
            target_y = max(0, min(target_y, len(game_state.maze[0]) - 1))
            
            # If target is wall, find nearest non-wall position
            if game_state.maze[target_x][target_y] == WALL:
                for dx, dy in DIRECTIONS.values():
                    new_x, new_y = target_x + dx, target_y + dy
                    if (0 <= new_x < len(game_state.maze) and 
                        0 <= new_y < len(game_state.maze[0]) and 
                        game_state.maze[new_x][new_y] != WALL):
                        target_x, target_y = new_x, new_y
                        break
            
            path = self.search.a_star(tuple(self.position), (target_x, target_y))
            if path:
                next_pos = path[0]
                return (next_pos[0] - self.position[0], next_pos[1] - self.position[1])
                
        return self._chase_behavior(game_state, pacman_pos)
        
    def _patrol_behavior(self, game_state) -> Tuple[int, int]:
        """Move in a semi-random pattern."""
        if not self.path:
            # Generate new patrol path
            current_pos = tuple(self.position)
            patrol_points = self._get_patrol_points(game_state)
            target = random.choice(patrol_points)
            self.path = self.search.a_star(current_pos, target)
            
        if self.path:
            next_pos = self.path[0]
            self.path = self.path[1:]
            return (next_pos[0] - self.position[0], next_pos[1] - self.position[1])
            
        return (0, 0)
        
    def _scatter_behavior(self, game_state) -> Tuple[int, int]:
        """Retreat to designated corner during scatter mode."""
        if self.scatter_corner:
            path = self.search.a_star(tuple(self.position), self.scatter_corner)
            if path:
                next_pos = path[0]
                return (next_pos[0] - self.position[0], next_pos[1] - self.position[1])
        return (0, 0)
        
    def _get_patrol_points(self, game_state) -> List[Tuple[int, int]]:
        """Get list of potential patrol points (intersections and corners)."""
        patrol_points = []
        for i in range(1, len(game_state.maze) - 1):
            for j in range(1, len(game_state.maze[0]) - 1):
                if game_state.maze[i][j] != WALL:
                    # Count number of non-wall neighbors
                    valid_neighbors = sum(1 for dx, dy in DIRECTIONS.values()
                                       if game_state.maze[i + dx][j + dy] != WALL)
                    # Add points that are intersections (3+ valid directions)
                    if valid_neighbors >= 3:
                        patrol_points.append((i, j))
                        
        return patrol_points