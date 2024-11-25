import pygame
import time
from src.game_state import GameState
from src.visualization import GameVisualizer
from src.pacman_agent import PacmanAgent
from src.constants import *

def show_game_over_screen(visualizer, score, is_win=True):
    """Show end game screen with score and options to restart or quit."""
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    
    # Game over/win message
    message = "YOU WIN!" if is_win else "GAME OVER"
    text = font.render(message, True, YELLOW)
    score_text = small_font.render(f"Final Score: {score}", True, WHITE)
    restart_text = small_font.render("Press SPACE to restart or ESC to quit", True, WHITE)
    
    # Center the text
    text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 50))
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 20))
    restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 70))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_SPACE:
                    return True
        
        # Draw end game screen
        visualizer.screen.fill(BLACK)
        visualizer.screen.blit(text, text_rect)
        visualizer.screen.blit(score_text, score_rect)
        visualizer.screen.blit(restart_text, restart_rect)
        pygame.display.flip()

def main():
    running = True
    
    while running:
        # Initialize game state, visualizer, and agent
        game_state = GameState()
        visualizer = GameVisualizer()
        pacman_agent = PacmanAgent(game_state)
        game_running = True
        last_move_time = time.time()

        while game_running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_running = False
                        running = False
                    elif event.key == pygame.K_p:  # Add pause functionality
                        time.sleep(0.5)

            # Update PACMAN position based on AI agent's decision
            current_time = time.time()
            if current_time - last_move_time >= 1/PACMAN_SPEED:
                # Get next move from AI agent
                dx, dy = pacman_agent.get_next_move()
                new_pos = [game_state.pacman_pos[0] + dx, game_state.pacman_pos[1] + dy]
                
                if game_state.is_valid_move(new_pos):
                    game_state.update_pacman_pos(new_pos)
                
                # Update ghost positions and check collisions
                game_state.update()
                last_move_time = current_time

            # Check game over conditions
            if game_state.game_over:
                game_running = False
            elif game_state.remaining_food == 0:
                game_running = False

            # Draw current game state
            visualizer.draw_maze(game_state.maze)
            visualizer.draw_pacman(game_state.pacman_pos)
            for ghost in game_state.ghosts:
                visualizer.draw_ghost(ghost)
            visualizer.draw_score(game_state.score)
            visualizer.draw_lives(game_state.lives)
            visualizer.update_display()

        # Show end game screen and check if player wants to restart
        if running:  # Only show if not closed with ESC or window X
            is_win = game_state.remaining_food == 0
            running = show_game_over_screen(visualizer, game_state.score, is_win=is_win)

    pygame.quit()

if __name__ == "__main__":
    main()