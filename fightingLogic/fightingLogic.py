# fightingLogic/fightingLogic.py
import pygame
import config
import random


class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        try:
            self.sprite_sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            print(f"Error loading spritesheet file {filename}: {e}")
            self.sprite_sheet = None

    def get_sprite(self, x, y, w, h):
        if self.sprite_sheet is None:
            return None # Or return a placeholder if you prefer

        sprite = pygame.Surface((w, h), pygame.SRCALPHA)
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, character_name, initial_x, initial_y, is_player_controlled=True):
        super().__init__()
        self.character_name = character_name
        self.is_player_controlled = is_player_controlled
        
        self.spritesheet_loader = None
        
        self.animations = {}
        self.current_frame = 0
        self.animation_speed = 5
        self.animation_timer = 0
        
        self._load_all_sprites()

        if not self.animations.get("idle") or not self.animations["idle"]:
            print(f"WARNING: No 'idle' animation found for {self.character_name} after _load_all_sprites. Using defualt_chicken.")
            self.animations["idle"] = [self._get_defualt_chicken_frame(100, 100)] 
            
        self.image = self.animations["idle"][0]
        self.rect = self.image.get_rect(midbottom=(initial_x, initial_y))


        self.hitbox_offset_x = 120
        self.hitbox_offset_y = 10
        self.hitbox_width_reduction = 40 
        self.hitbox_height_reduction = 20 

        self.hitbox = pygame.Rect(
            self.rect.x + self.hitbox_offset_x,
            self.rect.y + self.hitbox_offset_y,
            self.rect.width - self.hitbox_width_reduction,
            self.rect.height - self.hitbox_height_reduction
        )

        # --- END CHARACTER HITBOX ADDITIONS ---

   #--- ATTACK HITBOX PROPERTIES ---
        self.attack_hitbox = None
        self.attack_hitbox_width = 70
        self.attack_hitbox_height = 40
        self.attack_hitbox_offset_x_right = 50
        self.attack_hitbox_offset_x_left = -20
        self.attack_hitbox_offset_y = 20
        # --- END ATTACK HITBOX PROPERTIES ---

        # Movement variables
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = True
        self.jump_strength = -20
        self.facing_right = True # Initial direction

        # Animation states
        self.state = "idle"

        # Movement variables
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = True
        self.jump_strength = -20
        self.facing_right = True

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
        self.BASIC_ATTACK_COOLDOWN_TIME = 2

        self.has_dealt_hit_this_attack = False

    def _get_defualt_chicken_frame(self, width=100, height=100):
        default_sprite_sheet_path = "sprites/defualt_chicken.png"
        
        default_spritesheet = Spritesheet(default_sprite_sheet_path)
        if default_spritesheet.sprite_sheet is None:
            placeholder_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            placeholder_surface.fill((255, 0, 255, 128))
            font = pygame.font.Font(None, 20)
            text = font.render("NO CHICKEN!", True, config.WHITE)
            text_rect = text.get_rect(center=(width // 2, height // 2))
            placeholder_surface.blit(text, text_rect)
            return placeholder_surface
        
        chicken_frame = default_spritesheet.get_sprite(0, 0, width, height)
        if chicken_frame:
            return chicken_frame
        else:
            placeholder_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            placeholder_surface.fill((255, 0, 255, 128))
            return placeholder_surface

    def _create_placeholder(self, width=100, height=100):
        return self._get_defualt_chicken_frame(width, height)

    def _load_all_sprites(self):
        """Loads the main sprite sheet and parses individual animation frames, with chicken fallback."""
        current_frame_width = 100
        current_frame_height = 100
        sprite_sheet_path = None
        base_x_offset = 0
        base_y_offset = 0

        if self.character_name == "The Boat Man":
            sprite_sheet_path = "sprites/male_punch.png"
            base_x_offset = 5
            base_y_offset = 10
        elif self.character_name == "The Log Lady":
            sprite_sheet_path = "sprites/test_punching_female.png"
            base_x_offset = 5
            base_y_offset = 10
        else:
            print(f"No specific sprite sheet path defined for '{self.character_name}'. Using default chicken.")
            self._load_chicken_fallback_sprites(current_frame_width, current_frame_height)
            return # Exit the function here to prevent further execution

        # Only attempt to load the spritesheet if a path was defined
        if sprite_sheet_path:
            self.spritesheet_loader = Spritesheet(sprite_sheet_path)
            if self.spritesheet_loader.sprite_sheet:
                print(f"Loaded sprite sheet for {self.character_name}: {sprite_sheet_path}")
                
                # --- PARSE SPRITE SHEET USING get_sprite ---
                self.animations["idle"] = []
                self.animations["idle"].append(self.spritesheet_loader.get_sprite(base_x_offset + 0 * current_frame_width, base_y_offset, current_frame_width, current_frame_height))
                
                self.animations["basic_attack"] = []
                self.animations["basic_attack"].append(self.spritesheet_loader.get_sprite(base_x_offset + 0 * current_frame_width, base_y_offset, current_frame_width, current_frame_height))
                self.animations["basic_attack"].append(self.spritesheet_loader.get_sprite(base_x_offset + 1 * current_frame_width, base_y_offset, current_frame_width, current_frame_height))
                self.animations["basic_attack"].append(self.spritesheet_loader.get_sprite(base_x_offset + 2 * current_frame_width, base_y_offset, current_frame_width, current_frame_height))
                self.animations["basic_attack"].append(self.spritesheet_loader.get_sprite(base_x_offset + 3 * current_frame_width, base_y_offset, current_frame_width, current_frame_height))
                
                self.animations["walking"] = [self.animations["idle"][0]]
                self.animations["jumping"] = [self.animations["idle"][0]]
            else:
                # Fallback if the specific character sheet fails to load
                print(f"Error loading sprite sheet for {self.character_name}, using chicken fallback.")
                self._load_chicken_fallback_sprites(current_frame_width, current_frame_height)

        elif self.character_name == "The Log Lady":
            sprite_sheet_path = "sprites/test_punching_female.png"
            base_x_offset = 5
            base_y_offset = 10

            # --- USE THE SPRITESHEET CLASS HERE ---
            self.spritesheet_loader = Spritesheet(sprite_sheet_path)
            if self.spritesheet_loader.sprite_sheet:
                print(f"Loaded sprite sheet for {self.character_name}: {sprite_sheet_path}")

                # --- PARSE FEMALE SPRITE SHEET USING get_sprite ---
                self.animations["idle"] = []
                self.animations["idle"].append(self.spritesheet_loader.get_sprite(base_x_offset + 0 * current_frame_width, base_y_offset, current_frame_width, current_frame_height))
                
                self.animations["basic_attack"] = []
                self.animations["basic_attack"].append(self.spritesheet_loader.get_sprite(base_x_offset + 0 * current_frame_width, base_y_offset, current_frame_width, current_frame_height))
                self.animations["basic_attack"].append(self.spritesheet_loader.get_sprite(base_x_offset + 1 * current_frame_width, base_y_offset, current_frame_width, current_frame_height))
                self.animations["basic_attack"].append(self.spritesheet_loader.get_sprite(base_x_offset + 2 * current_frame_width, base_y_offset, current_frame_width, current_frame_height))
                self.animations["basic_attack"].append(self.spritesheet_loader.get_sprite(base_x_offset + 3 * current_frame_width, base_y_offset, current_frame_width, current_frame_height))
                
                self.animations["walking"] = [self.animations["idle"][0]]
                self.animations["jumping"] = [self.animations["idle"][0]]
            else:
                print(f"Error loading sprite sheet for {self.character_name}, using chicken fallback.")
                self._load_chicken_fallback_sprites(current_frame_width, current_frame_height)

        else: # This handles 'Kangaroo' or any other character not explicitly listed
            print(f"No specific sprite sheet path defined for '{self.character_name}'. Using default chicken.")
            self._load_chicken_fallback_sprites(current_frame_width, current_frame_height)

        sprite_sheet_path = None
        current_frame_width = 100
        current_frame_height = 100

        # Define offsets specific to each character type
        base_x_offset = 0  # Default or placeholder
        base_y_offset = 0  # Default or placeholder

        if self.character_name == "The Boat Man":
            sprite_sheet_path = "sprites/male_punch.png"
            # Define offsets for The Boat Man's sprite sheet
            # You'll need to inspect male_punch.png to find these actual values.
            # Using placeholders for now:
            base_x_offset = 5 # Example, adjust based on male_punch.png
            base_y_offset = 10 # Example, adjust based on male_punch.png

            try:
                self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
                print(f"Loaded sprite sheet for {self.character_name}: {sprite_sheet_path}")

                # --- PARSE MALE SPRITE SHEET ---
                self.animations["idle"] = []
                self.animations["idle"].append(self.sprite_sheet.subsurface(pygame.Rect(base_x_offset + 0 * current_frame_width, base_y_offset, current_frame_width, current_frame_height)))

                self.animations["basic_attack"] = []
                self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(base_x_offset + 0 * current_frame_width, base_y_offset, current_frame_width, current_frame_height)))
                self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(base_x_offset + 1 * current_frame_width, base_y_offset, current_frame_width, current_frame_height)))
                self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(base_x_offset + 2 * current_frame_width, base_y_offset, current_frame_width, current_frame_height)))
                self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(base_x_offset + 3 * current_frame_width, base_y_offset, current_frame_width, current_frame_height)))

                self.animations["walking"] = [self.animations["idle"][0]]
                self.animations["jumping"] = [self.animations["idle"][0]]

            except pygame.error as e:
                print(f"Error loading sprite sheet for {self.character_name}: {e}")
                self._load_chicken_fallback_sprites(current_frame_width, current_frame_height)


        elif self.character_name == "The Log Lady":
            sprite_sheet_path = "sprites/test_punching_female.png"
            # Offsets for The Log Lady are correctly defined here
            base_x_offset = 5
            base_y_offset = 10

            try:
                self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
                print(f"Loaded sprite sheet for {self.character_name}: {sprite_sheet_path}")

                # --- PARSE FEMALE SPRITE SHEET ---
                self.animations["idle"] = []
                self.animations["idle"].append(self.sprite_sheet.subsurface(pygame.Rect(base_x_offset + 0 * current_frame_width, base_y_offset, current_frame_width, current_frame_height)))

                self.animations["basic_attack"] = []
                self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(base_x_offset + 0 * current_frame_width, base_y_offset, current_frame_width, current_frame_height)))
                self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(base_x_offset + 1 * current_frame_width, base_y_offset, current_frame_width, current_frame_height)))
                self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(base_x_offset + 2 * current_frame_width, base_y_offset, current_frame_width, current_frame_height)))
                self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(base_x_offset + 3 * current_frame_width, base_y_offset, current_frame_width, current_frame_height)))

                self.animations["walking"] = [self.animations["idle"][0]]
                self.animations["jumping"] = [self.animations["idle"][0]]

            except pygame.error as e:
                print(f"Error loading sprite sheet for {self.character_name}: {e}")
                self._load_chicken_fallback_sprites(current_frame_width, current_frame_height)

        else: # This handles 'Kangaroo' or any other character not explicitly listed
            print(f"No specific sprite sheet path defined for '{self.character_name}'. Using default chicken.")
            self._load_chicken_fallback_sprites(current_frame_width, current_frame_height)

        # Final check to ensure self.image is set, even if all specific loading failed.
        # This part assumes self.image will be set either by a specific character
        # loading or by _load_chicken_fallback_sprites.
        # It's good practice to have a final fallback for self.image and self.rect.
        if not hasattr(self, 'image') or self.image is None:
            print(f"CRITICAL ERROR: self.image not set for {self.character_name}. Using emergency placeholder.")
            self.image = pygame.Surface((current_frame_width, current_frame_height))
            self.image.fill((255, 0, 255)) # Magenta for error
        if not hasattr(self, 'rect') or self.rect is None:
            self.rect = self.image.get_rect()

    def _load_chicken_fallback_sprites(self, width, height):
        """Helper to load and set up animations for the defualt_chicken."""
        chicken_frame = self._get_defualt_chicken_frame(width, height) 
        
        self.animations["idle"] = [chicken_frame]
        self.animations["basic_attack"] = [chicken_frame]
        self.animations["mid_attack"] = [chicken_frame]
        self.animations["super_attack"] = [chicken_frame]
        self.animations["take_damage"] = [chicken_frame]
        self.animations["death"] = [chicken_frame]
        self.animations["walking"] = [chicken_frame]
        self.animations["jumping"] = [chicken_frame]

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
                # Fallback if current state has no animation or it's empty
                print(f"WARNING: Animation state '{self.state}' not found or empty for {self.character_name}. Defaulting to idle.")
                if self.animations.get("idle"):
                    self.state = "idle" # Corrected from self.current_animation
                    self.current_frame = 0
                    current_image = self.animations["idle"][0]
                else:
                    # If even idle is missing (critical error during load), use a generic chicken frame
                    current_image = self._get_defualt_chicken_frame(self.rect.width, self.rect.height)
            
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

    # This single check at the top is very good and sufficient.
    if self.is_attacking or self.attack_cooldown > 0: 
        return

    distance_x = player_rect.centerx - self.rect.centerx
    abs_distance_x = abs(distance_x)
    close_range = 100

    # The AI's decision to attack is now based on the main cooldown.
    # No need to add another cooldown check here because of the line above.
    # The logic is solid.
    if abs_distance_x < close_range and not player_is_attacking:
        # Check for super attack first (highest priority)
        if self.attack_hit_count >= self.SUPER_ATTACK_THRESHOLD and abs_distance_x < close_range * 2:
            self.vel_x = 0
            print(f"DEBUG: {self.character_name} AI decided to super_attack!")
            return "super_attack"
        # Check for mid attack next
        elif self.attack_hit_count >= self.MID_ATTACK_THRESHOLD and abs_distance_x < close_range * 1.5:
            self.vel_x = 0
            print(f"DEBUG: {self.character_name} AI decided to mid_attack!")
            return "mid_attack"
        # Finally, check for basic attack
        elif (distance_x > 0 and self.rect.right < player_rect.left + 20) or \
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






