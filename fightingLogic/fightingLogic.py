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
        self.image = self.animations.get("idle", [pygame.Surface((150, 150), pygame.SRCALPHA)])[0]
        self.rect = self.image.get_rect(midbottom=(initial_x, initial_y))

        # --- HITBOX ADDITIONS ---
        # Initialize hitbox relative to the sprite's rect
        # Adjust these values (x_offset, y_offset, width_reduction, height_reduction)
        # to control the size and position of the hitbox relative to the sprite.
        # Example: A hitbox that's 20 pixels smaller on each side (total 40px smaller width/height)
        # and shifted slightly.
        self.hitbox_offset_x = 20 # Offset from left of sprite
        self.hitbox_offset_y = 10 # Offset from top of sprite
        self.hitbox_width_reduction = 40 # Total reduction from sprite width
        self.hitbox_height_reduction = 20 # Total reduction from sprite height

        self.hitbox = pygame.Rect(
            self.rect.x + self.hitbox_offset_x,
            self.rect.y + self.hitbox_offset_y,
            self.rect.width - self.hitbox_width_reduction,
            self.rect.height - self.hitbox_height_reduction
        )
        # --- END HITBOX ADDITIONS ---

        # Movement variables
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = True
        self.jump_strength = -20

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

    def _load_all_sprites(self):
        # ... (your existing _load_all_sprites method) ...
        sprite_sheet_path = ""
        if self.character_name == "The Boat Man":
            sprite_sheet_path = "sprites/test_punching.jpg"
        elif self.character_name == "The Log Lady":
            sprite_sheet_path = "sprites/EmployeePlaceHolder_Female.jpg"

        try:
            self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        except pygame.error as e:
            print(f"Error loading sprite sheet ({sprite_sheet_path}): {e}")
            placeholder = pygame.Surface((150, 150), pygame.SRCALPHA)
            color = config.BLUE if self.is_player_controlled else config.RED
            pygame.draw.circle(placeholder, color, (75, 75), 75)
            font = pygame.font.Font(None, 20)
            text = font.render("NO IMG", True, config.WHITE)
            text_rect = text.get_rect(center=(75, 75))
            placeholder.blit(text, text_rect)
            self.animations["idle"] = [placeholder]
            self.image = self.animations["idle"][0]
            return

        frame_width = 150
        frame_height = 150

        self.animations["idle"] = []
        for i in range(2):
            frame = self.sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            self.animations["idle"].append(frame)

        self.animations["basic_attack"] = []
        self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(2 * frame_width, 0, frame_width, frame_height)))
        self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(3 * frame_width, 0, frame_width, frame_height)))
        self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(0 * frame_width, frame_height, frame_width, frame_height)))
        self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(1 * frame_width, frame_height, frame_width, frame_height)))
        self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(2 * frame_width, frame_height, frame_width, frame_height)))
        self.animations["basic_attack"].append(self.sprite_sheet.subsurface(pygame.Rect(3 * frame_width, frame_height, frame_width, frame_height)))
        
        self.animations["walking"] = []
        start_row_walk = 2 * frame_height
        for i in range(4):
             frame = self.sprite_sheet.subsurface(pygame.Rect(i * frame_width, start_row_walk, frame_width, frame_height))
             self.animations["walking"].append(frame)

        self.animations["jumping"] = []
        if self.animations["idle"]:
            self.animations["jumping"].append(self.animations["idle"][0])
        else:
            self.animations["jumping"].append(pygame.Surface((frame_width, frame_height), pygame.SRCALPHA))

    def update(self):
        # ... (your existing update method) ...

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
                if self.vel_x == 0 and self.on_ground:
                    self.state = "idle" 
                elif self.vel_x != 0 and self.on_ground:
                    self.state = "walking"
                elif not self.on_ground:
                    self.state = "jumping"
                self.has_dealt_hit_this_attack = False

        # Handle basic attack cooldown
        if self.last_hit_by_basic_attack > 0:
            self.last_hit_by_basic_attack -= 1

        # --- UPDATE HITBOX POSITION ---
        # Update the hitbox position to follow the sprite's rect
        self.hitbox.x = self.rect.x + self.hitbox_offset_x
        self.hitbox.y = self.rect.y + self.hitbox_offset_y
        # --- END UPDATE HITBOX POSITION ---

        # ANIMATION UPDATE LOGIC
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            if self.state in self.animations and self.animations[self.state]:
                self.current_frame = (self.current_frame + 1) % len(self.animations[self.state])
                self.image = self.animations[self.state][self.current_frame]
            else:
                self.image = self.animations.get("idle", [pygame.Surface((150, 150), pygame.SRCALPHA)])[0]
                self.current_frame = 0
            
            if self.vel_x < 0:
                self.image = pygame.transform.flip(self.image, True, False)

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
        # ... (your existing attack method) ...
        if self.is_attacking or self.attack_cooldown > 0:
            return None

        self.is_attacking = True
        self.state = attack_type
        self.current_frame = 0
        self.attack_cooldown = 60
        self.has_dealt_hit_this_attack = False

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
        # ... (your existing take_damage method, likely where hitbox collision check happens) ...
        # IMPORTANT: When checking for collisions with other players/entities,
        # you should now use self.hitbox instead of self.rect.
        if not self.is_attacking:
            self.health -= amount
            if self.health < 0:
                self.health = 0
            print(f"{self.character_name} takes {amount} damage! Health: {self.health}")
            return True
        return False

    def handle_ai(self, player_rect, player_is_attacking):
        # ... (your existing handle_ai method) ...
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