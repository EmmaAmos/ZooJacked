# levelSelectMap.py
import pygame
import config

# Importing stages for level selection
import stages.stage1
import stages.stage2
import stages.stage3
import stages.bounusStage
import stages.crocodileCreekTutorial

class LevelSelectMap:
    def __init__(self):
        """
        Initializes the level selection map with available levels and their clickable areas on the map.
        """
        self.map_image = None
        self._load_map_image()

        # Define levels with their names, numbers, and the RECTANGLE on the map image
        # that the player will click to select them.
        # These coordinates are relative to the top-left of the AA_Map.png image.
        self.levels_data = {
            "Crocodile Creek Tutorial": {
                "level_num": 0,
                "map_rect": pygame.Rect(290, 805, 80, 80), # **ADJUST THESE COORDINATES for the purple dot**
                "tooltip": "Crocodile Creek Adventure Tutorial",
                "module": stages.crocodileCreekTutorial, # Pointing to the consolidated tutorial
                "button_color": config.PURPLE # Added color for visual button
            }
        }

        self.map_display_width = config.SCREEN_WIDTH * 0.9
        self.map_display_height = config.SCREEN_HEIGHT * 0.9

        self._load_map_image()
        if self.map_image:
            original_width, original_height = self.map_image.get_size()
            aspect_ratio = original_width / original_height

            if self.map_display_width / aspect_ratio > self.map_display_height:
                self.map_display_width = int(self.map_display_height * aspect_ratio)
            else:
                self.map_display_height = int(self.map_display_width / aspect_ratio)

        self.map_rect_on_screen = pygame.Rect(
            (config.SCREEN_WIDTH - self.map_display_width) // 2,
            (config.SCREEN_HEIGHT - self.map_display_height) // 2,
            self.map_display_width,
            self.map_display_height
        )

        self._scale_level_rects()

        self.hovered_level_name = None
        self.tooltip_font = pygame.font.Font(None, 30)
        self.button_font = pygame.font.Font(None, 24) # Font for button numbers/text

    def _load_map_image(self):
        """Loads the main map image for level selection."""
        try:
            self.map_image = pygame.image.load("assests/AA_Map.png").convert_alpha()
        except pygame.error as e:
            print(f"Error loading map image (assests/AA_Map.png): {e}")
            self.map_image = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            self.map_image.fill(config.RED)
            print("Using a red placeholder for the map image.")

    def _scale_level_rects(self):
        """Scales the defined map_rects to their positions on the actual displayed map."""
        if not self.map_image:
            return

        original_map_width, original_map_height = self.map_image.get_size()

        scale_x = self.map_display_width / original_map_width
        scale_y = self.map_display_height / original_map_height

        for level_name, data in self.levels_data.items():
            original_rect = data["map_rect"]

            scaled_x = int(original_rect.x * scale_x) + self.map_rect_on_screen.x
            scaled_y = int(original_rect.y * scale_y) + self.map_rect_on_screen.y
            scaled_width = int(original_rect.width * scale_x)
            scaled_height = int(original_rect.height * scale_y)

            data["scaled_rect"] = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)

    def handle_click(self, mouse_pos):
        """
        Checks if a level area on the map was clicked.
        :param mouse_pos: (x, y) tuple of the mouse click position.
        :return: The name of the clicked stage (e.g., "Forest") or None.
        """
        for level_name, data in self.levels_data.items():
            if data["scaled_rect"].collidepoint(mouse_pos):
                return level_name
        return None

    def get_level_info(self, level_name):
        """Retrieves the full data for a given level name."""
        return self.levels_data.get(level_name)

    def update(self, mouse_pos):
        """Updates the state, particularly for hover effects/tooltips."""
        self.hovered_level_name = None
        for level_name, data in self.levels_data.items():
            if data["scaled_rect"].collidepoint(mouse_pos):
                self.hovered_level_name = level_name
                break

    def draw(self, screen):
        """
        Draws the level selection map screen.
        :param screen: The Pygame screen surface to draw on.
        """
        screen.fill(config.BLACK)

        if self.map_image:
            scaled_map = pygame.transform.scale(self.map_image, (self.map_display_width, self.map_display_height))
            screen.blit(scaled_map, self.map_rect_on_screen.topleft)

        title_font = pygame.font.Font(None, config.FONT_SIZE_MAIN_TITLE - 20)
        title_surface = title_font.render("Select Your Adventure", True, config.WHITE)
        title_rect = title_surface.get_rect(center=(config.SCREEN_WIDTH // 2, 40))
        screen.blit(title_surface, title_rect)

       # Draw the buttons for each level
        for level_name, data in self.levels_data.items():
            button_rect = data["scaled_rect"]
            button_color = data["button_color"]

            # Check if this is the "Crocodile Creek Tutorial" and if we should make it invisible
            if level_name == "Crocodile Creek Tutorial":
                # Option 1: Skip drawing the button shape and its text entirely
                # Continue to the next level in the loop without drawing anything for this one
                continue # This will skip the rest of the loop for this iteration

                # Option 2 (if you still want a clickable area but no visual button):
                # You don't draw the rect here, but the handle_click logic would still work.
                # If you choose this, remove the 'continue' statement above and just
                # make sure the drawing commands below are within an 'else' block for other levels.
                # However, for true invisibility, 'continue' is cleaner.

            # Highlight if hovered
            if level_name == self.hovered_level_name:
                pygame.draw.rect(screen, config.WHITE, button_rect.inflate(10, 10), border_radius=5) # Background highlight
                pygame.draw.rect(screen, button_color, button_rect, border_radius=5) # Original button
            else:
                pygame.draw.rect(screen, button_color, button_rect, border_radius=5)

            # Draw level number or name on the button
            level_text_surface = self.button_font.render(str(data["level_num"]), True, config.WHITE if level_name == self.hovered_level_name else config.BLACK)
            level_text_rect = level_text_surface.get_rect(center=button_rect.center)
            screen.blit(level_text_surface, level_text_rect)


        if self.hovered_level_name:
            tooltip_text = self.levels_data[self.hovered_level_name]["tooltip"]
            tooltip_surface = self.tooltip_font.render(tooltip_text, True, config.BLACK)

            mouse_x, mouse_y = pygame.mouse.get_pos()
            tooltip_rect = tooltip_surface.get_rect(midbottom=(mouse_x, mouse_y - 5))

            pygame.draw.rect(screen, config.WHITE, tooltip_rect.inflate(10, 5), border_radius=5)
            screen.blit(tooltip_surface, tooltip_rect)
    
    # --- MENU BUTTON ADDITIONS ---
        self.menu_button_rect = pygame.Rect(config.SCREEN_WIDTH - 60, 20, 40, 30) # Top right corner
        self.menu_open = False # State to track if the menu is open

        # Menu options and their rectangles
        self.menu_options = {
            "Options": None,
            "Settings": None,
            "Character Select": None
        }
        self.menu_rect = None # Will be set when menu opens
        self.option_font = pygame.font.Font(None, 30) # Font for menu items
        self._calculate_menu_rects() # Initial calculation of menu dimensions
        # --- END MENU BUTTON ADDITIONS ---

    def _load_levels(self):
        # This function should be in your actual code.
        # Placeholder for demonstration if it's missing from the snippet you provided.
        return {
            "Crocodile Creek Tutorial": {"level_num": 1, "module": config.CROCODILE_CREEK_TUTORIAL_MODULE}
        }

    def _create_level_buttons(self):
        # This function should be in your actual code.
        # Placeholder for demonstration.
        for i, (level_name, level_info) in enumerate(self.levels.items()):
            button_rect = pygame.Rect(50, 100 + i * 70, 200, 50) # Example positioning
            self.level_buttons.append((level_name, button_rect))

    def _calculate_menu_rects(self):
        # Calculate menu dimensions and button positions
        menu_width = 200
        menu_height = len(self.menu_options) * 40 + 20 # 40 per item, 20 for padding
        menu_x = config.SCREEN_WIDTH - menu_width - 20 # 20px from right edge
        menu_y = self.menu_button_rect.bottom + 10 # 10px below the menu button
        self.menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)

        # Calculate individual option rects within the menu
        y_offset = menu_y + 10 # Start 10px from top of menu
        for option_name in self.menu_options:
            text_surface = self.option_font.render(option_name, True, config.WHITE)
            option_rect = text_surface.get_rect(center=(self.menu_rect.centerx, y_offset + text_surface.get_height() // 2))
            # Adjust to be relative to the menu's topleft for drawing, then move
            option_rect.x = menu_x + 10 # 10px padding from left of menu
            self.menu_options[option_name] = option_rect
            y_offset += 40 # 40px spacing for next option

    def handle_click(self, mouse_pos):
        # --- HANDLE MENU BUTTON CLICK ---
        if self.menu_button_rect.collidepoint(mouse_pos):
            self.menu_open = not self.menu_open # Toggle menu open/close
            return None # Don't process other clicks if menu button was clicked

        # --- HANDLE MENU ITEM CLICKS (if menu is open) ---
        if self.menu_open:
            for option_name, option_rect in self.menu_options.items():
                if option_rect.collidepoint(mouse_pos):
                    self.menu_open = False # Close menu after selection
                    if option_name == "Character Select":
                        print("DEBUG: Returning to character select screen.")
                        return "character_select" # Signal back to main.py
                    elif option_name == "Options":
                        print("Options button clicked (future functionality)")
                    elif option_name == "Settings":
                        print("Settings button clicked (future functionality)")
            return None # A menu item was clicked, don't process level clicks

        # --- EXISTING LEVEL BUTTON CLICK LOGIC ---
        for level_name, button_rect in self.level_buttons:
            if button_rect.collidepoint(mouse_pos):
                print(f"Level '{level_name}' button clicked!")
                return level_name
        return None

    def update(self, mouse_pos):
        # No specific update logic for this new feature, but keeping the method signature.
        pass

    def draw(self, screen):
        # Placeholder: Draw background
        screen.fill(config.PURPLE) # Assuming you have a blue sky color in config

        # --- EXISTING LEVEL BUTTON DRAWING ---
        for level_name, button_rect in self.level_buttons:
            pygame.draw.rect(screen, config.LIGHT_GREY, button_rect, border_radius=5)
            pygame.draw.rect(screen, config.DARK_GREY, button_rect, 2, border_radius=5)
            
            font = pygame.font.Font(None, 36)
            text_surface = font.render(level_name, True, config.BLACK)
            text_rect = text_surface.get_rect(center=button_rect.center)
            screen.blit(text_surface, text_rect)

        # --- DRAW MENU BUTTON (Tree Brown Lines) ---
        pygame.draw.rect(screen, config.BROWN, self.menu_button_rect, border_radius=5)
        line_thickness = 3
        line_padding = 8
        for i in range(3):
            y_pos = self.menu_button_rect.y + line_padding + i * (line_thickness + line_padding)
            pygame.draw.line(screen, config.WHITE,
                             (self.menu_button_rect.x + line_padding, y_pos),
                             (self.menu_button_rect.right - line_padding, y_pos),
                             line_thickness)
        
        # --- DRAW MENU (if open) ---
        if self.menu_open:
            pygame.draw.rect(screen, config.DARK_GREY, self.menu_rect, border_radius=5)
            pygame.draw.rect(screen, config.WHITE, self.menu_rect, 2, border_radius=5) # Outline

            for option_name, option_rect in self.menu_options.items():
                text_surface = self.option_font.render(option_name, True, config.WHITE)
                # Blit text centered within its calculated rect (which is inside the menu_rect)
                screen.blit(text_surface, text_surface.get_rect(center=option_rect.center))
                # Optional: draw outline for individual menu items (for debugging/visual feedback)
                # pygame.draw.rect(screen, config.RED, option_rect, 1)

# This part runs only if levelSelectMap.py is executed directly (not imported)
if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    # Create a dummy config module for testing purposes
    class Config:
        SCREEN_WIDTH = 1000
        SCREEN_HEIGHT = 700
        FONT_SIZE_MAIN_TITLE = 70
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)
        GREEN = (0, 200, 0)
        BLUE = (0, 0, 200)
        YELLOW = (255, 255, 0)
        BROWN = (139, 69, 19)
        CYAN = (0, 255, 255)
        ORANGE = (255, 165, 0)
        LIGHT_GREY = (200, 200, 200)
        PURPLE = (128, 0, 128)

    config = Config() # Override config with the dummy for testing

    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Level Select Map Test")

    level_map = LevelSelectMap()

    test_running = True
    while test_running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                test_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                selected_stage = level_map.handle_click(mouse_pos)
                if selected_stage:
                    info = level_map.get_level_info(selected_stage)
                    print(f"Clicked {selected_stage}: Level {info['level_num']}")

        level_map.update(mouse_pos)
        level_map.draw(screen)
        pygame.display.flip()

    pygame.quit()