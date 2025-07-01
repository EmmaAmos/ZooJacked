# stages/crocodileCreekTutorial.py
import pygame
import config
from fightingLogic.fightingLogic import Player
from fightingLogic.winnerScreen import WinnerScreen

class CrocodileCreekTutorial:
    def __init__(self, screen, player_character_name, opponent_character_name):
        self.screen = screen
        self.player_character_name = player_character_name
        self.opponent_character_name = opponent_character_name
        self.background_image = None

        self.player = None
        self.opponent = None
        self.all_sprites = pygame.sprite.Group() 

        self._load_background_image()
        self._setup_characters()

    def _load_background_image(self):
        try:
            self.background_image = pygame.image.load("assests/Croc_Tutorial.jpg").convert()
            self.background_image = pygame.transform.scale(self.background_image, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        except pygame.error as e:
            print(f"Error loading background image (assests/Croc_Tutorial.jpg): {e}")
            self.background_image = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            self.background_image.fill(config.GREEN)
            print("Using a green placeholder for Crocodile Creek Tutorial background.")

    def _setup_characters(self):
        player_initial_x = config.SCREEN_WIDTH * 0.2
        opponent_initial_x = config.SCREEN_WIDTH * 0.8
        ground_y = config.SCREEN_HEIGHT - config.GROUND_HEIGHT

        self.player = Player(self.player_character_name, player_initial_x, ground_y, is_player_controlled=True)
        self.opponent = Player(self.opponent_character_name, opponent_initial_x, ground_y, is_player_controlled=False)

        self.all_sprites.add(self.player)
        self.all_sprites.add(self.opponent)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            # --- 1. Event Handling ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    next_game_state = "quit" # Set next state to quit
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                        next_game_state = "level_select" # Go back to level select on Q

                    if self.player.is_player_controlled:
                        if event.key == pygame.K_a:
                            self.player.move(-1)
                        elif event.key == pygame.K_s:
                            self.player.move(1)
                        elif event.key == pygame.K_SPACE:
                            self.player.jump()
                        # Keeping 'J' as a keyboard basic attack option
                        elif event.key == pygame.K_j: 
                             if self.player.last_hit_by_basic_attack == 0:
                                 self.player.attack("basic")
                        elif event.key == pygame.K_w:
                            if self.player.attack_hit_count >= self.player.MID_ATTACK_THRESHOLD:
                                self.player.attack("mid")
                        elif event.key == pygame.K_e:
                            if self.player.attack_hit_count >= self.player.SUPER_ATTACK_THRESHOLD:
                                self.player.attack("super")

                # NEW: Mouse Click Event for Player Basic Attack
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.player.is_player_controlled and event.button == 1: # Left mouse button
                        distance_to_enemy = abs(self.player.rect.centerx - self.opponent.rect.centerx)
                        if distance_to_enemy < 150: 
                            if self.player.last_hit_by_basic_attack == 0:
                                self.player.attack("basic")

                elif event.type == pygame.KEYUP:
                    if self.player.is_player_controlled:
                        if event.key == pygame.K_a and self.player.vel_x < 0:
                            self.player.stop_move()
                        elif event.key == pygame.K_s and self.player.vel_x > 0:
                            self.player.stop_move()

            # --- 2. Update Game Logic ---
            self.all_sprites.update()

            # --- 3. Enemy AI Decision ---
            ai_action = self.opponent.handle_ai(self.player.rect, self.player.is_attacking)
            if ai_action == "basic_attack":
                self.opponent.attack("basic")
            elif ai_action == "mid_attack":
                self.opponent.attack("mid")
            elif ai_action == "super_attack":
                self.opponent.attack("super")

            # --- 4. Attack Collision Detection & Damage Application (REVISED) ---
            # Player attacking opponent
            if self.player.is_attacking and not self.player.has_dealt_hit_this_attack:
                attack_range_rect = self.player.rect.inflate(50, 0)
                if attack_range_rect.colliderect(self.opponent.rect) and not self.opponent.is_attacking:
                    damage_dealt = None
                    if self.player.state == "basic":
                        damage_dealt = self.player.BASIC_ATTACK_DAMAGE
                    elif self.player.state == "mid":
                        damage_dealt = self.player.MID_ATTACK_DAMAGE
                    elif self.player.state == "super":
                        damage_dealt = self.player.SUPER_ATTACK_DAMAGE

                    if damage_dealt is not None:
                        damage_success = self.opponent.take_damage(damage_dealt)
                        if damage_success:
                            self.player.attack_hit_count += 1
                            print(f"Player hit count: {self.player.attack_hit_count}")
                            self.player.has_dealt_hit_this_attack = True

            # Opponent attacking player
            if self.opponent.is_attacking and not self.opponent.has_dealt_hit_this_attack:
                attack_range_rect = self.opponent.rect.inflate(50, 0)
                if attack_range_rect.colliderect(self.player.rect): # Removed 'and not self.player.is_attacking' here for initial test
                    if not self.player.is_attacking: # Inner check to differentiate
                        damage_dealt = None
                        if self.opponent.state == "basic":
                            damage_dealt = self.opponent.BASIC_ATTACK_DAMAGE
                        elif self.opponent.state == "mid":
                            damage_dealt = self.opponent.MID_ATTACK_DAMAGE
                        elif self.opponent.state == "super":
                            damage_dealt = self.opponent.SUPER_ATTACK_DAMAGE

                        if damage_dealt is not None:
                            damage_success = self.player.take_damage(damage_dealt)
                            if damage_success:
                                self.opponent.attack_hit_count += 1
                                print(f"DEBUG: Enemy attack collision detected and player took damage! Enemy hit count: {self.opponent.attack_hit_count}")
                                self.opponent.has_dealt_hit_this_attack = True
                            else:
                                print("DEBUG: Enemy attack hit player, but player was attacking so no damage taken.")
                    else:
                        print("DEBUG: Enemy attack collision, but player was attacking. No damage taken.")

            # --- 5. Win/Loss Condition Checks (CONSOLIDATED & CORRECTED FLOW) ---
            if self.player.health <= 0:
                print(f"{self.player.character_name} defeated! Game Over!")
                # Opponent wins
                winner_screen = WinnerScreen(self.screen, self.opponent.character_name)
                next_game_state = winner_screen.run() # Run the winner screen and get its return value
                running = False # Exit the tutorial loop
            elif self.opponent.health <= 0:
                print(f"{self.opponent.character_name} defeated! You won!")
                # Player wins
                winner_screen = WinnerScreen(self.screen, self.player.character_name)
                next_game_state = winner_screen.run() # Run the winner screen and get its return value
                running = False # Exit the tutorial loop

            # --- 6. Drawing (ONLY if game is still active) ---
            if running: # Only draw the game elements if the game loop is still active
                if self.background_image:
                    self.screen.blit(self.background_image, (0, 0))
                self.all_sprites.draw(self.screen)

                self._draw_health_bar(self.screen, self.player, (50, 20), config.BLUE)
                self._draw_health_bar(self.screen, self.opponent, (config.SCREEN_WIDTH - 250, 20), config.RED)

                font = pygame.font.Font(None, 60)
                text_surface = font.render("Welcome to Crocodile Creek Tutorial!", True, config.WHITE)
                text_rect = text_surface.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT * 0.1))
                self.screen.blit(text_surface, text_rect)

                instruction_font = pygame.font.Font(None, 40)
                instruction_surface = instruction_font.render(f"You are {self.player.character_name}. Opponent is {self.opponent.character_name}.", True, config.WHITE)
                instruction_rect = instruction_surface.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT * 0.2))
                self.screen.blit(instruction_surface, instruction_rect)

                controls_text = instruction_font.render("Controls: 'A' (left), 'S' (right), 'Mouse Click/J' (basic), 'W' (mid), 'E' (super), 'Space' (jump), 'Q' (quit)", True, config.WHITE)
                controls_rect = controls_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT * 0.9))
                self.screen.blit(controls_text, controls_rect)

                # --- 7. Update Display and Control Frame Rate ---
                pygame.display.flip()
                clock.tick(60)
        print("Exiting Crocodile Creek Tutorial.")
        return "level_select"

    def _draw_health_bar(self, screen, character, position, color):
        bar_width = 200
        bar_height = 25
        border_thickness = 3

        health_percentage = character.health / 45.0
        current_bar_width = int(bar_width * health_percentage)
        if current_bar_width < 0: # Ensure bar doesn't go negative
            current_bar_width = 0

        pygame.draw.rect(screen, config.GREY, (position[0], position[1], bar_width, bar_height), border_radius=5)
        pygame.draw.rect(screen, color, (position[0], position[1], current_bar_width, bar_height), border_radius=5)
        pygame.draw.rect(screen, config.BLACK, (position[0], position[1], bar_width, bar_height), border_thickness, border_radius=5)

        font = pygame.font.Font(None, 24)
        name_text = font.render(character.character_name, True, config.BLACK)
        screen.blit(name_text, (position[0], position[1] - 25))

        hp_text = font.render(f"{character.health}/45 HP", True, config.BLACK)
        screen.blit(hp_text, (position[0] + bar_width + 10, position[1] + (bar_height // 2) - hp_text.get_height() // 2))

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    class Config:
        SCREEN_WIDTH = 1000
        SCREEN_HEIGHT = 700
        GREEN = (0, 200, 0)
        WHITE = (255, 255, 255)
        BLUE = (0, 0, 255)
        RED = (255, 0, 0)
        BLACK = (0, 0, 0)
        GREY = (150, 150, 150)
        PLAYER_SPEED = 5
        GRAVITY = 0.8
        GROUND_HEIGHT = 50

    config = Config()

    test_screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Crocodile Creek Tutorial Test")

    tutorial_stage = CrocodileCreekTutorial(test_screen, "The Boat Man", "The Log Lady")
    tutorial_stage.run()
    pygame.quit()