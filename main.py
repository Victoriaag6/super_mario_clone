import pygame
from player import Player
from platform import Platform
from enemy import Enemy
from coin import Coin
from coin_block import CoinBlock

# Clase Flag: bandera estática
class Flag:
    def __init__(self, x, y, size=(60, 120), image_path="assets/flag.png"):
        self.x = x
        self.y = y
        self.size = size
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        # No hay animación, así que no se necesita actualizar nada
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

# Inicializar pygame
pygame.init()

# Constantes
WIDTH, HEIGHT = 800, 600
FPS = 60

# Configurar pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Mario Clone")

# --- PANTALLA 1 ---
background1 = pygame.image.load("assets/fondo2.png")
background1 = pygame.transform.scale(background1, (WIDTH, HEIGHT))

platforms1 = [
    Platform(0, HEIGHT - 80, WIDTH, 80, "assets/suelo1.png"),  # Suelo principal
    Platform(250, 350, 300, 40, "assets/brick.jpg")            # Plataforma flotante
]

enemies1 = [
    Enemy(320, HEIGHT - 120, speed=2, size=(40, 40), frames_folder="assets/goomba/")
]

coin_blocks1 = [CoinBlock(550, 350, 40, 40)]
coins = []

# --- PANTALLA 2 (Final) ---
background2 = pygame.image.load("assets/fondo2.png")
background2 = pygame.transform.scale(background2, (WIDTH, HEIGHT))

platforms2 = [
    Platform(0, HEIGHT - 80, WIDTH, 80, "assets/suelo1.png")  # Suelo final
]

# Crear la bandera estática en la Pantalla 2
flag = Flag(600, HEIGHT - 200, size=(60, 120), image_path="assets/flag.png")

# Jugador y variables de juego
player = Player(100, HEIGHT - 150)
score = 0
font = pygame.font.Font(None, 40)
clock = pygame.time.Clock()

# Botón "Volver a Jugar"
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60
button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
BUTTON_COLOR = (200, 0, 0)
TEXT_COLOR = (255, 255, 255)

# Estado: pantalla actual (1 = nivel, 2 = final) y victoria
current_screen = 1
win = False

running = True
while running:
    clock.tick(FPS)

    # --- Manejo de eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Si Peach muere, botón de reinicio
        if event.type == pygame.MOUSEBUTTONDOWN and not player.alive and not win:
            if button_rect.collidepoint(event.pos):
                player.reset()
                score = 0
                win = False
                current_screen = 1
                # Reiniciar enemigos de la pantalla 1
                for enemy in enemies1:
                    enemy.reset()
                coins.clear()

    # --- Lógica de Pantalla 1 ---
    if current_screen == 1 and not win:
        # Dibujar fondo
        screen.blit(background1, (0, 0))

        # Verificar colisión con bloques de monedas (golpe desde abajo)
        for block in coin_blocks1:
            if player.rect.colliderect(block.rect) and player.velocity_y < 0:
                new_coin = block.hit()
                if new_coin:
                    coins.append(new_coin)

        # Actualizar y dibujar si Peach está viva
        if player.alive:
            player.update(platforms1, coin_blocks1, enemies1)
            for enemy in enemies1:
                enemy.update()  # Eliminar el argumento platforms1
                # Cambiar dirección si el enemigo se sale de los límites de la plataforma
                for plat in platforms1:
                    if enemy.rect.left <= plat.rect.left or enemy.rect.right >= plat.rect.right:
                        enemy.change_direction()
            for coin in coins:
                coin.update()
                if player.rect.colliderect(coin.rect) and not coin.collected:
                    coin.collect()
                    score += 10

            # Dibujar elementos de la pantalla 1
            for plat in platforms1:
                plat.draw(screen)
            for block in coin_blocks1:
                block.draw(screen)
            for coin in coins:
                coin.draw(screen)
            for enemy in enemies1:
                enemy.draw(screen)
        player.draw(screen)

        # Mostrar puntaje
        score_text = font.render(f"Monedas: {score}", True, (255, 255, 0))
        screen.blit(score_text, (20, 20))

        # Cambiar a Pantalla 2 si Peach llega al borde derecho
        if player.rect.x >= WIDTH - 50:
            current_screen = 2
            player.rect.x = 50
            player.rect.y = HEIGHT - 150

    # --- Lógica de Pantalla 2 (Final) ---
    elif current_screen == 2 and not win:
        screen.blit(background2, (0, 0))
        for plat in platforms2:
            plat.draw(screen)
        # Actualizar y dibujar la bandera estática
        flag.update()
        flag.draw(screen)
        if player.alive:
            player.update(platforms2, [], [])  # Sin bloques ni enemigos en la segunda pantalla
        player.draw(screen)
        score_text = font.render(f"Monedas: {score}", True, (255, 255, 0))
        screen.blit(score_text, (20, 20))
        # Verificar si Peach toca la bandera para ganar
        if player.rect.colliderect(flag.rect):
            win = True
            player.win()  # Activar animación de victoria

    # --- Lógica de Victoria ---
    if win:
        # No llenar la pantalla de negro, solo mostrar el mensaje de victoria
        victory_text = font.render("¡Ganaste!", True, (255, 255, 0))
        screen.blit(victory_text, (WIDTH // 2 - 60, HEIGHT // 2 - 20))
        player.draw(screen)  # Dibujar el sprite de victoria

    # Mostrar botón "Volver a Jugar" si Peach muere y no hay victoria
    if not player.alive and not win:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect, border_radius=10)
        text = font.render("Volver a Jugar", True, TEXT_COLOR)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()
