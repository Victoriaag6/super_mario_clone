import pygame
from player import Player
from platform import Platform
from enemy import Enemy

# Inicializar pygame
pygame.init()

# Constantes
WIDTH, HEIGHT = 800, 600
FPS = 60

# Configurar pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Mario Clone")

# Cargar fondo del nivel
background = pygame.image.load("assets/fondo.jpg")

# Crear objetos
player = Player(100, HEIGHT - 150)

# Crear plataformas con textura de ladrillos (más grandes)
platforms = [
    Platform(0, HEIGHT - 80, WIDTH, 80, "assets/suelo.jpg"),  # Suelo principal más alto
    Platform(250, 350, 300, 40, "assets/brick.jpg")           # Plataforma flotante más grande
]

# Crear enemigos (Goombas) con animación y movimiento
enemies = [
    Enemy(300, 310, speed=2, frames_folder="assets/goomba/"),  # Goomba en la plataforma flotante
    Enemy(500, HEIGHT - 120, speed=2, frames_folder="assets/goomba/")  # Goomba en el suelo
]

# Reloj
clock = pygame.time.Clock()

# Fuente y botón "Volver a Jugar"
font = pygame.font.Font(None, 40)  # Fuente más grande y clara
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60
button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
BUTTON_COLOR = (200, 0, 0)
TEXT_COLOR = (255, 255, 255)

# Bucle del juego
running = True
while running:
    clock.tick(FPS)
    screen.blit(background, (0, 0))  # Dibujar fondo

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not player.alive:
            if button_rect.collidepoint(event.pos):
                player.reset()

    # Si el jugador está vivo, actualizar normalmente
    if player.alive:
        player.update(platforms, enemies)

        # Actualizar enemigos (Goombas)
        for enemy in enemies:
            enemy.update()

            # Hacer que el enemigo cambie de dirección si toca un borde de la plataforma
            for platform in platforms:
                if enemy.rect.left <= platform.rect.left or enemy.rect.right >= platform.rect.right:
                    enemy.change_direction()

        # Dibujar plataformas con textura de ladrillos
        for platform in platforms:
            platform.draw(screen)

        # Dibujar enemigos
        for enemy in enemies:
            enemy.draw(screen)

    # Dibujar jugador
    player.draw(screen)

    # Mostrar botón "Volver a Jugar" si el jugador muere
    if not player.alive:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect, border_radius=10)  # Botón con bordes redondeados
        text = font.render("Volver a Jugar", True, TEXT_COLOR)
        
        # Centrar el texto en el botón
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()
