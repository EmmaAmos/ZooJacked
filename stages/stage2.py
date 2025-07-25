import pygame
import config # Assuming you have a config.py with SCREEN_WIDTH and SCREEN_HEIGHT

class Stage1:
    def __init__(self, screen):
        """
        Initializes Stage 1.
        :param screen: The Pygame screen surface to draw on.
        """
        self.screen = screen
        self.background_image = None
        self._load_background_image()

    def _load_background_image(self):
        """Loads the background image for Stage 1."""
        try:
            # CORRECTED PATH based on your file structure
            self.background_image = pygame.image.load("assests/Stage_2.png").convert()
            # Scale the image to fit the screen dimensions
            self.background_image = pygame.transform.scale(self.background_image, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        except pygame.error as e:
            print(f"Error loading background image (assests/Stage_2.png): {e}")
            self.background_image = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            self.background_image.fill(config.BLUE) # Use a placeholder color if image fails
            print("Using a blue placeholder for Stage 1 background.")

    def run(self):
        """
        Main loop for Stage 1. This is where the actual game logic for Stage 1 would go.
        For now, it just displays the background and waits for quit.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False # Allow quitting the stage
                # Add any stage-specific event handling here (e.g., player input)

            # --- Drawing ---
            if self.background_image:
                self.screen.blit(self.background_image, (0, 0)) # Draw the background

            # You can add other game elements here later (player, enemies, etc.)
            font = pygame.font.Font(None, 74)
            text_surface = font.render("Welcome to Stage 1!", True, config.WHITE)
            text_rect = text_surface.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
            self.screen.blit(text_surface, text_rect)

            pygame.display.flip() # Update the full display Surface to the screen

        print("Exiting Stage 1.")
        # When this method finishes, control will return to the main game loop,
        # which can then go back to the level selection map or main menu.

# This allows you to test Stage1 directly if you run this file
if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    # Dummy config for testing
    class Config:
        SCREEN_WIDTH = 1000
        SCREEN_HEIGHT = 700
        BLUE = (0, 0, 200)
        WHITE = (255, 255, 255)

    config = Config()

    test_screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Stage 1 Test")

    stage_1 = Stage1(test_screen)
    stage_1.run()
    pygame.quit()