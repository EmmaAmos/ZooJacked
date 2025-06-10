# stages/crocodileCreekTutorial.py
import pygame
import config # Assuming you'll need access to config variables

class CrocodileCreekTutorial:
    def __init__(self, screen, character_name):
        self.screen = screen
        self.character_name = character_name
        self.running = True
        self.font = pygame.font.Font(None, 50) # Use a reasonable font size
        
        # Load the background image: Stage_Boat_Tutorial.jpg
        try:
            self.background_image = pygame.image.load("assests/Stage_Boat_Tutorial.jpg").convert()
            self.background_image = pygame.transform.scale(self.background_image, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        except pygame.error as e:
            print(f"Error loading tutorial background image (Stage_Boat_Tutorial.jpg): {e}")
            self.background_image = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            self.background_image.fill(config.BLUE) # Blue placeholder if image fails
            print("Using a blue placeholder for the tutorial background.")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "quit" # Signal to main loop to quit Pygame
            # Add other stage-specific event handling (e.g., advancing tutorial text)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # Press ESC to exit tutorial for testing
                    self.running = False
                    return "level_finished"

    def update(self):
        # Update game logic for the tutorial (e.g., move tutorial elements, animations)
        pass

    def draw(self):
        # Draw the background image
        self.screen.blit(self.background_image, (0, 0))

        # Draw tutorial text
        tutorial_text = [
            f"Welcome to Crocodile Creek Tutorial, {self.character_name}!",
            "Learn to navigate the treacherous waters.",
            "Press ESC to return to the map."
        ]
        
        y_offset = 100
        for line in tutorial_text:
            text_surface = self.font.render(line, True, config.WHITE) # Use white text for contrast
            text_rect = text_surface.get_rect(center=(config.SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += 60 # Space out lines

    def run(self):
        """Main loop for the Crocodile Creek Tutorial stage."""
        clock = pygame.time.Clock()
        
        while self.running:
            result = self.handle_events()
            if result: # If handle_events returns a result (quit or level_finished)
                return result

            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(60) # Limit to 60 FPS
        
        return "level_finished" # Default return if loop ends without a specific signal

# This function will be called from main.py
def run_stage(screen, character_name):
    tutorial_stage = CrocodileCreekTutorial(screen, character_name)
    return tutorial_stage.run()