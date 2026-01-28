# fightingLogic/fightingLogic.py
import pygame
import config
import random

def draw_controls_overlay(screen):
    """Draws the control instructions on the screen."""
    font = pygame.font.SysFont("Arial", 28, bold=True)
    
    overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 190))  
    screen.blit(overlay, (0, 0))

    # Show game controls on screen
    controls = [
        ("MOVE", "A / S Keys"),
        ("JUMP", "Spacebar"),
        ("BASIC ATTACK", "Left Click / J"),
        ("MID / SUPER", "W / E Keys")
    ]

    for i, (action, key) in enumerate(controls):
        color = (255, 255, 255) if action != "" else (255, 215, 0)
        text_surf = font.render(f"{action}   {key}", True, color)
        text_rect = text_surf.get_rect(center=(config.SCREEN_WIDTH // 2, 200 + (i * 45)))
        screen.blit(text_surf, text_rect)

class Spritesheet:
    def __init__(self, filename):
        try:
            self.sprite_sheet = pygame.image.load(filename).convert_alpha()
        except:
            self.sprite_sheet = None

    def get_sprite(self, x, y, w, h):
        if not self.sprite_sheet: return None
        sprite = pygame.Surface((w, h), pygame.SRCALPHA)
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, character_name, initial_x, initial_y, is_player_controlled=True):
        super().__init__()
        self.character_name = character_name
        self.is_player_controlled = is_player_controlled
        self.animations = {}
        self.current_frame = 0
        self.animation_speed = 8 # Slightly slower for smoother looks
        self.animation_timer = 0
        
        self._load_all_sprites()
        
        # Initial image setup
        self.image = self.animations["idle"][0]
        self.rect = self.image.get_rect(midbottom=(initial_x, initial_y))

        # Hitbox (The area where the player GETS hit)
        self.hitbox = pygame.Rect(0, 0, 50, 80) 
        
        # Attack Hitbox (The area where the player DEALS damage)
        self.attack_hitbox = None
        self.attack_hitbox_width = 70
        self.attack_hitbox_height = 40

        # Stats
        self.health = 45
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = True
        self.facing_right = True
        self.state = "idle"
        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_hit_count = 0
        self.has_dealt_hit_this_attack = False
        
        self.BASIC_ATTACK_DAMAGE = 5
        self.MID_ATTACK_DAMAGE = 10
        self.SUPER_ATTACK_DAMAGE = 15
        self.MID_ATTACK_THRESHOLD = 5
        self.SUPER_ATTACK_THRESHOLD = 10
        self.last_hit_by_basic_attack = 0

    def _load_all_sprites(self):
        w, h = 100, 100
        path = None
        
        if self.character_name == "The Boat Man":
            path = "sprites/male_punch.png"
        elif self.character_name == "The Log Lady":
            path = "sprites/test_punching_female.png"

        sheet = Spritesheet(path) if path else None

        if sheet and sheet.sprite_sheet:
            self.animations["idle"] = [sheet.get_sprite(5, 10, w, h)]
            self.animations["basic_attack"] = [sheet.get_sprite(5 + (i*w), 10, w, h) for i in range(4)]
            self.animations["walking"] = [self.animations["idle"][0]]
            self.animations["jumping"] = [self.animations["idle"][0]]
            # Add placeholders for mid/super so they don't crash
            self.animations["mid"] = self.animations["basic_attack"]
            self.animations["super"] = self.animations["basic_attack"]
        else:
            self._load_chicken_fallback(w, h)

    def _load_chicken_fallback(self, w, h):
        # Create a simple colored square if the chicken file is also missing
        fallback = pygame.Surface((w, h), pygame.SRCALPHA)
        fallback.fill((255, 0, 255, 180)) # Purple error color
        
        states = ["idle", "basic_attack", "walking", "jumping", "mid", "super"]
        for s in states:
            self.animations[s] = [fallback]

    def update(self):
        # Direction
        if self.vel_x > 0: self.facing_right = True
        elif self.vel_x < 0: self.facing_right = False

        # Physics
        if not self.on_ground:
            self.vel_y += config.GRAVITY
        
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Floor
        if self.rect.bottom >= config.SCREEN_HEIGHT - config.GROUND_HEIGHT:
            self.rect.bottom = config.SCREEN_HEIGHT - config.GROUND_HEIGHT
            self.vel_y = 0
            self.on_ground = True

        # Sync Hitbox to Sprite center
        self.hitbox.center = self.rect.center

        # Handle Attack State
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            if self.attack_cooldown == 0:
                self.is_attacking = False
                self.attack_hitbox = None
                self.state = "idle"
        
        if self.last_hit_by_basic_attack > 0:
            self.last_hit_by_basic_attack -= 1

        self._animate()

    def _animate(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            frames = self.animations.get(self.state, self.animations["idle"])
            self.current_frame = (self.current_frame + 1) % len(frames)
            
            img = frames[self.current_frame]
            if not self.facing_right:
                self.image = pygame.transform.flip(img, True, False)
            else:
                self.image = img

    def move(self, direction):
        if not self.is_attacking:
            self.vel_x = direction * config.PLAYER_SPEED
            if self.on_ground: self.state = "walking"

    def stop_move(self):
        self.vel_x = 0
        if self.on_ground and not self.is_attacking: self.state = "idle"

    def jump(self):
        if self.on_ground:
            self.vel_y = -15 # Jump strength
            self.on_ground = False
            self.state = "jumping"

    def attack(self, attack_type="basic"):
        if self.is_attacking: return
        
        self.is_attacking = True
        self.state = "basic_attack" # Map mid/super to this animation for now
        self.current_frame = 0
        self.attack_cooldown = 30
        self.has_dealt_hit_this_attack = False

        # Position the hitbox in front of the player
        side = self.rect.right if self.facing_right else self.rect.left - self.attack_hitbox_width
        self.attack_hitbox = pygame.Rect(side, self.rect.centery, self.attack_hitbox_width, self.attack_hitbox_height)

    def take_damage(self, amount):
        # Only take damage if not currently attacking (defense bonus)
        if not self.is_attacking:
            self.health -= amount
            return True
        return False

    def handle_ai(self, player_rect, player_is_attacking):
        if self.is_player_controlled: return None
        
        # Calculate center-to-center distance
        dist_x = player_rect.centerx - self.rect.centerx
        abs_dist = abs(dist_x)
        
        # --- AI TUNING CONSTANTS ---
        attack_range = 65    # Distance at which AI starts swinging
        stop_threshold = 55  # AI will keep walking until it reaches this "sweet spot"
        
        # 1. Decision: Attack if in range
        if abs_dist <= attack_range:
            self.stop_move() # Stop walking to perform the attack
            # Use a random check so it doesn't spam perfectly every frame
            if random.random() < 0.03: 
                return "basic_attack"
        
        # 2. Decision: Move if too far
        elif abs_dist > stop_threshold:
            # Move toward player
            direction = 1 if dist_x > 0 else -1
            self.move(direction)
            
        # 3. Decision: Standing still (already at the sweet spot)
        else:
            self.stop_move()

        # 4. Optional: Random Jump logic
        if self.on_ground and random.random() < 0.005:
            self.jump()
        return None
