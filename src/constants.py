# Game window settings
WINDOW_WIDTH = 570  # 19 cells * 30 pixels
WINDOW_HEIGHT = 570  # 19 cells * 30 pixels
CELL_SIZE = 30

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Game settings
FPS = 60
PACMAN_SPEED = 10
GHOST_SPEED = 1.5

# Direction vectors (dx, dy)
DIRECTIONS = {
    'RIGHT': (0, 1),
    'LEFT': (0, -1),
    'DOWN': (1, 0),
    'UP': (-1, 0)
}

# Cell types
WALL = 1
FOOD = 2
POWER_PELLET = 3
EMPTY = 0