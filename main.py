import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Zoo-Jacked")

# --- Load Images ---
try:
    boot_up_screen_img = pygame.image.load("assests/bootUpscreen.jpg").convert()
    dialog_bg_img = pygame.image.load("assests/DiologBG.jpg").convert()

    # Load character images from the 'sprites' folder
    # IMPORTANT: Ensure EmployeePlaceHolder_Female.jpg is actually a JPG/PNG
    # and not an AVIF, as Pygame doesn't support AVIF natively.
    # Use .convert_alpha() if images have transparency, otherwise .convert() is fine.
    raw_male_character_img = pygame.image.load("sprites/EmployeePlaceHolder_Male.jpg").convert_alpha()
    raw_female_character_img = pygame.image.load("sprites/EmployeePlaceHolder_Female.jpg").convert_alpha()

except pygame.error as e:
    print(f"Error loading image: {e}")
    print("Please ensure your image files are in the correct folders ('assests' or 'sprites') and named correctly.")
    pygame.quit()
    exit()

# --- Set up Fonts and Text ---
main_title_font = pygame.font.Font(None, 100)
button_font = pygame.font.Font(None, 50)
# character_button_font is no longer strictly needed if no text on character buttons
# but keeping it in case you want to add names below the characters later.
character_button_font = pygame.font.Font(None, 40)

# Colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Main Menu Title
main_title_text_surface = main_title_font.render("Zoo-jacked", True, RED)
main_title_text_rect = main_title_text_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 100))

# --- Button Properties (Main Menu) ---
button_width, button_height = 200, 60
button_radius = 10

# --- Main Menu Button Positions and Text ---
story_button_rect = pygame.Rect(screen_width // 2 - button_width - 20, 500, button_width, button_height)
levels_button_rect = pygame.Rect(screen_width // 2 + 20, 500, button_width, button_height)

story_text_surface = button_font.render("Story Mode", True, BLACK)
levels_text_surface = button_font.render("Levels", True, BLACK)

# --- Character Selection Screen Elements ---

# Define the desired size for character images
CHAR_IMG_WIDTH = 200 # Example width
CHAR_IMG_HEIGHT = 200 # Example height

# Scale the character images
male_character_img = pygame.transform.scale(raw_male_character_img, (CHAR_IMG_WIDTH, CHAR_IMG_HEIGHT))
female_character_img = pygame.transform.scale(raw_female_character_img, (CHAR_IMG_WIDTH, CHAR_IMG_HEIGHT))

# Calculate positions to center them side-by-side
# Total width occupied by both images + space between them
total_char_display_width = CHAR_IMG_WIDTH * 2 + 50 # 50 pixels space between them
start_x = (screen_width - total_char_display_width) // 2
display_y = screen_height // 2 - CHAR_IMG_HEIGHT // 2 # Vertically centered

# Get Rects for collision detection and blitting
# These rects will be used for both drawing AND click detection
male_character_rect = male_character_img.get_rect(topleft=(start_x, display_y))
female_character_rect = female_character_img.get_rect(topleft=(start_x + CHAR_IMG_WIDTH + 50, display_y))

# NO MORE SEPARATE BUTTON RECTS FOR CHARACTER SELECTION - THE IMAGE RECTS ARE USED

# Game state
current_screen = "main_menu"
selected_character = None

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if current_screen == "main_menu":
                if story_button_rect.collidepoint(mouse_pos):
                    current_screen = "story_mode"
                elif levels_button_rect.collidepoint(mouse_pos):
                    print("Levels button clicked!")
            elif current_screen == "story_mode":
                # Check for clicks on the character image RECTS
                if male_character_rect.collidepoint(mouse_pos):
                    selected_character = "The Boat Man"
                    print("Male character selected!")
                    # You can transition to the next game state here if selection is final
                    # For example: current_screen = "game_start"
                elif female_character_rect.collidepoint(mouse_pos):
                    selected_character = "The Log Lady"
                    print("Female character selected!")
                    # You can transition to the next game state here if selection is final
                    # For example: current_screen = "game_start"

    # --- Drawing Logic ---
    if current_screen == "main_menu":
        screen.blit(boot_up_screen_img, (0, 0))
        screen.blit(main_title_text_surface, main_title_text_rect)

        pygame.draw.rect(screen, YELLOW, story_button_rect, border_radius=button_radius)
        pygame.draw.rect(screen, YELLOW, levels_button_rect, border_radius=button_radius)

        # Optional: Debugging borders (remove after testing)
        pygame.draw.rect(screen, (0, 255, 0), story_button_rect, 3, border_radius=button_radius)
        pygame.draw.rect(screen, (0, 0, 255), levels_button_rect, 3, border_radius=button_radius)

        screen.blit(story_text_surface, story_text_surface.get_rect(center=story_button_rect.center))
        screen.blit(levels_text_surface, levels_text_surface.get_rect(center=levels_button_rect.center))

    elif current_screen == "story_mode":
        screen.blit(dialog_bg_img, (0, 0)) # Draw background first

        # Display character images using their calculated rects
        screen.blit(male_character_img, male_character_rect)
        screen.blit(female_character_img, female_character_rect)

        # NO MORE DRAWING OF SEPARATE CHARACTER BUTTONS OR THEIR TEXT HERE

        # Optionally, display which character was selected
        if selected_character:
            selected_text = button_font.render(f"Selected: {selected_character}", True, BLACK)
            selected_text_rect = selected_text.get_rect(center=(screen_width // 2, 100))
            pygame.draw.rect(screen, WHITE, selected_text_rect.inflate(20, 10), border_radius=5)
            screen.blit(selected_text, selected_text_rect)

    # Update the display for the current frame
    pygame.display.flip()

# Quit Pygame
pygame.quit()