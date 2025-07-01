# fightingLogic/fightingLogic.py
import pygame
import config
import random # <--- ADD THIS LINE!

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
        self.jump_strength = -20

        # Animation states (for later)
        self.state = "idle"

        # --- FIGHTING ATTRIBUTES ---
        self.health = 45 # Starting health for both player and enemy
        self.is_attacking = False # True if currently in an attack animation/frame
        self.attack_cooldown = 0 # Timer/duration for the attack animation and cooldown period
        self.attack_hit_count = 0 # Counts successful hits for special attacks

        self.BASIC_ATTACK_DAMAGE = 5
        self.MID_ATTACK_DAMAGE = 10
        self.SUPER_ATTACK_DAMAGE = 15
        self.MID_ATTACK_THRESHOLD = 5 # Hits needed to unlock mid attack
        self.SUPER_ATTACK_THRESHOLD = 10 # Hits needed to unlock super attack

        self.last_hit_by_basic_attack = 0 # Timer for basic attack cooldown (prevents rapid basic hits)
        self.BASIC_ATTACK_COOLDOWN_TIME = 30 # Frames/ticks cooldown between basic attacks

        self.has_dealt_hit_this_attack = False # NEW: Flag to prevent multiple hits from one attack

    def _load_sprite(self):
        # ... (your existing _load_sprite method) ...
        sprite_path = ""
        if self.character_name == "The Boat Man":
            sprite_path = "sprites/EmployeePlaceHolder_Male.jpg"
        elif self.character_name == "The Log Lady":
            sprite_path = "sprites/EmployeePlaceHolder_Female.jpg"

        try:
            image = pygame.image.load(sprite_path).convert_alpha() # Use convert_alpha for transparency
            image = pygame.transform.scale(image, (150, 150))
            return image
        except pygame.error as e:
            print(f"Error loading character sprite ({sprite_path}): {e}")
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
            self.vel_y += config.GRAVITY
            if self.vel_y > 10:
                self.vel_y = 10

        # Update position
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Simple floor collision
        if self.rect.bottom >= config.SCREEN_HEIGHT - config.GROUND_HEIGHT:
            self.rect.bottom = config.SCREEN_HEIGHT - config.GROUND_HEIGHT
            self.vel_y = 0
            self.on_ground = True

        # Keep player within screen bounds horizontally
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x = 0
        if self.rect.right > config.SCREEN_WIDTH:
            self.rect.right = config.SCREEN_WIDTH
            self.vel_x = 0
        
        # Handle attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            if self.attack_cooldown == 0:
                self.is_attacking = False # Attack animation/duration is over
                self.state = "idle" # Return to idle state
                self.has_dealt_hit_this_attack = False # NEW: Reset hit flag for next attack

        # Handle basic attack cooldown
        if self.last_hit_by_basic_attack > 0:
            self.last_hit_by_basic_attack -= 1

    def move(self, direction):
        self.vel_x = direction * config.PLAYER_SPEED

    def stop_move(self):
        self.vel_x = 0

    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False

    def attack(self, attack_type="basic"):
        if self.is_attacking or self.attack_cooldown > 0:
            return None # Cannot attack if already attacking or on cooldown

        self.is_attacking = True
        self.state = attack_type # Set state for potential animation later
        self.attack_cooldown = 60 # Example cooldown in frames (adjust as needed for animation time)
        self.has_dealt_hit_this_attack = False # NEW: Ensure this is reset when attack begins

        damage = 0
        if attack_type == "basic":
            damage = self.BASIC_ATTACK_DAMAGE
            self.last_hit_by_basic_attack = self.BASIC_ATTACK_COOLDOWN_TIME
            print(f"{self.character_name} uses BASIC Attack! Deals {damage} damage.")
        elif attack_type == "mid":
            damage = self.MID_ATTACK_DAMAGE
            self.attack_hit_count = 0 # Reset hit counter after using mid attack
            print(f"{self.character_name} uses MID Attack! Deals {damage} damage.")
        elif attack_type == "super":
            damage = self.SUPER_ATTACK_DAMAGE
            self.attack_hit_count = 0 # Reset hit counter after using super attack
            print(f"{self.character_name} uses SUPER Attack! Deals {damage} damage.")
        else:
            print(f"Unknown attack type: {attack_type}")
            return None

        return damage

    def take_damage(self, amount):
        # The rule is: "Neither can hurt the other if one is already attacking."
        # So, if the character is currently attacking, they won't take damage.
        if not self.is_attacking:
            self.health -= amount
            if self.health < 0:
                self.health = 0
            print(f"{self.character_name} takes {amount} damage! Health: {self.health}")
            # You might add a hit animation or sound here
            return True # Indicate damage was successfully taken
        return False # Indicate damage was not taken (due to being in attack)

    def handle_ai(self, player_rect, player_is_attacking):
        #Basic AI for the enemy. player_rect is the rect of the human player
        if self.is_player_controlled:
            return

        if self.is_attacking or self.attack_cooldown > 0:
            return

        distance_x = player_rect.centerx - self.rect.centerx
        abs_distance_x = abs(distance_x)
        close_range = 100 # Distance for basic attack

        # AI DECISION LOGIC
        # Condition 1: Basic Attack if close, player not attacking, and no basic cooldown
        if abs_distance_x < close_range and not player_is_attacking and self.last_hit_by_basic_attack == 0:
            # Added a simple check to prevent overlap before attack, adjust as needed
            if (distance_x > 0 and self.rect.right < player_rect.left + 20) or \
               (distance_x < 0 and self.rect.left > player_rect.right - 20) or \
               abs_distance_x < 50: # Force attack if very close
                self.vel_x = 0
                print(f"DEBUG: {self.character_name} AI decided to basic_attack! (Player not attacking)") # ADD THIS LINE
                return "basic_attack"

        # Condition 2: Mid Attack (if unlocked)
        if self.attack_hit_count >= self.MID_ATTACK_THRESHOLD and abs_distance_x < close_range * 1.5:
            self.vel_x = 0
            print(f"DEBUG: {self.character_name} AI decided to mid_attack!") # ADD THIS LINE
            return "mid_attack"

        # Condition 3: Super Attack (if unlocked)
        if self.attack_hit_count >= self.SUPER_ATTACK_THRESHOLD and abs_distance_x < close_range * 2:
            self.vel_x = 0
            print(f"DEBUG: {self.character_name} AI decided to super_attack!") # ADD THIS LINE
            return "super_attack"

        # Movement: Move towards player if not close enough
        if abs_distance_x > close_range / 2:
            if distance_x > 0:
                self.move(1)
            else:
                self.move(-1)
        else:
            self.stop_move()

        # Jumping (simple AI jump)
        if self.on_ground and random.randint(1, 100) == 1:
            self.jump()

        return None