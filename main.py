# main.py
import pygame

# Initialize Pygame (main modules)
pygame.init()
pygame.font.init()

import config
import screens
import stages

# --- TEMPORARY TEST IMPORTS ---
# Removed the stages.tutorialStage import as it caused an error previously and is likely not needed
# If you still have it in your actual file and it causes issues, remove/comment it out.
# try:
#     import stages.tutorialStage
#     print("stages.tutorialStage imported successfully in main.py!")
# except ModuleNotFoundError as e:
#     print(f"Error importing stages.tutorialStage in main.py: {e}")
# --- END TEMPORARY TEST IMPORTS ---

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
selected_level_info = None
level_name = None

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
                clicked_level_name = level_map_instance.handle_click(mouse_pos)
                if clicked_level_name:
                    level_name = clicked_level_name
                    selected_level_info = level_map_instance.get_level_info(level_name)
                    print(f"Selected Level: {selected_level_info['level_num']} ({level_name})")

                    # --- IMPORTANT CHANGE HERE ---
                    # Now, when transitioning to game_play, determine the opponent
                    # and instantiate the stage with both characters
                    if selected_level_info.get("module") == stages.crocodileCreekTutorial: # Only for this specific tutorial
                        # Determine the opponent based on the selected character
                        opponent_character = None
                        if selected_character == "The Boat Man":
                            opponent_character = "The Log Lady"
                        elif selected_character == "The Log Lady":
                            opponent_character = "The Boat Man"

                        # Create and run the stage instance with character info
                        # Ensure your stages.crocodileCreekTutorial.CrocodileCreekTutorial class
                        # accepts these arguments in its __init__ method.
                        current_stage_instance = stages.crocodileCreekTutorial.CrocodileCreekTutorial(
                            screen, selected_character, opponent_character
                        )
                        current_stage_instance.run() # This will block until the stage exits
                        current_screen = "level_select" # Go back to level select after stage finishes
                    else:
                        # For other stages not yet implemented with character logic,
                        # you might just go to the placeholder screen or raise an error.
                        current_screen = "game_play" # Transition to game_play (for placeholder if no specific stage run)
                    # --- END IMPORTANT CHANGE ---

    # --- Update Logic ---
    if current_screen == "level_select":
        level_map_instance.update(mouse_pos)

    # --- Drawing Logic ---
    if current_screen == "main_menu":
        screens.draw_main_menu(screen)
    elif current_screen == "story_mode":
        screens.draw_character_select_screen(screen, selected_character)
    elif current_screen == "level_select":
        level_map_instance.draw(screen)
    elif current_screen == "game_play": # This block now only runs if the above 'if selected_level_info.get("module") == stages.crocodileCreekTutorial' was FALSE
        # This section is mostly for stages that don't have their 'run' method called directly yet
        # It's your current placeholder for other stages.
        screen.fill(config.WHITE)
        font = pygame.font.Font(None, 50)
        game_text = font.render(f"Playing as {selected_character} in {level_name} (Stage Not Fully Implemented)!", True, config.BLACK)
        game_text_rect = game_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
        screen.blit(game_text, game_text_rect)

    elif current_screen == "game_over":
        screens.draw_game_over_screen(screen)

    pygame.display.flip()

pygame.quit()