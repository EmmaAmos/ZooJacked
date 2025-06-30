## stages/crocodileCreekTutorial.py
import pygame
import config # Assuming you have a config.py with SCREEN_WIDTH and SCREEN_HEIGHT

class CrocodileCreekTutorial: # Make sure your class name matches this in main.py
    def __init__(self, screen):
        """
        Initializes the Crocodile Creek Tutorial stage.
        :param screen: The Pygame screen surface to draw on.
        """
        self.screen = screen
        self.background_image = None
        self._load_background_image()

    def _load_background_image(self):
        """Loads the background image for Crocodile Creek Tutorial."""
        try:
            # CORRECTED PATH based on your file structure
            # Assumes Croc_Tutorial.jpg is directly in the 'assests' folder
            self.background_image = pygame.image.load("assests/Croc_Tutorial.jpg").convert()
            # Scale the image to fit the screen dimensions
            self.background_image = pygame.transform.scale(self.background_image, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        except pygame.error as e:
            print(f"Error loading background image (assests/Croc_Tutorial.jpg): {e}")
            self.background_image = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            self.background_image.fill(config.GREEN) # Use a placeholder color if image fails
            print("Using a green placeholder for Crocodile Creek Tutorial background.")

    def run(self):
        """
        Main loop for the Crocodile Creek Tutorial.
        For now, it just displays the background and waits for quit.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False # Allow quitting the stage
                # Add any stage-specific event handling here (e.g., player input, tutorial steps)

            # --- Drawing ---
            if self.background_image:
                self.screen.blit(self.background_image, (0, 0)) # Draw the background

            # You can add tutorial text, prompts, or other elements here
            font = pygame.font.Font(None, 60)
            text_surface = font.render("Welcome to Crocodile Creek Tutorial!", True, config.WHITE)
            text_rect = text_surface.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(text_surface, text_rect)

            instruction_font = pygame.font.Font(None, 40)
            instruction_surface = instruction_font.render("Press 'Q' to quit (for now)", True, config.WHITE)
            instruction_rect = instruction_surface.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(instruction_surface, instruction_rect)


            pygame.display.flip() # Update the full display Surface to the screen

        print("Exiting Crocodile Creek Tutorial.")
        # When this method finishes, control will return to the main game loop,
        # which will then go back to the level selection map.

# This allows you to test CrocodileCreekTutorial directly if you run this file
if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    # Dummy config for testing
    class Config:
        SCREEN_WIDTH = 1000
        SCREEN_HEIGHT = 700
        GREEN = (0, 200, 0)
        WHITE = (255, 255, 255)

    config = Config()

    test_screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Crocodile Creek Tutorial Test")

    tutorial_stage = CrocodileCreekTutorial(test_screen)
    tutorial_stage.run()
    pygame.quit()