from main import Character, character  # Importing Character and character from main.py
from sprites import Enemy  # Importing only Enemy from sprites.py

class FightingLogic:
    def __init__(self, player_character: Character, enemy: Enemy):
        self.player = player_character
        self.enemy = enemy

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:  # Move forward
                self.player.move_forward()
            elif event.key == pygame.K_a:  # Move backward
                self.player.move_backward()
            elif event.key == pygame.K_SPACE:  # Jump
                self.player.jump()
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Punch
            self.player.punch()
            self.check_punch_collision()

    def check_punch_collision(self):
        # Check if the player's punch hits the enemy
        if self.player.is_punching and self.player.hitbox.colliderect(self.enemy.hitbox):
            self.enemy.take_damage()

        # Check if the enemy punches the player
        if self.enemy.is_punching and self.enemy.hitbox.colliderect(self.player.hitbox):
            self.player.take_damage()

# Example usage in main.py
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # Initialize player and enemy
    player = Character(x=100, y=300)  # Example starting position
    enemy = Enemy(x=500, y=300)  # Example starting position
    logic = FightingLogic(player, enemy)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            logic.handle_input(event)

        # Update game state
        player.update()
        enemy.update()

        # Render game
        screen.fill((0, 0, 0))  # Clear screen with black
        player.draw(screen)
        enemy.draw(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
