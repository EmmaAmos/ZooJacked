# main.py
import pygame

# Initialize Pygame (main modules)
pygame.init()
pygame.font.init()
import stages.BoatRideTutorial
import config
import screens
import stages
import levelSelectMap 

# --- Game Initialization ---

# Set up the display
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Zoo-Jacked")

# Load all assets (images) managed by the screens module
screens.load_game_assets()
screens.setup_character_select_rects() # Ensure this runs AFTER images are loaded

# Create an instance of the LevelSelectMap
# Consolidating to one instance variable name
level_select_map = levelSelectMap.LevelSelectMap()

# Game state variables
current_screen = "main_menu"
selected_character = None
# selected_level_info will be populated when a level is clicked
# level_name will be populated when a level is clicked
current_stage_instance = None # To hold the active stage object when playing a level

# --- Main Game Loop ---
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    # --- Event Handling ---
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
                    current_screen = "level_select" # Move to level select after character pick
                elif screens.female_character_rect.collidepoint(mouse_pos):
                    selected_character = "The Log Lady"
                    print(f"{selected_character} selected!")
                    current_screen = "level_select" # Move to level select after character pick
            elif current_screen == "level_select":
                action_result = level_select_map.handle_click(mouse_pos)

                if action_result: # Check if something was clicked (not None)
                    if action_result == "character_select":
                        # Transition back to character select screen from menu
                        current_screen = "story_mode" # "story_mode" is your character select
                        print("DEBUG: Transitioning to character select screen from level select menu.")
                    else: # It's a level name that was clicked
                        level_name = action_result # Store the level name
                        selected_level_info = level_select_map.get_level_info(level_name)

                        if selected_level_info: # Ensure level info was actually found
                            print(f"Selected Level: {selected_level_info['level_num']} ({level_name})")

                            # --- Level Specific Logic ---
                            # Check if the selected level is the BoatRideTutorial
                            if selected_level_info.get("module") == stages.BoatRideTutorial:
                                # Determine the opponent based on the selected character
                                opponent_character = None
                                if selected_character == "The Boat Man":
                                    opponent_character = "The Log Lady"
                                elif selected_character == "The Log Lady":
                                    opponent_character = "The Boat Man"

                                # Create and run the stage instance with character info
                                # Ensure your stages.BoatRideTutorial.BoatRideTutorial class
                                # accepts these arguments in its __init__ method.
                                current_stage_instance = stages.BoatRideTutorial.BoatRideTutorial(
                                    screen, selected_character, opponent_character
                                )
                                # The .run() method should contain its own game loop and return when done.
                                current_stage_instance.run() # This will block until the stage exits

                                # After the stage finishes, return to level select
                                current_screen = "level_select"
                                print(f"Exiting {level_name}. Returning to level select.")
                            else:
                                # For other stages not yet implemented with specific character logic,
                                # transition to a generic game_play placeholder or more advanced stage handling.
                                current_screen = "game_play" # Transition to game_play placeholder
                                print(f"Starting generic game_play for {level_name}.")
                        else:
                            print(f"Error: Could not find info for level '{level_name}'")

    # --- Update Logic (for the currently active screen) ---
    if current_screen == "level_select":
        level_select_map.update(mouse_pos) # Update level select map for hovers, etc.
    # Add other update logic for different screens if they have dynamic elements
    # elif current_screen == "game_play" and current_stage_instance:
    #     current_stage_instance.update() # If your stages have an update method outside their run()

    # --- Drawing Logic (for the currently active screen) ---
    screen.fill(config.BLACK) # Clear the screen each frame

    if current_screen == "main_menu":
        screens.draw_main_menu(screen)
    elif current_screen == "story_mode": # This is now the character selection screen
        screens.draw_character_select_screen(screen, selected_character)
    elif current_screen == "level_select":
        level_select_map.draw(screen) # Draw the level map using the single instance
    elif current_screen == "game_play": # This block now only runs if a non-tutorial level is selected
        # This section is your placeholder for other stages.
        # You'll expand this later to dynamically load and run other stages.
        screen.fill(config.WHITE)
        font = pygame.font.Font(None, 50)
        game_text = font.render(f"Playing as {selected_character} in {level_name} (Stage Not Fully Implemented)!", True, config.BLACK)
        game_text_rect = game_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
        screen.blit(game_text, game_text_rect)
    elif current_screen == "game_over":
        screens.draw_game_over_screen(screen)
    # Add more `elif` conditions for other screens as you implement them

    pygame.display.flip() # Update the full display Surface to the screen

pygame.quit() # Uninitialize pygame modules