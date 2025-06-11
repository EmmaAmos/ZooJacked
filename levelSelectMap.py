# levelSelectMap.py
import pygame
import config

# Import all your stage modules here
import stages.stage1
import stages.stage2
import stages.stage3
import stages.bounusStage
# Import the consolidated tutorial stage
import stages.crocodileCreekTutorial # <--- This is the correct import for your tutorial stage

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
            "Forest": {
                "level_num": 1,
                "map_rect": pygame.Rect(200, 320, 80, 80), # Example: area around the birds
                "tooltip": "Forest Level",
                "module": stages.stage1
            },
            "Desert": {
                "level_num": 2,
                "map_rect": pygame.Rect(180, 240, 80, 80), # Example: area around Crocodile Creek
                "tooltip": "Desert Level",
                "module": stages.stage2
            },
            "Kangaroo Outback": {
                "level_num": 3,
                "map_rect": pygame.Rect(120, 420, 80, 80), # Example: area around the kangaroo
                "tooltip": "Kangaroo Outback",
                "module": stages.stage3
            },
            "Stingray Bay": {
                "level_num": 4,
                "map_rect": pygame.Rect(440, 100, 100, 100), # Example: area around Stingray Bay icon
                "tooltip": "Stingray Bay Adventure",
                "module": stages.bounusStage
            },
            "The Reef Aquarium": {
                "level_num": 5,
                "map_rect": pygame.Rect(650, 100, 100, 100), # Example: area around The Reef Aquarium icon
                "tooltip": "Explore The Reef",
                "module": stages.bounusStage
            },
            # All tutorial-like stages now point to stages.crocodileCreekTutorial
            "Boat Tutorial": {
                "level_num": 6,
                "map_rect": pygame.Rect(500, 400, 100, 100), # Placeholder, adjust based on where you want this on the map
                "tooltip": "Boat Man's Tutorial",
                "module": stages.crocodileCreekTutorial # <--- Pointing to the consolidated tutorial
            },
            "Guest Services": {
                "level_num": 7,
                "map_rect": pygame.Rect(720, 340, 60, 60), # Ensure these are correct for the '?' icon
                "tooltip": "Help & Information",
                "module": stages.crocodileCreekTutorial # <--- Pointing to the consolidated tutorial
            },
            "Crocodile Creek Tutorial": {
                "level_num": 8,
                "map_rect": pygame.Rect(180, 240, 80, 80), # **ADJUST THESE COORDINATES for the purple dot**
                "tooltip": "Crocodile Creek Adventure Tutorial",
                "module": stages.crocodileCreekTutorial # <--- Pointing to the consolidated tutorial
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

        # Optional: Draw debug rectangles for clickable areas (remove in final game)
        # for level_name, data in self.levels_data.items():
        #     # Draw an outline for debugging the clickable areas
        #     pygame.draw.rect(screen, config.RED, data["scaled_rect"], 2)

        if self.hovered_level_name:
            tooltip_text = self.levels_data[self.hovered_level_name]["tooltip"]
            tooltip_surface = self.tooltip_font.render(tooltip_text, True, config.BLACK)

            mouse_x, mouse_y = pygame.mouse.get_pos()
            tooltip_rect = tooltip_surface.get_rect(midbottom=(mouse_x, mouse_y - 5))

            pygame.draw.rect(screen, config.WHITE, tooltip_rect.inflate(10, 5), border_radius=5)
            screen.blit(tooltip_surface, tooltip_rect)

# This part runs only if levelSelectMap.py is executed directly (not imported)
if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

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