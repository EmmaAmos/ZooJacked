# fightingLogic/fightingLogic.py
import pygame
import config
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, character_name, initial_x, initial_y, is_player_controlled=True):
        super().__init__()
        self.character_name = character_name
        self.is_player_controlled = is_player_controlled
        
        self.sprite_sheet = None
        self.animations = {}
        self.current_frame = 0
        self.animation_speed = 5
        self.animation_timer = 0
        
        self._load_all_sprites()
        self.image = self.animations.get("idle", [self._create_placeholder()])[0]
        self.rect = self.image.get_rect(midbottom=(initial_x, initial_y))

        # --- CHARACTER HITBOX (for taking damage/collisions) ---
        self.hitbox_offset_x = 20
        self.hitbox_offset_y = 10
        self.hitbox_width_reduction = 0 # Set to 0 to make it same width as sprite
        self.hitbox_height_reduction = 0 # Set to 0 to make it same height as sprite

        self.hitbox = pygame.Rect(
            self.rect.x + self.hitbox_offset_x,
            self.rect.y + self.hitbox_offset_y,
            self.rect.width - self.hitbox_width_reduction,
            self.rect.height - self.hitbox_height_reduction
        )
        # --- END CHARACTER HITBOX ADDITIONS ---

        # --- ATTACK HITBOX PROPERTIES ---
        self.attack_hitbox = None # This will hold the Rect for the attack hitbox
        self.attack_hitbox_width = 70  # Width of the basic punch hitbox
        self.attack_hitbox_height = 40 # Height of the basic punch hitbox
        # Offsets for positioning the attack hitbox relative to the player's rect
        self.attack_hitbox_offset_x_right = 50 # X-offset when facing right (from self.rect.right)
        self.attack_hitbox_offset_x_left = -20 # X-offset when facing left (from self.rect.left)
        self.attack_hitbox_offset_y = 20 # Y-offset (from self.rect.y)
        # --- END ATTACK HITBOX PROPERTIES ---

        # Movement variables
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = True
        self.jump_strength = -20
        self.facing_right = True # Initial direction

        # Animation states
        self.state = "idle"

        # --- FIGHTING ATTRIBUTES ---
        self.health = 45
        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_hit_count = 0

        self.BASIC_ATTACK_DAMAGE = 5
        self.MID_ATTACK_DAMAGE = 10
        self.SUPER_ATTACK_DAMAGE = 15
        self.MID_ATTACK_THRESHOLD = 5
        self.SUPER_ATTACK_THRESHOLD = 10

        self.last_hit_by_basic_attack = 0
        self.BASIC_ATTACK_COOLDOWN_TIME = 30

        self.has_dealt_hit_this_attack = False

    def _create_placeholder(self, width=150, height=150):
        """Helper function to create a placeholder surface for missing sprites."""
        placeholder = pygame.Surface((width, height), pygame.SRCALPHA)
        color = config.BLUE if self.is_player_controlled else config.RED
        pygame.draw.circle(placeholder, color, (width // 2, height // 2), width // 2 - 5)
        font = pygame.font.Font(None, 20)
        text = font.render("NO IMG", True, config.WHITE)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        placeholder.blit(text, text_rect)
        return placeholder

    def _load_all_sprites(self):
        """Loads the main sprite sheet and parses individual animation frames."""
        
        if self.character_name == "The Boat Man":
            sprite_sheet_path = "sprites/male_punch.png" # Assuming this is your test_punching.jpg
            male_frame_width = 150  # Based on test_punching.jpg
            male_frame_height = 150 # Based on test_punching.jpg
            
            try:
                self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
            except pygame.error as e:
                print(f"Error loading sprite sheet ({sprite_sheet_path}): {e}")
                placeholder_img = self._create_placeholder(male_frame_width, male_frame_height)
                self.animations["idle"] = [placeholder_img]
                self.image = self.animations["idle"][0]
                return

            # --- PARSE MALE SPRITE SHEET (Adjusted based on test_punching.jpg layout) ---
            self.animations["idle"] = []
            # First row, second image (standing) and possibly the first for a slight variation
            self.animations["idle"].append(self.sprite_sheet.subsurface(pygame.Rect(1 * male_frame_width, 0, male_frame_width, male_frame_height)))
            
            self.animations["basic_attack"] = []
            # Based on test_punching.jpg, the basic attack starts on the first row, third image, and continues to the second row.
            # Frame 1: First row, 3rd image (punch start)
            self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(2 * male_frame_width, 0, male_frame_width, male_frame_height)))
            # Frame 2: First row, 4th image (punch extension)
            self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(3 * male_frame_width, 0, male_frame_width, male_frame_height)))
            # Frame 3: Second row, 1st image (punch with effect)
            self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(0 * male_frame_width, 1 * male_frame_height, male_frame_width, male_frame_height)))
            # Frame 4: Second row, 2nd image (punch follow through) - adjust as needed
            self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(1 * male_frame_width, 1 * male_frame_height, male_frame_width, male_frame_height)))
            # Add more frames if your basic attack animation has them.
            # Example if you want more frames from test_punching.jpg:
            # self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(2 * male_frame_width, 1 * male_frame_height, male_frame_width, male_frame_height))) # Third frame in second row
            # self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(3 * male_frame_width, 1 * male_frame_height, male_frame_width, male_frame_height))) # Fourth frame in second row
            # self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(0 * male_frame_width, 2 * male_frame_height, male_frame_width, male_frame_height))) # First frame in third row
            # self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(1 * male_frame_width, 2 * male_frame_height, male_frame_width, male_frame_height))) # Second frame in third row
            # self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(2 * male_frame_width, 2 * male_frame_height, male_frame_width, male_frame_height))) # Third frame in third row
            # self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(3 * male_frame_width, 2 * male_frame_height, male_frame_width, male_frame_height))) # Fourth frame in third row

            self.animations["walking"] = []
            # Assuming walking frames are in a specific row.
            # If your walking animation is made of frames from test_punching.jpg, you'll need to define them here.
            # For now, using idle frames as a placeholder if no dedicated walking frames are shown:
            self.animations["walking"] = [self.animations["idle"][0]] # Use first idle frame if no distinct walk.

            self.animations["jumping"] = []
            if self.animations["idle"]: 
                self.animations["jumping"].append(self.animations["idle"][0]) 
            else: 
                self.animations["jumping"].append(self._create_placeholder(male_frame_width, male_frame_height))


        elif self.character_name == "The Log Lady":
            sprite_sheet_path = "sprites/female_punch.bmp" # Assuming .bmp as discussed
            female_frame_width = 150
            female_frame_height = 150

            try:
                self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
            except pygame.error as e:
                print(f"Error loading sprite sheet ({sprite_sheet_path}): {e}")
                placeholder_img = self._create_placeholder(female_frame_width, female_frame_height)
                self.animations["idle"] = [placeholder_img]
                self.image = self.animations["idle"][0]
                return


            # --- PARSE FEMALE SPRITE SHEET ---
            self.animations["idle"] = []
            # The yellow box in female_punch_exampleFrames.jpg is the idle/first frame of attack sequence.
            self.animations["idle"].append(self.sprite_sheet.subsurface(pygame.Rect(0 * female_frame_width, 0, female_frame_width, female_frame_height)))

            self.animations["basic_attack"] = []
            # Based on your description: yellow, green, pink boxes
            # Frame 1 (Yellow box): First row, 1st image
            self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(0 * female_frame_width, 0, female_frame_width, female_frame_height)))
            # Frame 2 (Green box): First row, 2nd image (punch with effect)
            self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(1 * female_frame_width, 0, female_frame_width, female_frame_height)))
            # Frame 3 (Pink box): First row, 3rd image (punch follow through/end)
            self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(2 * female_frame_width, 0, female_frame_width, female_frame_height)))

            self.animations["walking"] = [self.animations["idle"][0]] # Use idle frame as placeholder
            self.animations["jumping"] = [self.animations["idle"][0]] # Use idle frame as placeholder
        
    def update(self):
        # Update facing direction based on movement
        if self.vel_x > 0:
            self.facing_right = True
        elif self.vel_x < 0:
            self.facing_right = False

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
            if self.state == "jumping":
                if self.vel_x == 0:
                    self.state = "idle"
                else:
                    self.state = "walking"

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
                self.is_attacking = False
                self.attack_hitbox = None # IMPORTANT: Remove attack hitbox when cooldown ends
                if self.vel_x == 0 and self.on_ground:
                    self.state = "idle" 
                elif self.vel_x != 0 and self.on_ground:
                    self.state = "walking"
                elif not self.on_ground:
                    self.state = "jumping"
                self.has_dealt_hit_this_attack = False

        # Handle basic attack cooldown (for player to initiate next attack)
        if self.last_hit_by_basic_attack > 0:
            self.last_hit_by_basic_attack -= 1

        # --- UPDATE CHARACTER HITBOX POSITION ---
        self.hitbox.x = self.rect.x + self.hitbox_offset_x
        self.hitbox.y = self.rect.y + self.hitbox_offset_y
        # --- END UPDATE CHARACTER HITBOX POSITION ---

        # --- UPDATE ATTACK HITBOX POSITION (if active) ---
        if self.attack_hitbox:
            if self.facing_right:
                self.attack_hitbox.x = self.rect.right - self.attack_hitbox_width + self.attack_hitbox_offset_x_right
            else:
                self.attack_hitbox.x = self.rect.left - self.attack_hitbox_offset_x_left # Adjust for left-facing
            self.attack_hitbox.y = self.rect.y + self.attack_hitbox_offset_y
        # --- END UPDATE ATTACK HITBOX POSITION ---


        # ANIMATION UPDATE LOGIC
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            if self.state in self.animations and self.animations[self.state]:
                self.current_frame = (self.current_frame + 1) % len(self.animations[self.state])
                current_image = self.animations[self.state][self.current_frame] # Get the current frame
            else:
                current_image = self.animations.get("idle", [self._create_placeholder()])[0]
                self.current_frame = 0
            
            # Apply flip only once based on facing_right
            if not self.facing_right:
                self.image = pygame.transform.flip(current_image, True, False)
            else:
                self.image = current_image # Use the original image if facing right

    def move(self, direction):
        self.vel_x = direction * config.PLAYER_SPEED
        if self.on_ground and self.state != "basic_attack":
            self.state = "walking"

    def stop_move(self):
        self.vel_x = 0
        if self.on_ground and self.state != "basic_attack":
            self.state = "idle"

    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False
            self.state = "jumping"

    def attack(self, attack_type="basic"):
        if self.is_attacking or self.attack_cooldown > 0:
            return None

        self.is_attacking = True
        self.state = attack_type
        self.current_frame = 0 
        self.attack_cooldown = 60 # Duration of attack animation/cooldown

        # --- CREATE ATTACK HITBOX WHEN ATTACK STARTS ---
        if attack_type == "basic":
            # Position the attack hitbox relative to the player's current position and facing direction
            if self.facing_right:
                attack_x = self.rect.right - self.attack_hitbox_width + self.attack_hitbox_offset_x_right
            else:
                attack_x = self.rect.left - self.attack_hitbox_offset_x_left # Adjust for left-facing
            
            attack_y = self.rect.y + self.attack_hitbox_offset_y
            
            self.attack_hitbox = pygame.Rect(
                attack_x,
                attack_y,
                self.attack_hitbox_width,
                self.attack_hitbox_height
            )
            # You might want to delay the activation of the hitbox to a specific animation frame
            # (e.g., if self.current_frame == 2 for a punch) for more precise hit detection.
            # For now, it activates immediately with the attack.
        # --- END CREATE ATTACK HITBOX ---

        self.has_dealt_hit_this_attack = False # Reset hit flag for this new attack

        damage = 0
        if attack_type == "basic":
            damage = self.BASIC_ATTACK_DAMAGE
            self.last_hit_by_basic_attack = self.BASIC_ATTACK_COOLDOWN_TIME
            print(f"{self.character_name} uses BASIC Attack! Deals {damage} damage.")
        elif attack_type == "mid":
            damage = self.MID_ATTACK_DAMAGE
            self.attack_hit_count = 0
            print(f"{self.character_name} uses MID Attack! Deals {damage} damage.")
        elif attack_type == "super":
            damage = self.SUPER_ATTACK_DAMAGE
            self.attack_hit_count = 0
            print(f"{self.character_name} uses SUPER Attack! Deals {damage} damage.")
        else:
            print(f"Unknown attack type: {attack_type}")
            return None

        return damage

    def take_damage(self, amount):
        if not self.is_attacking:
            self.health -= amount
            if self.health < 0:
                self.health = 0
            print(f"{self.character_name} takes {amount} damage! Health: {self.health}")
            return True
        return False

    def handle_ai(self, player_rect, player_is_attacking):
        if self.is_player_controlled:
            return

        if self.is_attacking or self.attack_cooldown > 0:
            return

        distance_x = player_rect.centerx - self.rect.centerx
        abs_distance_x = abs(distance_x)
        close_range = 100

        if abs_distance_x < close_range and not player_is_attacking and self.last_hit_by_basic_attack == 0:
            if (distance_x > 0 and self.rect.right < player_rect.left + 20) or \
               (distance_x < 0 and self.rect.left > player_rect.right - 20) or \
               abs_distance_x < 50:
                self.vel_x = 0
                print(f"DEBUG: {self.character_name} AI decided to basic_attack! (Player not attacking)")
                return "basic_attack"

        if self.attack_hit_count >= self.MID_ATTACK_THRESHOLD and abs_distance_x < close_range * 1.5:
            self.vel_x = 0
            print(f"DEBUG: {self.character_name} AI decided to mid_attack!")
            return "mid_attack"

        if self.attack_hit_count >= self.SUPER_ATTACK_THRESHOLD and abs_distance_x < close_range * 2:
            self.vel_x = 0
            print(f"DEBUG: {self.character_name} AI decided to super_attack!")
            return "super_attack"

        if abs_distance_x > close_range / 2:
            if distance_x > 0:
                self.move(1)
            else:
                self.move(-1)
        else:
            self.stop_move()

        if self.on_ground and random.randint(1, 100) == 1:
            self.jump()

        return None