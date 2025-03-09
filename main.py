import pygame
from player import Player
from platform import Platform
from enemy import Enemy

# Inicializar pygame
pygame.init()

# Constantes
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colores
WHITE = (255, 255, 255)
BUTTON_COLOR = (200, 0, 0)

# Configurar pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Mario Clone")

# Cargar fondo
background = pygame.image.load("assets/fondo.jpg")

# Crear objetos
player = Player(100, HEIGHT - 150)
platforms = [Platform(0, HEIGHT - 40, WIDTH, 40), Platform(300, 400, 200, 20)]
enemies = [Enemy(500, HEIGHT - 80)]

# Reloj
clock = pygame.time.Clock()

# Fuente para el botón
font = pygame.font.Font(None, 36)
button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 50, 150, 50)

# Bucle del juego
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    # Dibujar fondo
    screen.blit(background, (0, 0))

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not player.alive:
            if button_rect.collidepoint(event.pos):
                player.reset()

    # Si el jugador está vivo, se ejecuta el juego normalmente
    if player.alive:
        player.update(platforms, enemies)
        for enemy in enemies:
            enemy.update()

        # Dibujar plataformas
        for platform in platforms:
            platform.draw(screen)

        # Dibujar enemigos
        for enemy in enemies:
            enemy.draw(screen)

    # Dibujar jugador
    player.draw(screen)

    # Mostrar botón "Volver a Jugar" si el jugador está muerto
    if not player.alive:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
        text = font.render("Volver a Jugar", True, (255, 255, 255))
        screen.blit(text, (button_rect.x + 15, button_rect.y + 10))

    pygame.display.flip()

pygame.quit()
