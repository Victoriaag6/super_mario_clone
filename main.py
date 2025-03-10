import pygame
from player import Player
from platform import Platform
from enemy import Enemy
from coin import Coin
from coin_block import CoinBlock

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

# Crear jugador
player = Player(100, HEIGHT - 150)

# Crear plataformas
platforms = [
    Platform(0, HEIGHT - 80, WIDTH, 80, "assets/suelo.jpg"),  # Suelo principal
    Platform(250, 350, 300, 40, "assets/brick.jpg")           # Plataforma flotante
]

# Crear enemigo (Goomba)
enemies = [Enemy(320, HEIGHT - 110, speed=2, size=(30, 30), frames_folder="assets/goomba/")]

# Lista de monedas generadas
coins = []

# Crear bloques de monedas
coin_blocks = [CoinBlock(400, 310, 40, 40)]

# Contador de monedas
score = 0
font = pygame.font.Font(None, 40)

# Reloj
clock = pygame.time.Clock()

# Botón "Volver a Jugar"
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

    # Verificar colisión con bloques de monedas
    for block in coin_blocks:
        if player.rect.colliderect(block.rect) and player.velocity_y < 0:  # Golpe desde abajo
            new_coin = block.hit()
            if new_coin:
                coins.append(new_coin)  # Agregar la moneda generada

    # Si el jugador está vivo, actualizar normalmente
    if player.alive:
        player.update(platforms, coin_blocks, enemies)

        # Actualizar enemigos (Goombas)
        for enemy in enemies:
            enemy.update()
            
            # Hacer que el enemigo cambie de dirección si toca un borde de la plataforma
            for platform in platforms:
                if enemy.rect.left <= platform.rect.left or enemy.rect.right >= platform.rect.right:
                    enemy.change_direction()

        # Actualizar monedas
        for coin in coins:
            coin.update()
            if player.rect.colliderect(coin.rect) and not coin.collected:
                coin.collect()
                score += 10  # Sumar puntos

        # Dibujar plataformas
        for platform in platforms:
            platform.draw(screen)

        # Dibujar bloques de monedas
        for block in coin_blocks:
            block.draw(screen)

        # Dibujar monedas en pantalla
        for coin in coins:
            coin.draw(screen)

        # Dibujar enemigos
        for enemy in enemies:
            enemy.draw(screen)

    # Dibujar jugador
    player.draw(screen)

    # Mostrar contador de monedas
    score_text = font.render(f"Monedas: {score}", True, (255, 255, 0))
    screen.blit(score_text, (20, 20))

    # Mostrar botón "Volver a Jugar" si el jugador muere
    if not player.alive:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect, border_radius=10)
        text = font.render("Volver a Jugar", True, TEXT_COLOR)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()
