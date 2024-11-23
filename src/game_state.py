import numpy as np
from .ghost import Ghost
from .constants import *

class GameState:
    def __init__(self):
        # Initialize maze layout
        self.maze = np.array([
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1],
            [1,3,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,3,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,2,1,2,1,1,1,1,1,2,1,2,1,1,2,1],
            [1,2,2,2,2,1,2,2,2,1,2,2,2,1,2,2,2,2,1],
            [1,1,1,1,2,1,1,1,0,1,0,1,1,1,2,1,1,1,1],
            [1,0,0,1,2,1,0,0,0,0,0,0,0,1,2,1,0,0,1],
            [1,1,1,1,2,1,0,1,1,0,1,1,0,1,2,1,1,1,1],
            [0,0,0,0,2,0,0,1,0,0,0,1,0,0,2,0,0,0,0],
            [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
            [1,0,0,1,2,1,0,0,0,0,0,0,0,1,2,1,0,0,1],
            [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
            [1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,2,1],
            [1,3,2,1,2,2,2,2,2,2,2,2,2,2,2,1,2,3,1],
            [1,1,2,1,2,1,2,1,1,1,1,1,2,1,2,1,2,1,1],
            [1,2,2,2,2,1,2,2,2,1,2,2,2,1,2,2,2,2,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ])
        
        # Initialize ghosts with different personalities
        self.ghosts = [
            Ghost((8, 9), 'chase'),    # Red ghost - direct chase
            Ghost((9, 9), 'ambush'),   # Pink ghost - ambush
            Ghost((10, 9), 'patrol'),  # Blue ghost - patrol
        ]
        
        # Set scatter corners for each ghost
        self.ghosts[0].set_scatter_corner((1, 1))      # Top-left
        self.ghosts[1].set_scatter_corner((1, 17))     # Top-right
        self.ghosts[2].set_scatter_corner((17, 1))     # Bottom-left
        
        # Game state variables
        self.pacman_pos = [10, 9]  # Starting position
        self.last_pacman_pos = [10, 9]
        self.lives = 3
        self.score = 0
        self.game_over = False
        self.remaining_food = self._count_food()
        self.scatter_mode = False
        self.scatter_timer = 0

    def update(self):
        """Update game state including ghost positions and check collisions."""
        # Update ghost positions
        for ghost in self.ghosts:
            dx, dy = ghost.get_next_move(self, tuple(self.pacman_pos))
            new_pos = [ghost.position[0] + dx, ghost.position[1] + dy]
            
            if self.is_valid_move(new_pos):
                ghost.position = new_pos
                
        # Check for collisions with ghosts
        self._check_ghost_collisions()
        
        # Update scatter mode
        self._update_scatter_mode()

    def _check_ghost_collisions(self):
        """Check if Pacman collides with any ghost."""
        for ghost in self.ghosts:
            if tuple(self.pacman_pos) == tuple(ghost.position):
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                else:
                    self._reset_positions()
                break

    def _reset_positions(self):
        """Reset Pacman and ghost positions after losing a life."""
        self.pacman_pos = [10, 9]
        self.last_pacman_pos = [10, 9]
        for i, ghost in enumerate(self.ghosts):
            ghost.position = [8 + i, 9]

    def _update_scatter_mode(self):
        """Toggle scatter mode periodically."""
        self.scatter_timer += 1
        if self.scatter_timer >= 600:  # Toggle every 10 seconds (60 FPS * 10)
            self.scatter_mode = not self.scatter_mode
            for ghost in self.ghosts:
                ghost.scatter_mode = self.scatter_mode
            self.scatter_timer = 0

    def get_pacman_direction(self) -> tuple:
        """Get Pacman's current direction based on last movement."""
        dx = self.pacman_pos[0] - self.last_pacman_pos[0]
        dy = self.pacman_pos[1] - self.last_pacman_pos[1]
        return (dx, dy)

    def is_valid_move(self, pos):
        """Check if the given position is a valid move."""
        x, y = pos
        return (0 <= x < len(self.maze) and 
                0 <= y < len(self.maze[0]) and 
                self.maze[x][y] != WALL)

    def update_pacman_pos(self, new_pos):
        """Update Pacman's position and track movement."""
        self.last_pacman_pos = self.pacman_pos.copy()
        self.pacman_pos = new_pos
        self.update_score(new_pos)

    def update_score(self, pos):
        """Update score based on what Pacman ate."""
        x, y = pos
        if self.maze[x][y] == FOOD:
            self.score += 10
            self.maze[x][y] = EMPTY
            self.remaining_food -= 1
        elif self.maze[x][y] == POWER_PELLET:
            self.score += 50
            self.maze[x][y] = EMPTY
            self.remaining_food -= 1

    def _count_food(self):
        """Count the total number of food pellets and power pellets in the maze."""
        return np.sum(self.maze == FOOD) + np.sum(self.maze == POWER_PELLET)