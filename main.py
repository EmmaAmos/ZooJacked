#main.py
import pygame

# --- Game Initialization ---
 #these two must come first
pygame.init()
pygame.font.init()

#before these
import config
import screens
import stages
import levelSelectMap
import stages.BoatRideTutorial
import stages.stage1 
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Zoo-Jacked")

screens.load_game_assets()
screens.setup_character_select_rects()

level_select_map = levelSelectMap.LevelSelectMap()

# Game state variables
current_screen = "main_menu"
selected_character = None
running = True

# --- Main Game Loop ---
while running:
    mouse_pos = pygame.mouse.get_pos()

    # 1. EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # --- Main Menu Logic ---
            if current_screen == "main_menu":
                if screens.story_button_rect.collidepoint(mouse_pos):
                    current_screen = "story_mode"
                elif screens.levels_button_rect.collidepoint(mouse_pos):
                    current_screen = "level_select"

            # --- Character Selection Logic ---
            elif current_screen == "story_mode":
                if screens.male_character_rect.collidepoint(mouse_pos):
                    selected_character = "The Boat Man"
                    current_screen = "level_select"
                elif screens.female_character_rect.collidepoint(mouse_pos):
                    selected_character = "The Log Lady"
                    current_screen = "level_select"

            # --- Level Selection Logic ---
            elif current_screen == "level_select":
                action_result = level_select_map.handle_click(mouse_pos)

                if action_result:
                    if action_result == "character_select":
                        current_screen = "story_mode"
                    else:
                        # Identify the level
                        level_name = action_result
                        selected_level_info = level_select_map.get_level_info(level_name)

                        if selected_level_info:
                            # 1. Determine Opponent
                            opponent = "Kangaroo" if level_name == "Kangaroo Boogaloo" else "The Log Lady"
                            
                            # 2. Pick the right Stage Module
                            stage_class = selected_level_info.get("module")
                            
                            # 3. LAUNCH THE STAGE
                            # This is where the game "pauses" main.py and runs the fight
                            try:
                                if stage_class == stages.BoatRideTutorial:
                                    current_stage = stages.BoatRideTutorial.BoatRideTutorial(screen, selected_character, opponent)
                                else:
                                    current_stage = stages.stage1.Stage1(screen, selected_character, opponent)
                                
                                # This .run() call handles the "Press Enter to Start" and the fight
                                result = current_stage.run() 
                                
                                if result == "quit":
                                    running = False
                                current_screen = "level_select" # Return here after fight
                            except Exception as e:
                                print(f"Error launching stage: {e}")

    # 2. UPDATE LOGIC (Main Menu animations/hovers)
    if current_screen == "level_select":
        level_select_map.update(mouse_pos)

    # 3. DRAWING LOGIC
    screen.fill(config.BLACK)

    if current_screen == "main_menu":
        screens.draw_main_menu(screen)
    elif current_screen == "story_mode":
        screens.draw_character_select_screen(screen, selected_character)
    elif current_screen == "level_select":
        level_select_map.draw(screen)
    elif current_screen == "game_over":
        screens.draw_game_over_screen(screen)

    pygame.display.flip()

pygame.quit()