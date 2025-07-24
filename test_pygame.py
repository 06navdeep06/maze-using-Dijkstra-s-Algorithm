import pygame

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Test")

# Colors
WHITE = (255, 255, 255)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Drawing
    screen.fill(WHITE)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
print("Pygame test finished successfully.")
