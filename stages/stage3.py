#stages/stage3.py
import pygame
import config
from fightingLogic.fightingLogic import Player, draw_controls_overlay 
from fightingLogic.winnerScreen import WinnerScreen

class Stage1:
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
            # Matches your folder spelling: "assests"
            self.background_image = pygame.image.load("assests/Stage_3.webp").convert()
            self.background_image = pygame.transform.scale(self.background_image, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        except pygame.error as e:
            print(f"Error loading background image (assests/Stage_1.png): {e}")
            self.background_image = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            self.background_image.fill(config.GREEN)

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
        
        # --- TIMER SETUP ---
        countdown_seconds = 10
        start_ticks = pygame.time.get_ticks() 
        
        waiting_to_start = True
        running = True
        next_game_state = "level_select"

        while running:
            # 1. Timer Logic
            if waiting_to_start:
                seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
                current_timer = max(0, countdown_seconds - seconds_passed)
                if current_timer <= 0:
                    waiting_to_start = False

            # 2. Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                # Gameplay inputs are locked until the countdown finishes
                if not waiting_to_start:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            running = False
                        
                        if self.player.is_player_controlled:
                            # Movement
                            if event.key == pygame.K_a: self.player.move(-1)
                            elif event.key == pygame.K_s: self.player.move(1)
                            elif event.key == pygame.K_SPACE: self.player.jump()
                            
                            # Keyboard Attacks
                            elif event.key == pygame.K_j: self.player.attack("basic")
                            elif event.key == pygame.K_w:
                                if self.player.attack_hit_count >= self.player.MID_ATTACK_THRESHOLD:
                                    self.player.attack("mid")
                            elif event.key == pygame.K_e:
                                if self.player.attack_hit_count >= self.player.SUPER_ATTACK_THRESHOLD:
                                    self.player.attack("super")

                    # Mouse Attack
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.player.is_player_controlled:
                            self.player.attack("basic")

                    # Stop Movement
                    elif event.type == pygame.KEYUP:
                        if self.player.is_player_controlled:
                            if event.key in [pygame.K_a, pygame.K_s]:
                                self.player.stop_move()

            # 3. Game Logic Update (Only runs after countdown)
            if not waiting_to_start:
                self.all_sprites.update()
                
                # Enemy AI Decision
                ai_action = self.opponent.handle_ai(self.player.rect, self.player.is_attacking)
                if ai_action:
                    # Normalizing "basic_attack" to "basic"
                    self.opponent.attack(ai_action.replace("_attack", ""))

                self._check_collisions()

                # Win/Loss Check
                if self.player.health <= 0 or self.opponent.health <= 0:
                    winner = self.player.character_name if self.opponent.health <= 0 else self.opponent.character_name
                    winner_screen = WinnerScreen(self.screen, winner)
                    return winner_screen.run()

            # 4. Drawing
            if self.background_image:
                self.screen.blit(self.background_image, (0, 0))
            
            self.all_sprites.draw(self.screen)
            
            # Draw UI Elements
            self._draw_health_bar(self.screen, self.player, (50, 40), config.BLUE)
            self._draw_health_bar(self.screen, self.opponent, (config.SCREEN_WIDTH - 250, 40), config.RED)

            # Draw Overlays (Timer and Controls)
            if waiting_to_start:
                self._draw_countdown_overlay(current_timer)
                draw_controls_overlay(self.screen) # Now shows during the countdown

            pygame.display.flip()
            clock.tick(60)

        return next_game_state

    def _check_collisions(self):
        """Calculates hit detection for both characters."""
        # Player attacking opponent
        if self.player.is_attacking and not self.player.has_dealt_hit_this_attack:
            attack_rect = self.player.rect.inflate(60, 0)
            if attack_rect.colliderect(self.opponent.rect) and not self.opponent.is_attacking:
                # Dynamically get damage based on state (BASIC, MID, SUPER)
                damage_attr = f"{self.player.state.upper()}_ATTACK_DAMAGE"
                damage = getattr(self.player, damage_attr, self.player.BASIC_ATTACK_DAMAGE)
                
                if self.opponent.take_damage(damage):
                    self.player.attack_hit_count += 1
                    self.player.has_dealt_hit_this_attack = True

        # Opponent attacking player
        if self.opponent.is_attacking and not self.opponent.has_dealt_hit_this_attack:
            attack_rect = self.opponent.rect.inflate(60, 0)
            if attack_rect.colliderect(self.player.rect) and not self.player.is_attacking:
                damage_attr = f"{self.opponent.state.upper()}_ATTACK_DAMAGE"
                damage = getattr(self.opponent, damage_attr, self.opponent.BASIC_ATTACK_DAMAGE)
                
                if self.player.take_damage(damage):
                    self.opponent.attack_hit_count += 1
                    self.opponent.has_dealt_hit_this_attack = True

    def _draw_health_bar(self, screen, character, position, color):
        bar_width, bar_height = 200, 25
        health_perc = max(0, character.health / 45.0)
        
        # Background
        pygame.draw.rect(screen, config.GREY, (position[0], position[1], bar_width, bar_height), border_radius=5)
        # Health Fill
        pygame.draw.rect(screen, color, (position[0], position[1], int(bar_width * health_perc), bar_height), border_radius=5)
        # Outline
        pygame.draw.rect(screen, config.BLACK, (position[0], position[1], bar_width, bar_height), 2, border_radius=5)

        font = pygame.font.Font(None, 24)
        name_text = font.render(f"{character.character_name}: {int(character.health)} HP", True, config.BLACK)
        screen.blit(name_text, (position[0], position[1] - 25))

    def _draw_countdown_overlay(self, time_left):
        """Renders a dim background and a large timer."""
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150)) # Translucent black
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.SysFont("Arial", 120, bold=True)
        # Use Gold color for the timer
        text_surf = font.render(str(time_left), True, (255, 215, 0))
        text_rect = text_surf.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
        self.screen.blit(text_surf, text_rect)

# For direct testing
if __name__ == "__main__":
    pygame.init()
    test_screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    # Replace with your actual character names
    game = Stage1(test_screen, "Player", "Enemy")
    game.run()
    pygame.quit()