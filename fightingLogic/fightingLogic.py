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
        
        # Load character-specific sprites or fall back to chicken
        self._load_all_sprites()

        # Ensure "idle" animation exists. If not, use the defualt_chicken frame.
        if not self.animations.get("idle") or not self.animations["idle"]:
            print(f"WARNING: No 'idle' animation found for {self.character_name} after _load_all_sprites. Using defualt_chicken.")
            # Use the default frame size for chicken if no specific size was set by _load_all_sprites
            self.animations["idle"] = [self._get_defualt_chicken_frame(100, 100)] 
            
        self.image = self.animations["idle"][0]
        self.rect = self.image.get_rect(midbottom=(initial_x, initial_y))

        # --- CHARACTER HITBOX (for taking damage/collisions) ---
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
        self.BASIC_ATTACK_COOLDOWN_TIME = 2 # This is very short, consider increasing

        self.has_dealt_hit_this_attack = False

    def _get_defualt_chicken_frame(self, width=100, height=100): # Added default width/height
        """
        Loads the defualt_chicken sprite sheet and returns its first idle frame.
        This is the preferred graphical fallback for all missing sprites.
        """
        default_sprite_sheet_path = "sprites/defualt_chicken.png" 

        try:
            default_sheet = pygame.image.load(default_sprite_sheet_path).convert_alpha()
            
            chicken_frame_width = 100
            chicken_frame_height = 100
            
            return default_sheet.subsurface(pygame.Rect(0, 0, chicken_frame_width, chicken_frame_height))
        except pygame.error as e:
            print(f"CRITICAL ERROR: Could not load defualt_chicken sprite sheet ({default_sprite_sheet_path}): {e}")
            placeholder_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            placeholder_surface.fill((255, 0, 255, 128)) # Semi-transparent magenta for visibility
            font = pygame.font.Font(None, 20)
            text = font.render("NO CHICKEN!", True, config.WHITE)
            text_rect = text.get_rect(center=(width // 2, height // 2))
            placeholder_surface.blit(text, text_rect)
            return placeholder_surface

    def _create_placeholder(self, width=100, height=100): # Now consistently returns chicken frame
        """
        Helper function to create a placeholder surface for missing sprites.
        This now consistently returns the defualt_chicken frame.
        """
        return self._get_defualt_chicken_frame(width, height)

    def _load_all_sprites(self):
        """Loads the main sprite sheet and parses individual animation frames, with chicken fallback."""
        
        sprite_sheet_path = None
        # Define default frame_width/height at the start of the function for general use
        current_frame_width = 100 
        current_frame_height = 100

        if self.character_name == "The Boat Man":
            sprite_sheet_path = "sprites/male_punch.png"
            # No need to redefine male_frame_width/height here, current_frame_width/height will be used.
            
        elif self.character_name == "The Log Lady":
            sprite_sheet_path = "sprites/female_punch.bmp"
            # No need to redefine female_frame_width/height here, current_frame_width/height will be used.

        # Try to load the specific character's sprite sheet
        if sprite_sheet_path:
            try:
                self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
                print(f"Loaded sprite sheet for {self.character_name}: {sprite_sheet_path}")

                # --- PARSE MALE SPRITE SHEET ---
                if self.character_name == "The Boat Man":
                    self.animations["idle"] = []
                    self.animations["idle"].append(self.sprite_sheet.subsurface(pygame.Rect(1 * current_frame_width, 0, current_frame_width, current_frame_height)))
                    
                    self.animations["basic_attack"] = []
                    self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(2 * current_frame_width, 0, current_frame_width, current_frame_height)))
                    self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(3 * current_frame_width, 0, current_frame_width, current_frame_height)))
                    self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(0 * current_frame_width, 1 * current_frame_height, current_frame_width, current_frame_height)))
                    self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(1 * current_frame_width, 1 * current_frame_height, current_frame_width, current_frame_height)))
                    
                    self.animations["walking"] = [self.animations["idle"][0]]
                    self.animations["jumping"] = [self.animations["idle"][0]]

                # --- PARSE FEMALE SPRITE SHEET ---
                elif self.character_name == "The Log Lady":
                    self.animations["idle"] = []
                    self.animations["idle"].append(self.sprite_sheet.subsurface(pygame.Rect(0 * current_frame_width, 0, current_frame_width, current_frame_height)))

                    self.animations["basic_attack"] = []
                    self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(0 * current_frame_width, 0, current_frame_width, current_frame_height)))
                    self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(1 * current_frame_width, 0, current_frame_width, current_frame_height)))
                    self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(2 * current_frame_width, 0, current_frame_width, current_frame_height))) # Corrected 'female_frame_height' to 'current_frame_height'

                    self.animations["walking"] = [self.animations["idle"][0]]
                    self.animations["jumping"] = [self.animations["idle"][0]]
                
                # After attempting to load and parse, ensure 'idle' animation is set.
                # If not, it means parsing failed or the character name was not matched,
                # so fall back to chicken.
                if not self.animations.get("idle") or not self.animations["idle"]:
                    print(f"WARNING: 'idle' animation not populated for {self.character_name}. Falling back to chicken.")
                    self._load_chicken_fallback_sprites(current_frame_width, current_frame_height) # Explicitly load chicken
                
            except pygame.error as e: # This 'except' block is now correctly placed to catch errors from the 'try' above it
                print(f"Error loading sprite sheet for {self.character_name} from {sprite_sheet_path}: {e}")
                print(f"Falling back to defualt_chicken for {self.character_name}.")
                self._load_chicken_fallback_sprites(current_frame_width, current_frame_height) # Explicitly load chicken
        else:
            # If character_name is unknown or no specific path, use chicken directly
            print(f"No specific sprite sheet path defined for '{self.character_name}'. Using defualt_chicken.")
            self._load_chicken_fallback_sprites(current_frame_width, current_frame_height)

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






