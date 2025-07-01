# fightingLogic/fightingLogic.py
import pygame
import config

class Player(pygame.sprite.Sprite):
    def __init__(self, character_name, initial_x, initial_y, is_player_controlled=True):
        super().__init__()
        self.character_name = character_name
        self.is_player_controlled = is_player_controlled
        self.image = self._load_sprite()
        self.rect = self.image.get_rect(midbottom=(initial_x, initial_y))

        # Movement variables
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = True
        self.jump_strength = -20 # Negative for upwards movement in Pygame

        # Animation states (for later)
        self.state = "idle"
        # self.animations = self._load_animations() # Placeholder for later

    def _load_sprite(self):
        #Loads the character sprite based on the name.
        sprite_path = ""
        if self.character_name == "The Boat Man":
            sprite_path = "sprites/EmployeePlaceHolder_Male.jpg"
        elif self.character_name == "The Log Lady":
            sprite_path = "sprites/EmployeePlaceHolder_Female.jpg"

        try:
            image = pygame.image.load(sprite_path).convert()
            # Scale the character sprite for visibility, adjust as needed
            image = pygame.transform.scale(image, (150, 150))
            return image
        except pygame.error as e:
            print(f"Error loading character sprite ({sprite_path}): {e}")
            # YOU NEED TO ADD THE REST OF THE ERROR HANDLING HERE
            # (e.g., creating a placeholder surface and returning it)
            # This part was cut off in your provided code,
            # but it's crucial for preventing a crash if the image doesn't load.
            # Example (from my previous suggestion):
            placeholder = pygame.Surface((150, 150), pygame.SRCALPHA)
            color = config.BLUE if self.is_player_controlled else config.RED
            pygame.draw.circle(placeholder, color, (75, 75), 75)
            font = pygame.font.Font(None, 20)
            text = font.render("NO IMG", True, config.WHITE)
            text_rect = text.get_rect(center=(75, 75))
            placeholder.blit(text, text_rect)
            return placeholder


    def update(self):
        """Update the player's position and state."""
        # Apply gravity
        if not self.on_ground:
            self.vel_y += config.GRAVITY # Assuming GRAVITY is defined in config.py
            if self.vel_y > 10: # Cap downward velocity
                self.vel_y = 10

        # Update position
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Simple floor collision (assuming the bottom of the screen is the floor)
        # You'll need more sophisticated collision for platforms
        if self.rect.bottom >= config.SCREEN_HEIGHT - config.GROUND_HEIGHT: # Assuming GROUND_HEIGHT in config
            self.rect.bottom = config.SCREEN_HEIGHT - config.GROUND_HEIGHT
            self.vel_y = 0
            self.on_ground = True

        # Keep player within screen bounds horizontally (optional for fighting game)
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x = 0
        if self.rect.right > config.SCREEN_WIDTH:
            self.rect.right = config.SCREEN_WIDTH
            self.vel_x = 0


    def move(self, direction):
        """Move the player horizontally. -1 for left, 1 for right."""
        self.vel_x = direction * config.PLAYER_SPEED # Assuming PLAYER_SPEED in config.py

    def stop_move(self):
        """Stop horizontal movement."""
        self.vel_x = 0

    def jump(self):
        """Make the player jump."""
        if self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False

    # --- Placeholder for fighting and enemy logic (for later) ---
    def attack(self):
        # Implement attack animation and hit detection
        print(f"{self.character_name} attacks!")

    def take_damage(self, amount):
        # Reduce health, play hit animation
        print(f"{self.character_name} takes {amount} damage!")

    def handle_ai(self, target_player):
        # Basic AI for the tutorial enemy
        if not self.is_player_controlled:
            # Example: simple follow or attack logic
            pass # Implement later