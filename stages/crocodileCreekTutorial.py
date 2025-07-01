# stages/crocodileCreekTutorial.py
import pygame
import config
from fightingLogic.fightingLogic import Player

class CrocodileCreekTutorial:
    def __init__(self, screen, player_character_name, opponent_character_name):
        self.screen = screen
        self.player_character_name = player_character_name
        self.opponent_character_name = opponent_character_name
        self.background_image = None

        self.player = None
        self.opponent = None
        self.all_sprites = pygame.sprite.Group() # Group for all game sprites

        self._load_background_image()
        self._setup_characters() # New method to set up Player objects

    def _load_background_image(self):
        # ... (same as before) ...
        try:
            self.background_image = pygame.image.load("assests/Croc_Tutorial.jpg").convert()
            self.background_image = pygame.transform.scale(self.background_image, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        except pygame.error as e:
            print(f"Error loading background image (assests/Croc_Tutorial.jpg): {e}")
            self.background_image = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            self.background_image.fill(config.GREEN)
            print("Using a green placeholder for Crocodile Creek Tutorial background.")

    def _setup_characters(self):
        """Creates Player objects for the player and opponent."""
        # Initial positions - place them on the ground level
        player_initial_x = config.SCREEN_WIDTH * 0.2
        opponent_initial_x = config.SCREEN_WIDTH * 0.8
        ground_y = config.SCREEN_HEIGHT - config.GROUND_HEIGHT

        self.player = Player(self.player_character_name, player_initial_x, ground_y, is_player_controlled=True)
        self.opponent = Player(self.opponent_character_name, opponent_initial_x, ground_y, is_player_controlled=False)

        self.all_sprites.add(self.player)
        self.all_sprites.add(self.opponent)


    def run(self):
        """
        Main loop for the Crocodile Creek Tutorial.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: # Press 'Q' to quit the stage
                        running = False
                    if self.player.is_player_controlled: # Only handle input for player
                        if event.key == pygame.K_a:
                            self.player.move(-1) # Move left (backwards)
                        elif event.key == pygame.K_s:
                            self.player.move(1)  # Move right (forwards)
                        elif event.key == pygame.K_SPACE:
                            self.player.jump()
                if event.type == pygame.KEYUP:
                    if self.player.is_player_controlled: # Only handle input for player
                        if event.key == pygame.K_a and self.player.vel_x < 0:
                            self.player.stop_move()
                        elif event.key == pygame.K_s and self.player.vel_x > 0:
                            self.player.stop_move()


            # --- Update Logic ---
            self.all_sprites.update() # Call update method for all sprites


            # --- Drawing ---
            if self.background_image:
                self.screen.blit(self.background_image, (0, 0))

            self.all_sprites.draw(self.screen) # Draw all sprites


            # Tutorial text and instructions
            font = pygame.font.Font(None, 60)
            text_surface = font.render("Welcome to Crocodile Creek Tutorial!", True, config.WHITE)
            text_rect = text_surface.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT * 0.1))
            self.screen.blit(text_surface, text_rect)

            instruction_font = pygame.font.Font(None, 40)
            instruction_surface = instruction_font.render(f"You are {self.player.character_name}. Opponent is {self.opponent.character_name}.", True, config.WHITE)
            instruction_rect = instruction_surface.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT * 0.2))
            self.screen.blit(instruction_surface, instruction_rect)

            controls_text = instruction_font.render("Controls: 'A' (back), 'S' (forward), 'Space' (jump), 'Q' (quit)", True, config.WHITE)
            controls_rect = controls_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT * 0.9))
            self.screen.blit(controls_text, controls_rect)


            pygame.display.flip()

        print("Exiting Crocodile Creek Tutorial.")

# This allows you to test CrocodileCreekTutorial directly if you run this file
if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    # Dummy config for testing (ensure it has all required constants)
    class Config:
        SCREEN_WIDTH = 1000
        SCREEN_HEIGHT = 700
        GREEN = (0, 200, 0)
        WHITE = (255, 255, 255)
        BLUE = (0, 0, 255)
        RED = (255, 0, 0)
        PLAYER_SPEED = 5
        GRAVITY = 0.8
        GROUND_HEIGHT = 50

    config = Config()

    test_screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Crocodile Creek Tutorial Test")

    tutorial_stage = CrocodileCreekTutorial(test_screen, "The Boat Man", "The Log Lady")
    tutorial_stage.run()
    pygame.quit()