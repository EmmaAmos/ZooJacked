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
        self._load_map_image() # Initial load of map image

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
            },
            "Kangaroo Boogaloo": {
                "level_num": 1,
                "map_rect": pygame.Rect(390, 805, 80, 80),
                "tooltip": "Kangaroo Boogaloo",
                "module": stages.stage2,
                "button_color": config.GREEN
            }
        }

        self.map_display_width = config.SCREEN_WIDTH * 0.9
        self.map_display_height = config.SCREEN_HEIGHT * 0.9

        # Ensure self.map_image is loaded before scaling calculations
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

        self._scale_level_rects() # This populates 'scaled_rect' for each level in self.levels_data

        # --- IMPORTANT: Initialization and call for level_buttons ---
        self.level_buttons = [] # Initialize level_buttons as an empty list
        self._create_level_buttons() # Call the method to populate level_buttons with (name, scaled_rect) tuples
        # --- End of important additions ---

        self.hovered_level_name = None
        self.tooltip_font = pygame.font.Font(None, 30)
        self.button_font = pygame.font.Font(None, 24)

        # --- MENU BUTTON ADDITIONS ---
        self.menu_button_rect = pygame.Rect(config.SCREEN_WIDTH - 60, 20, 40, 30)
        self.menu_open = False

        self.menu_options = {
            "Options": None,
            "Settings": None,
            "Character Select": None
        }
        self.menu_rect = None
        self.option_font = pygame.font.Font(None, 30)
        self._calculate_menu_rects()
        # --- END MENU BUTTON ADDITIONS ---

    def _load_map_image(self):
        # Your existing _load_map_image function
        try:
            self.map_image = pygame.image.load("assests/AA_Map.png").convert_alpha()
        except pygame.error as e:
            print(f"Error loading map image (assests/AA_Map.png): {e}")
            self.map_image = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            self.map_image.fill(config.RED)
            print("Using a red placeholder for the map image.")

    def _scale_level_rects(self):
        # Your existing _scale_level_rects function
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

    def _create_level_buttons(self):
        """
        Populates self.level_buttons with (level_name, scaled_rect) tuples.
        This allows handle_click and draw to easily iterate over clickable level areas.
        """
        self.level_buttons = [] # Clear the list just in case (e.g., if called again)
        for level_name, data in self.levels_data.items():
            if "scaled_rect" in data: # Ensure scaled_rect exists before adding
                self.level_buttons.append((level_name, data["scaled_rect"]))
            else:
                print(f"Warning: Level '{level_name}' has no 'scaled_rect'. Run _scale_level_rects first.")

    def _calculate_menu_rects(self):
        # Your existing _calculate_menu_rects function
        menu_width = 200
        menu_height = len(self.menu_options) * 40 + 20
        menu_x = config.SCREEN_WIDTH - menu_width - 20
        menu_y = self.menu_button_rect.bottom + 10
        self.menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)

        y_offset = menu_y + 10
        for option_name in self.menu_options:
            text_surface = self.option_font.render(option_name, True, config.WHITE)
            option_rect = text_surface.get_rect(center=(self.menu_rect.centerx, y_offset + text_surface.get_height() // 2))
            option_rect.x = menu_x + 10
            self.menu_options[option_name] = option_rect
            y_offset += 40

    def handle_click(self, mouse_pos):
        # Your existing handle_click function
        if self.menu_button_rect.collidepoint(mouse_pos):
            self.menu_open = not self.menu_open
            return None

        if self.menu_open:
            for option_name, option_rect in self.menu_options.items():
                if option_rect.collidepoint(mouse_pos):
                    self.menu_open = False
                    if option_name == "Character Select":
                        return "character_select"
                    elif option_name == "Options":
                        print("Options button clicked (future functionality)")
                    elif option_name == "Settings":
                        print("Settings button clicked (future functionality)")
            return None

        for level_name, button_rect in self.level_buttons: # This now correctly iterates over self.level_buttons
            if button_rect.collidepoint(mouse_pos):
                return level_name
        return None

    def get_level_info(self, level_name):
        # Your existing get_level_info function
        return self.levels_data.get(level_name)

    def update(self, mouse_pos):
        # Your existing update function
        self.hovered_level_name = None
        for level_name, data in self.levels_data.items():
            if data["scaled_rect"].collidepoint(mouse_pos):
                self.hovered_level_name = level_name
                break

    def draw(self, screen):
        # Your existing draw function
        screen.fill(config.BLACK)

        if self.map_image:
            scaled_map = pygame.transform.scale(self.map_image, (self.map_display_width, self.map_display_height))
            screen.blit(scaled_map, self.map_rect_on_screen.topleft)

        title_font = pygame.font.Font(None, config.FONT_SIZE_MAIN_TITLE - 20)
        title_surface = title_font.render("Select Your Adventure", True, config.WHITE)
        title_rect = title_surface.get_rect(center=(config.SCREEN_WIDTH // 2, 40))
        screen.blit(title_surface, title_rect)

        for level_name, data in self.levels_data.items():
            button_rect = data["scaled_rect"]
            button_color = data["button_color"]

            if level_name == "Crocodile Creek Tutorial":
                continue

            if level_name == self.hovered_level_name:
                pygame.draw.rect(screen, config.WHITE, button_rect.inflate(10, 10), border_radius=5)
                pygame.draw.rect(screen, button_color, button_rect, border_radius=5)
            else:
                pygame.draw.rect(screen, button_color, button_rect, border_radius=5)

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
        
        pygame.draw.rect(screen, config.BROWN, self.menu_button_rect, border_radius=5)
        line_thickness = 3
        line_padding = 8
        for i in range(3):
            y_pos = self.menu_button_rect.y + line_padding + i * (line_thickness + line_padding)
            pygame.draw.line(screen, config.WHITE,
                             (self.menu_button_rect.x + line_padding, y_pos),
                             (self.menu_button_rect.right - line_padding, y_pos),
                             line_thickness)
        
        if self.menu_open:
            pygame.draw.rect(screen, config.DARK_GREY, self.menu_rect, border_radius=5)
            pygame.draw.rect(screen, config.WHITE, self.menu_rect, 2, border_radius=5)

            for option_name, option_rect in self.menu_options.items():
                text_surface = self.option_font.render(option_name, True, config.WHITE)
                screen.blit(text_surface, text_surface.get_rect(center=option_rect.center))

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

    def _create_level_buttons(self):
        """
        Creates the clickable button rects for levels based on their scaled_rects.
        This method is crucial for populating self.level_buttons.
        """
        # Clear existing buttons if called multiple times (e.g., if levels change dynamically)
        self.level_buttons = [] 
        for level_name, data in self.levels_data.items():
            # The 'scaled_rect' is already calculated by _scale_level_rects
            # We just need to add it to level_buttons for iteration in draw/handle_click
            self.level_buttons.append((level_name, data["scaled_rect"]))


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
        # Iterate over self.level_buttons which now stores the scaled_rects
        for level_name, button_rect in self.level_buttons:
            if button_rect.collidepoint(mouse_pos):
                print(f"Level '{level_name}' button clicked!")
                return level_name
        return None

    def get_level_info(self, level_name):
        """Retrieves the full data for a given level name."""
        return self.levels_data.get(level_name)

    def update(self, mouse_pos):
        """Updates the state, particularly for hover effects/tooltips."""
        # Update hovered level for tooltips
        self.hovered_level_name = None
        for level_name, data in self.levels_data.items():
            if data["scaled_rect"].collidepoint(mouse_pos):
                self.hovered_level_name = level_name
                break
        
        # If menu is open, no need to update level hovers, but this is fine.
        # You might want to update menu item hovers here if you add them later.

    def draw(self, screen):
        """
        Draws the level selection map screen.
        :param screen: The Pygame screen surface to draw on.
        """
        screen.fill(config.BLACK) # Fill background with black

        if self.map_image:
            scaled_map = pygame.transform.scale(self.map_image, (self.map_display_width, self.map_display_height))
            screen.blit(scaled_map, self.map_rect_on_screen.topleft)

        title_font = pygame.font.Font(None, config.FONT_SIZE_MAIN_TITLE - 20)
        title_surface = title_font.render("Select Your Adventure", True, config.WHITE)
        title_rect = title_surface.get_rect(center=(config.SCREEN_WIDTH // 2, 40))
        screen.blit(title_surface, title_rect)

        # Draw the buttons for each level
        for level_name, data in self.levels_data.items():
            # Use data["scaled_rect"] directly for drawing
            button_rect = data["scaled_rect"]
            button_color = data["button_color"]

            # Check if this is the "Crocodile Creek Tutorial" and if we should make it invisible
            if level_name == "Crocodile Creek Tutorial":
                continue # Skip drawing this level's button

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

        # Draw tooltips if a level is hovered
        if self.hovered_level_name:
            tooltip_text = self.levels_data[self.hovered_level_name]["tooltip"]
            tooltip_surface = self.tooltip_font.render(tooltip_text, True, config.BLACK)

            mouse_x, mouse_y = pygame.mouse.get_pos()
            tooltip_rect = tooltip_surface.get_rect(midbottom=(mouse_x, mouse_y - 5))

            pygame.draw.rect(screen, config.WHITE, tooltip_rect.inflate(10, 5), border_radius=5)
            screen.blit(tooltip_surface, tooltip_rect)
        
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
            pygame.draw.rect(screen, config.GREY, self.menu_rect, border_radius=5)
            pygame.draw.rect(screen, config.WHITE, self.menu_rect, 2, border_radius=5) # Outline

            for option_name, option_rect in self.menu_options.items():
                text_surface = self.option_font.render(option_name, True, config.WHITE)
                screen.blit(text_surface, text_surface.get_rect(center=option_rect.center))


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
        DARK_GREY = (50, 50, 50) # Added for menu background

        # Dummy modules for testing
        class CrocodileCreekTutorialModule:
            pass
        CROCODILE_CREEK_TUTORIAL_MODULE = CrocodileCreekTutorialModule()

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
                selected_action = level_map.handle_click(mouse_pos) # Changed to selected_action
                if selected_action:
                    if selected_action == "character_select":
                        print("Test: Character Select button clicked!")
                    else: # It's a level name
                        info = level_map.get_level_info(selected_action)
                        print(f"Test: Clicked {selected_action}: Level {info['level_num']}")

        level_map.update(mouse_pos)
        level_map.draw(screen)
        pygame.display.flip()

    pygame.quit()