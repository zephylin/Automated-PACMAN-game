import pygame
from typing import List, Tuple
from .constants import *

class GameVisualizer:
    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('AI PACMAN')
        self.clock = pygame.time.Clock()
        self.game_state = None  # Add this line

    def set_game_state(self, game_state):
        """Set the current game state for visualization."""
        self.game_state = game_state

    def draw_maze(self, maze):
        """Draw the maze with walls, food pellets, and power pellets."""
        self.screen.fill(BLACK)
        
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                x = j * CELL_SIZE
                y = i * CELL_SIZE
                cell = maze[i][j]
                
                if cell == WALL:
                    # Draw wall
                    pygame.draw.rect(self.screen, BLUE, 
                                   (x, y, CELL_SIZE, CELL_SIZE))
                elif cell == FOOD:
                    # Draw food pellet
                    pygame.draw.circle(self.screen, WHITE,
                                     (x + CELL_SIZE//2, y + CELL_SIZE//2), 3)
                elif cell == POWER_PELLET:
                    # Draw power pellet
                    pygame.draw.circle(self.screen, WHITE,
                                     (x + CELL_SIZE//2, y + CELL_SIZE//2), 7)

    def draw_pacman(self, pos):
        """Draw PACMAN at the given position."""
        x = pos[1] * CELL_SIZE + CELL_SIZE//2
        y = pos[0] * CELL_SIZE + CELL_SIZE//2
        pygame.draw.circle(self.screen, YELLOW,
                         (x, y), CELL_SIZE//2 - 2)

    def draw_ghost(self, ghost):
        """Draw a single ghost."""
        x = ghost.position[1] * CELL_SIZE + CELL_SIZE//2
        y = ghost.position[0] * CELL_SIZE + CELL_SIZE//2
        
        # Different colors for different ghost personalities
        color = {
            'chase': RED,
            'ambush': (255, 182, 255),  # Pink
            'patrol': (0, 255, 255)      # Cyan
        }.get(ghost.personality, RED)
        
        # Draw ghost body
        pygame.draw.circle(self.screen, color,
                         (x, y), CELL_SIZE//2 - 2)

    def draw_lives(self, lives):
        """Draw remaining lives."""
        for i in range(lives):
            x = i * (CELL_SIZE + 5) + 10
            y = WINDOW_HEIGHT - 25
            pygame.draw.circle(self.screen, YELLOW,
                             (x, y), CELL_SIZE//3)

    def draw_score(self, score):
        """Draw the current score."""
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, WHITE)
        self.screen.blit(score_text, (WINDOW_WIDTH - 150, WINDOW_HEIGHT - 30))

    def draw_path_exploration(self, explored_nodes: List[Tuple[int, int]], final_path: List[Tuple[int, int]], algorithm_name: str):
        """Visualize how different algorithms explore paths."""
        # Colors for different algorithms
        colors = {
            'BFS': (100, 100, 255),  # Light blue for BFS exploration
            'DFS': (255, 100, 100),  # Light red for DFS exploration
            'A*': (100, 255, 100)    # Light green for A* exploration
        }
        
        # Draw all explored nodes with small circles
        color = colors.get(algorithm_name, (255, 255, 255))  # Default to white if algorithm not found
        for node in explored_nodes:
            x = node[1] * CELL_SIZE + CELL_SIZE//2
            y = node[0] * CELL_SIZE + CELL_SIZE//2
            pygame.draw.circle(self.screen, color, (x, y), 2)  # Small dots for explored nodes
        
        # Draw final path with lines if it exists
        if final_path:
            # Start from Pacman's position
            start_pos = self.game_state.pacman_pos
            path_with_start = [start_pos] + final_path
            
            for i in range(len(path_with_start) - 1):
                start_x = path_with_start[i][1] * CELL_SIZE + CELL_SIZE//2
                start_y = path_with_start[i][0] * CELL_SIZE + CELL_SIZE//2
                end_x = path_with_start[i+1][1] * CELL_SIZE + CELL_SIZE//2
                end_y = path_with_start[i+1][0] * CELL_SIZE + CELL_SIZE//2
                pygame.draw.line(self.screen, YELLOW, (start_x, start_y), (end_x, end_y), 2)
        
        # Draw algorithm name
        font = pygame.font.Font(None, 24)
        text = font.render(f'Algorithm: {algorithm_name}', True, WHITE)
        self.screen.blit(text, (10, WINDOW_HEIGHT - 30))

    def update_display(self):
        """Update the display."""
        pygame.display.flip()
        self.clock.tick(FPS)

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, value):
        self._screen = value