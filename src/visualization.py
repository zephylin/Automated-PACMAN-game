import pygame
from .constants import *

class GameVisualizer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('AI PACMAN')
        self.clock = pygame.time.Clock()

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