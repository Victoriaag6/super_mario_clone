import pygame
from player import Player
from platform import Platform
from enemy import Enemy

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Mario Clone")

# Load assets
background = pygame.image.load("assets/fondo.jpg")
player = Player(100, HEIGHT - 150)
platforms = [Platform(0, HEIGHT - 40, WIDTH, 40), Platform(300, 400, 200, 20)]
enemies = [Enemy(500, HEIGHT - 80)]

# Clock
clock = pygame.time.Clock()

# Game Loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    # Draw background
    screen.blit(background, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update player and enemies
    player.update(platforms)
    for enemy in enemies:
        enemy.update()

    # Draw everything
    for platform in platforms:
        platform.draw(screen)

    for enemy in enemies:
        enemy.draw(screen)

    player.draw(screen)

    pygame.display.flip()

pygame.quit()
