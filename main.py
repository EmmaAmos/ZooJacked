# main.py
import pygame

# Initialize Pygame (main modules)
pygame.init()
pygame.font.init()

import config
import screens
import levelSelectMap

# Set up the display
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Zoo-Jacked")

# Load all assets (images) managed by the screens module
screens.load_game_assets()
screens.setup_character_select_rects()

# Create an instance of the LevelSelectMap
level_map_instance = levelSelectMap.LevelSelectMap()

# Game state variables
current_screen = "main_menu"
selected_character = None
selected_level_info = None # Store the full info dictionary for the selected level

# Main game loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "main_menu":
                if screens.story_button_rect.collidepoint(mouse_pos):
                    current_screen = "story_mode"
                elif screens.levels_button_rect.collidepoint(mouse_pos):
                    current_screen = "level_select"
                    print("Levels button clicked (going to level select)!")
            elif current_screen == "story_mode":
                if screens.male_character_rect.collidepoint(mouse_pos):
                    selected_character = "The Boat Man"
                    print(f"{selected_character} selected!")
                    current_screen = "level_select"
                elif screens.female_character_rect.collidepoint(mouse_pos):
                    selected_character = "The Log Lady"
                    print(f"{selected_character} selected!")
                    current_screen = "level_select"
            elif current_screen == "level_select":
                level_name = level_map_instance.handle_click(mouse_pos)
                if level_name:
                    selected_level_info = level_map_instance.get_level_info(level_name)
                    print(f"Selected Level: {selected_level_info['level_num']} ({level_name})")
                    current_screen = "game_play" # Transition to game_play

    # --- Update Logic ---
    if current_screen == "level_select":
        level_map_instance.update(mouse_pos) # Update the map for hover effects
    # Add other update logic for different screens here if needed

    # --- Drawing Logic ---
    if current_screen == "main_menu":
        screens.draw_main_menu(screen)
    elif current_screen == "story_mode":
        screens.draw_character_select_screen(screen, selected_character)
    elif current_screen == "level_select":
        level_map_instance.draw(screen)
    elif current_screen == "game_play":
        # Check if a character and level are selected before attempting to run the stage
        if selected_character and selected_level_info and selected_level_info.get("module"):
            # Call a function from the selected stage module
            # We assume each stage module has a 'run_stage' function
            # that takes the screen and selected character as arguments.
            # This function should contain the main game loop for that stage
            # and return when the stage is over (e.g., player wins/loses or exits).
            print(f"Starting {selected_level_info['name']} with {selected_character}...")
            
            # Here, you would call the main function of your stage.
            # For this to work, each stage file (e.g., stages/stage1.py)
            # needs a function that handles its gameplay loop.
            # Example: selected_level_info["module"].run_stage(screen, selected_character)
            
            # For now, let's just keep the placeholder text
            screen.fill(config.WHITE)
            font = pygame.font.Font(None, 50)
            game_text = font.render(f"Playing as {selected_character} in {selected_level_info['name']}!", True, config.BLACK)
            game_text_rect = game_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
            screen.blit(game_text, game_text_rect)
            
            # IMPORTANT: Your actual stage loop will need to manage its own events and drawing
            # and eventually set 'current_screen' back to 'level_select' or 'game_over'
            # when it finishes. This structure needs a "stage manager" or robust state machine.
            # For now, this is just a placeholder display.
        else:
            # Handle cases where level info or character is missing
            screen.fill(config.RED)
            error_font = pygame.font.Font(None, 40)
            error_text = error_font.render("Error: Character or Level not fully selected!", True, config.WHITE)
            error_rect = error_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
            screen.blit(error_text, error_rect)

    elif current_screen == "game_over":
        screens.draw_game_over_screen(screen)

    # Update the display for the current frame
    pygame.display.flip()

# Quit Pygame
pygame.quit()