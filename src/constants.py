# Game window settings
WINDOW_WIDTH = 570
WINDOW_HEIGHT = 570
CELL_SIZE = 30

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 182, 255)
CYAN = (0, 255, 255)
BLUE_GHOST = (33, 33, 255)  # Color for vulnerable ghosts
FLASHING_GHOST = (255, 255, 255)  # Flashing color when vulnerability ending

# Game settings
FPS = 60
PACMAN_SPEED = 10
GHOST_NORMAL_SPEED = 1.5
GHOST_VULNERABLE_SPEED = 1.0
GHOST_TUNNEL_SPEED = 0.5

# Power pellet settings
POWER_PELLET_DURATION = 600  # 10 seconds at 60 FPS
POWER_PELLET_WARNING = 180   # 3 seconds warning before ending
GHOST_POINTS = [200, 400, 800, 1600]  # Points for eating ghosts in succession

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