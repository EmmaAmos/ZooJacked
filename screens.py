# screens.py
import pygame
import config # Import our config file

# --- Image Loading (Now loaded centrally, but still managed in screens.py init) ---
# We'll keep these global variables as the loaded surfaces
boot_up_screen_img = None
dialog_bg_img = None
male_character_img = None
female_character_img = None

# LevelSelectMap instance
level_select_map = None # Will be initialized in main.py

# LevelSelectMap instance
level_select_map = None # Will be initialized in main.py

def load_game_assets():
    """Loads and scales all necessary game images."""
    global boot_up_screen_img, dialog_bg_img, male_character_img, female_character_img
    try:
        boot_up_screen_img = pygame.image.load("assests/bootUpscreen.jpg").convert()
        dialog_bg_img = pygame.image.load("assests/DiologBG.jpg").convert()

        # Assuming EmployeePlaceHolder_Female.bmp is a JPG/PNG now
        raw_male_character_img = pygame.image.load("sprites/EmployeePlaceHolder_Male.png").convert_alpha()
        raw_female_character_img = pygame.image.load("sprites/EmployeePlaceHolder_Female.bmp").convert_alpha()

        # These lines need to be consistently indented, typically 4 spaces from the 'try'
        male_character_img = raw_male_character_img
        female_character_img = raw_female_character_img

    except pygame.error as e:
        print(f"Error loading image: {e}")
        print("Please ensure your image files are in the correct folders ('assests' or 'sprites') and named correctly.")
        pygame.quit()
        exit()

# --- Initial Setup for Screens ---
# Fonts
main_title_font = pygame.font.Font(None, config.FONT_SIZE_MAIN_TITLE)
button_font = pygame.font.Font(None, config.FONT_SIZE_BUTTON)
character_button_font = pygame.font.Font(None, config.FONT_SIZE_CHAR_BUTTON)

# Main Menu Text Surfaces
main_title_text_surface = main_title_font.render("Zoo-jacked", True, config.RED)
main_title_text_rect = main_title_text_surface.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 100))

story_text_surface = button_font.render("Story Mode", True, config.BLACK)
levels_text_surface = button_font.render("Levels", True, config.BLACK)

# Main Menu Button Rects
story_button_rect = pygame.Rect(config.SCREEN_WIDTH // 2 - config.BUTTON_WIDTH - 20, 500, config.BUTTON_WIDTH, config.BUTTON_HEIGHT)
levels_button_rect = pygame.Rect(config.SCREEN_WIDTH // 2 + 20, 500, config.BUTTON_WIDTH, config.BUTTON_HEIGHT)

# Character Select Image Rects (initialized after images are loaded)
male_character_rect = None
female_character_rect = None

def setup_character_select_rects():
    """Calculates and sets up rects for character images after they are loaded."""
    global male_character_rect, female_character_rect
    total_char_display_width = config.CHAR_IMG_WIDTH * 2 + config.CHAR_SPACING
    start_x = (config.SCREEN_WIDTH - total_char_display_width) // 2
    display_y = config.SCREEN_HEIGHT // 2 - config.CHAR_IMG_HEIGHT // 2

    male_character_rect = male_character_img.get_rect(topleft=(start_x, display_y))
    female_character_rect = female_character_img.get_rect(topleft=(start_x + config.CHAR_IMG_WIDTH + config.CHAR_SPACING, display_y))

# --- Main Menu Screen Drawing Function ---
def draw_main_menu(screen):
    """Draws the main menu screen elements."""
    screen.blit(boot_up_screen_img, (0, 0))
    screen.blit(main_title_text_surface, main_title_text_rect)

    pygame.draw.rect(screen, config.YELLOW, story_button_rect, border_radius=config.BUTTON_RADIUS)
    pygame.draw.rect(screen, config.YELLOW, levels_button_rect, border_radius=config.BUTTON_RADIUS)

    pygame.draw.rect(screen, config.GREEN, story_button_rect, 3, border_radius=config.BUTTON_RADIUS) # Debug border
    pygame.draw.rect(screen, config.BLUE, levels_button_rect, 3, border_radius=config.BUTTON_RADIUS) # Debug border

    screen.blit(story_text_surface, story_text_surface.get_rect(center=story_button_rect.center))
    screen.blit(levels_text_surface, levels_text_surface.get_rect(center=levels_button_rect.center))

# --- Story Mode (Character Selection) Screen Drawing Function ---
def draw_character_select_screen(screen, selected_character):
    """Draws the character selection screen elements."""
    screen.blit(dialog_bg_img, (0, 0))

    screen.blit(male_character_img, male_character_rect)
    screen.blit(female_character_img, female_character_rect)

    if selected_character:
        selected_text = button_font.render(f"Selected: {selected_character}", True, config.BLACK) # Corrected!
        selected_text_rect = selected_text.get_rect(center=(config.SCREEN_WIDTH // 2, 100))
        pygame.draw.rect(screen, config.WHITE, selected_text_rect.inflate(20, 10), border_radius=5)
        screen.blit(selected_text, selected_text_rect)

# --- Game Over/Level Cleared (Example, not implemented yet) ---
def draw_game_over_screen(screen):
    screen.fill(config.BLACK)
    font = pygame.font.Font(None, 74)
    text_surface = font.render("Game Over!", True, config.RED)
    text_rect = text_surface.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
    screen.blit(text_surface, text_rect)