import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame Setup Example")

# Load the AA_Map image
aa_map = pygame.image.load("assests/bootUpscreen.jpg")  

# Replace with the correct path to your image

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the AA_Map image on the screen
    screen.blit(aa_map, (0, 0))  # Adjust the position as needed

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()