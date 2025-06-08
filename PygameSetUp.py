import pygame

# 1. Initialize Pygame
pygame.init()

# 2. Set up the game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Street Fighter Game")

# 3. Game variables
FPS = 60
clock = pygame.time.Clock()

# 4. Load assets (your images!)
background_stage_1 = pygame.image.load("/c:/Users/elove/Desktop/MyOwnWebsites/ZooJacked/assets/Stage_1.webp").convert()
male_character_placeholder = pygame.image.load("/c:/Users/elove/Desktop/MyOwnWebsites/ZooJacked/assets/EmployeePlaceHolder_Male.jpg").convert_alpha()
female_character_placeholder = pygame.image.load("/c:/Users/elove/Desktop/MyOwnWebsites/ZooJacked/assets/EmployeePlaceHolder_Female.jpg").convert_alpha()

# You'll likely want a function or class to manage loading all your stage backgrounds
# and character sprites as you get more detailed.

# 5. Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Handle player input (keyboard presses for movement, attacks, etc.)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
            print("Jump animation triggered")  # Replace with actual jump animation logic
            elif event.key == pygame.K_d:
            print("Walk forward animation triggered")  # Replace with actual walk forward logic
            elif event.key == pygame.K_a:
            print("Walk backward animation triggered")  # Replace with actual walk backward logic

    # 6. Update game state (character positions, health, attack states, etc.)
    # This is where your game logic will go.

    # Example: Update character positions
    # Define initial positions for characters if not already defined
    if 'male_x' not in locals():
        male_x, male_y = 100, 400  # Initial position for male character
    if 'female_x' not in locals():
        female_x, female_y = 600, 400  # Initial position for female character

    # Movement logic (placeholder)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:  # Move male character to the right
        male_x += 5
    if keys[pygame.K_a]:  # Move male character to the left
        male_x -= 5
    if keys[pygame.K_RIGHT]:  # Move female character to the right
        female_x += 5
    if keys[pygame.K_LEFT]:  # Move female character to the left
        female_x -= 5

    # Ensure characters stay within screen bounds
    male_x = max(0, min(SCREEN_WIDTH - male_character_placeholder.get_width(), male_x))
    female_x = max(0, min(SCREEN_WIDTH - female_character_placeholder.get_width(), female_x))

    # Placeholder for health or attack state updates
    print(f"Male character position: ({male_x}, {male_y})")
    print(f"Female character position: ({female_x}, {female_y})")

    # 7. Draw everything
    screen.fill((0, 0, 0)) # Fill screen with black, or draw your background
    # screen.blit(background_stage_1, (0,0)) # Draw current stage background
    # screen.blit(male_character_placeholder, (x, y)) # Draw characters
    # screen.blit(female_character_placeholder, (x2, y2))

    pygame.display.flip() # Update the full display Surface to the screen

    # 8. Control frame rate
    clock.tick(FPS)

# 9. Quit Pygame
pygame.quit()