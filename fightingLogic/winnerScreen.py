# fightingLogic/winnerScreen.py

import pygame
import config # Ensure your config.py has colors like WHITE, BLACK, BLUE, RED

class WinnerScreen:
    def __init__(self, screen, winner_name):
        """
        Initializes the Winner Screen.

        Args:
            screen (pygame.Surface): The main display surface.
            winner_name (str): The name of the character who won the stage.
        """
        self.screen = screen
        self.winner_name = winner_name
        self.font_large = pygame.font.Font(None, 100) # Font for winner message
        self.font_medium = pygame.font.Font(None, 50) # Font for instructions

        # Determine winner specific color for emphasis (optional)
        self.winner_color = config.BLUE if "Boat Man" in self.winner_name else config.RED # Example based on character names

    def run(self):
        """
        Runs the game loop for the Winner Screen.
        Displays the winner and waits for user input to proceed.
        Returns the next game state (e.g., "level_select").
        """
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Allow quitting directly from winner screen
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    # Any key press will move to the next state
                    running = False

            # Drawing
            self.screen.fill(config.BLACK) # Black background for the winner screen

            # Winner Message
            winner_text = f"{self.winner_name} Wins!"
            winner_surface = self.font_large.render(winner_text, True, self.winner_color)
            winner_rect = winner_surface.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(winner_surface, winner_rect)

            # Instruction Message
            instruction_text = "Press any key to continue..."
            instruction_surface = self.font_medium.render(instruction_text, True, config.WHITE)
            instruction_rect = instruction_surface.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(instruction_surface, instruction_rect)

            pygame.display.flip()
            clock.tick(60) # Cap frame rate

        return "level_select" # Return to level selection after the screen