import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame Setup Example")

# Load the bootUpscreen image
aa_map = pygame.image.load("assests/bootUpscreen.jpg")

# Set up the font and text
font = pygame.font.Font(None, 100)  # None uses the default font, 100 is the font size
text = font.render("Zoo-jacked", True, (255, 0, 0))  # Red color (R, G, B)
text_rect = text.get_rect(center=(400, 300))  # Center the text on the screen

# Button properties
button_font = pygame.font.Font(None, 50)  # Font for the buttons
button_color = (255, 255, 0)  # Yellow color
button_text_color = (0, 0, 0)  # Black color
button_width, button_height = 200, 60
button_radius = 10

# Button positions
story_button_rect = pygame.Rect(150, 500, button_width, button_height)
levels_button_rect = pygame.Rect(450, 500, button_width, button_height)

# Render button text
story_text = button_font.render("Story Mode", True, button_text_color)
levels_text = button_font.render("Levels", True, button_text_color)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the bootUpscreen image on the screen
    screen.blit(aa_map, (0, 0))

    # Draw the text on the screen
    screen.blit(text, text_rect)

    # Draw the buttons
    pygame.draw.rect(screen, button_color, story_button_rect, border_radius=button_radius)
    pygame.draw.rect(screen, button_color, levels_button_rect, border_radius=button_radius)

    # Draw the button text
    screen.blit(story_text, story_text.get_rect(center=story_button_rect.center))
    screen.blit(levels_text, levels_text.get_rect(center=levels_button_rect.center))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()