import random
from typing import Tuple, List, Dict
import math
from .constants import *

class Ghost:
    def __init__(self, position: Tuple[int, int], personality: str):
        self.position = list(position)
        self.personality = personality
        self.direction = random.choice(list(DIRECTIONS.values()))
        self.scatter_mode = False
        self.scatter_corner = None
        self.path = []
        self.is_vulnerable = False
        self.is_eaten = False
        self.movement_cooldown = 0
        self.target = None
        self.home_position = list(position)  # Remember starting position
        
    def get_legal_moves(self, game_state) -> List[Tuple[int, int]]:
        """Get list of legal moves from current position."""
        legal_moves = []
        for dx, dy in DIRECTIONS.values():
            new_x = self.position[0] + dx
            new_y = self.position[1] + dy
            if game_state.is_valid_move([new_x, new_y]):
                legal_moves.append((dx, dy))
        return legal_moves
        
    def get_next_move(self, game_state, pacman_pos: Tuple[int, int]) -> Tuple[int, int]:
        """Determine the next move based on current state."""
        # Handle movement speed based on state
        speed = self._get_current_speed()
        self.movement_cooldown += 1
        if self.movement_cooldown < speed:
            return (0, 0)
        self.movement_cooldown = 0
        
        # If eaten, return to home
        if self.is_eaten:
            return self._return_home(game_state)
            
        # If vulnerable, run away
        if self.is_vulnerable:
            return self._run_away(game_state, pacman_pos)
            
        # Normal behavior based on personality
        if self.scatter_mode:
            return self._scatter_behavior(game_state)
        
        if self.personality == 'chase':
            return self._chase_behavior(game_state, pacman_pos)
        elif self.personality == 'ambush':
            return self._ambush_behavior(game_state, pacman_pos)
        else:  # patrol
            return self._patrol_behavior(game_state, pacman_pos)
            
    def _get_current_speed(self) -> int:
        """Determine current movement speed based on ghost state."""
        if self.is_eaten:
            return GHOST_TUNNEL_SPEED
        elif self.is_vulnerable:
            return GHOST_VULNERABLE_SPEED
        else:
            return GHOST_NORMAL_SPEED
            
    def _chase_behavior(self, game_state, pacman_pos: Tuple[int, int]) -> Tuple[int, int]:
        """Aggressive chase - directly pursue Pacman."""
        return self._move_towards_target(game_state, pacman_pos)
        
    def _ambush_behavior(self, game_state, pacman_pos: Tuple[int, int]) -> Tuple[int, int]:
        """Ambush behavior - try to predict and intercept Pacman."""
        pacman_direction = game_state.get_pacman_direction()
        if pacman_direction != (0, 0):
            # Target 4 cells ahead of Pacman
            target_x = pacman_pos[0] + pacman_direction[0] * 4
            target_y = pacman_pos[1] + pacman_direction[1] * 4
            # Keep target in bounds
            target_x = max(0, min(target_x, len(game_state.maze) - 1))
            target_y = max(0, min(target_y, len(game_state.maze[0]) - 1))
            return self._move_towards_target(game_state, (target_x, target_y))
        return self._chase_behavior(game_state, pacman_pos)
        
    def _patrol_behavior(self, game_state, pacman_pos: Tuple[int, int]) -> Tuple[int, int]:
        """Patrol behavior - alternate between patrolling and chasing."""
        if self.target is None or random.random() < 0.02:  # 2% chance to change target
            # Choose a random point near Pacman
            radius = random.randint(2, 8)
            angle = random.random() * 2 * math.pi
            target_x = int(pacman_pos[0] + radius * math.cos(angle))
            target_y = int(pacman_pos[1] + radius * math.sin(angle))
            
            # Keep target in bounds
            target_x = max(0, min(target_x, len(game_state.maze) - 1))
            target_y = max(0, min(target_y, len(game_state.maze[0]) - 1))
            
            self.target = (target_x, target_y)
            
        return self._move_towards_target(game_state, self.target)
        
    def _run_away(self, game_state, pacman_pos: Tuple[int, int]) -> Tuple[int, int]:
        """Run away from Pacman when vulnerable."""
        legal_moves = self.get_legal_moves(game_state)
        if not legal_moves:
            return (0, 0)
            
        # Choose the move that maximizes distance from Pacman
        best_move = None
        max_distance = -1
        
        for dx, dy in legal_moves:
            new_x = self.position[0] + dx
            new_y = self.position[1] + dy
            distance = (new_x - pacman_pos[0])**2 + (new_y - pacman_pos[1])**2
            
            if distance > max_distance:
                max_distance = distance
                best_move = (dx, dy)
                
        return best_move if best_move else (0, 0)
    
    def _scatter_behavior(self, game_state):
        """Makes ghost retreat to its assigned corner when in scatter mode."""
        # Define scatter corners if not already assigned
        if self.scatter_corner is None:
            # Assign different corners based on ghost personality
            corners = {
                'chase': (1, 1),                    # Top-left
                'ambush': (1, len(game_state.maze[0])-2),  # Top-right
                'patrol': (len(game_state.maze)-2, 1)      # Bottom-left
            }
            self.scatter_corner = corners.get(self.personality, (1, 1))
        
        # Move towards scatter corner
        return self._move_towards_target(game_state, self.scatter_corner)
        
    def _return_home(self, game_state) -> Tuple[int, int]:
        """Return to home position when eaten."""
        return self._move_towards_target(game_state, self.home_position)
        
    def _move_towards_target(self, game_state, target: Tuple[int, int]) -> Tuple[int, int]:
        """Move towards a target position using available moves."""
        legal_moves = self.get_legal_moves(game_state)
        if not legal_moves:
            return (0, 0)
            
        # Choose the move that minimizes distance to target
        best_move = None
        min_distance = float('inf')
        
        for dx, dy in legal_moves:
            new_x = self.position[0] + dx
            new_y = self.position[1] + dy
            distance = (new_x - target[0])**2 + (new_y - target[1])**2
            
            if distance < min_distance:
                min_distance = distance
                best_move = (dx, dy)
                
        return best_move if best_move else (0, 0)
        
    def make_vulnerable(self):
        """Make ghost vulnerable after Pacman eats power pellet."""
        self.is_vulnerable = True
        self.is_eaten = False
        
    def make_normal(self):
        """Return ghost to normal state."""
        self.is_vulnerable = False
        self.is_eaten = False
        
    def get_eaten(self):
        """Mark ghost as eaten."""
        self.is_eaten = True
        self.is_vulnerable = False