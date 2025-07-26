# config.py

# Screen Dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FONT_SIZE_MAIN_TITLE = 70

# Colors (add these if they're not already present)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)       # <--- Add this if missing
CYAN = (0, 255, 255)        # <--- Add this if missing
ORANGE = (255, 165, 0)      # <--- Add this if missing
LIGHT_GREY = (200, 200, 200) # <--- Add this if missing
PURPLE = (128, 0, 128)
GREY = (128, 128, 128)

# Font Sizes
FONT_SIZE_MAIN_TITLE = 100
FONT_SIZE_BUTTON = 50
FONT_SIZE_CHAR_BUTTON = 40

# Button Properties
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60
BUTTON_RADIUS = 10

# Character Image Properties
CHAR_IMG_WIDTH = 200
CHAR_IMG_HEIGHT = 200
CHAR_SPACING = 50 # Space between characters


# Game Physics and Player Constants (NEW)
PLAYER_SPEED = 5        # How many pixels the player moves per frame horizontally
GRAVITY = 0.8           # Gravity strength, pulls objects down
GROUND_HEIGHT = 50      # Distance from bottom of screen to the "ground" level

# UI Bar and Text Positions
HEALTH_BAR_Y_OFFSET = 50  # Adjust this value to move everything down more
NAME_Y_OFFSET = 20        # Adjust this value for the name relative to the bar

# UI Text Properties
PLAYER_NAME_FONT_SIZE = 36 # Larger size
WHITE = (255, 255, 255)   # Define white color if not already present