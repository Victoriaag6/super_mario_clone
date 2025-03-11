import pygame
from player import Player
from platform import Platform
from enemy import Enemy
from coin import Coin
from coin_block import CoinBlock

# Clase Flag: bandera estática (sin animación)
class Flag:
    def __init__(self, x, y, size=(100, 250), image_path="assets/flag.png"):
        self.x = x
        self.y = y
        self.size = size
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        pass  # Sin animación en la bandera estática

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

# Clase Lava: similar a Platform pero con efecto de muerte
class Lava:
    def __init__(self, x, y, width, height, image_path="assets/lava.png"):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

# Inicializar pygame y el mixer de audio
pygame.init()
pygame.mixer.init()

# Constantes y configuración de pantalla
WIDTH, HEIGHT = 800, 600
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Mario Clone")

# --- Cargar sonidos ---
sound_walk = pygame.mixer.Sound("assets/sounds/walk.mp3")
sound_jump = pygame.mixer.Sound("assets/sounds/jump.mp3")
sound_victory = pygame.mixer.Sound("assets/sounds/victory.mp3")
sound_lose = pygame.mixer.Sound("assets/sounds/lose.mp3")
walking_sound_playing = False
victory_played = False
defeat_played = False

# --- PANTALLA 1 ---
background1 = pygame.image.load("assets/fondo2.png")
background1 = pygame.transform.scale(background1, (WIDTH, HEIGHT))
platforms1 = [
    Platform(0, HEIGHT - 80, WIDTH, 80, "assets/suelo1.png"),  # Suelo principal
    Platform(250, 350, 260, 40, "assets/brick.jpg")             # Plataforma flotante
]
enemies1 = [
    Enemy(320, HEIGHT - 120, speed=2, size=(40, 40), frames_folder="assets/goomba/")
]
coin_blocks1 = [CoinBlock(510, 350, 40, 40)]
coins = []

# --- PANTALLA 2 (Final) ---
background2 = pygame.image.load("assets/fondo2.png")
background2 = pygame.transform.scale(background2, (WIDTH, HEIGHT))
# Escalera rellena de ladrillos (ejemplo de escalera similar al original)
platforms2 = [
    Platform(0, HEIGHT - 80, WIDTH, 80, "assets/suelo1.png"),
    # Fila inferior (4 bloques)
    Platform(200, HEIGHT - 120, 50, 40, "assets/brick.jpg"),
    Platform(250, HEIGHT - 120, 50, 40, "assets/brick.jpg"),
    Platform(300, HEIGHT - 120, 50, 40, "assets/brick.jpg"),
    Platform(350, HEIGHT - 120, 50, 40, "assets/brick.jpg"),
    # Segunda fila (3 bloques)
    Platform(260, HEIGHT - 160, 50, 40, "assets/brick.jpg"),
    Platform(300, HEIGHT - 160, 50, 40, "assets/brick.jpg"),
    Platform(350, HEIGHT - 160, 50, 40, "assets/brick.jpg"),
    # Tercera fila (2 bloques)
    Platform(300, HEIGHT - 200, 50, 40, "assets/brick.jpg"),
    Platform(350, HEIGHT - 200, 50, 40, "assets/brick.jpg"),
    # Fila superior (1 bloque)
    Platform(350, HEIGHT - 240, 50, 40, "assets/brick.jpg")
]
# Agregar lava en la segunda pantalla (opcional)
lava = Lava(430, HEIGHT - 100, 250, 80, "assets/lava.png")
# Crear la bandera final en la segunda pantalla
flag = Flag(700, HEIGHT - 80 - 240, size=(100, 250), image_path="assets/flag.png")

# Jugador y variables de juego
player = Player(100, HEIGHT - 150)
score = 0
font = pygame.font.Font(None, 40)
clock = pygame.time.Clock()

# Botón "Volver a Jugar"
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60
button_rect = pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2, BUTTON_WIDTH, BUTTON_HEIGHT)
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
        
        # Botón de reinicio si Peach muere y no hay victoria
        if event.type == pygame.MOUSEBUTTONDOWN and not player.alive and not win:
            if button_rect.collidepoint(event.pos):
                player.reset()
                score = 0
                win = False
                current_screen = 1
                victory_played = False
                defeat_played = False
                for enemy in enemies1:
                    enemy.reset()
                coins.clear()
        
        # Detectar salto y reproducir sonido
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and player.on_ground:
                sound_jump.play()
    
    # Reproducir sonido de caminar mientras se presionan teclas de movimiento
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
        if not walking_sound_playing:
            sound_walk.play(loops=-1)
            walking_sound_playing = True
    else:
        if walking_sound_playing:
            sound_walk.stop()
            walking_sound_playing = False

    # --- PANTALLA 1 ---
    if current_screen == 1 and not win:
        screen.blit(background1, (0, 0))
        
        # Bloques de monedas
        for block in coin_blocks1:
            if player.rect.colliderect(block.rect) and player.velocity_y < 0:
                new_coin = block.hit()
                if new_coin:
                    coins.append(new_coin)
        
        if player.alive:
            player.update(platforms1, coin_blocks1, enemies1)
            for enemy in enemies1:
                enemy.update()  # Remove the extra argument
                for plat in platforms1:
                    if enemy.rect.left <= plat.rect.left or enemy.rect.right >= plat.rect.right:
                        enemy.change_direction()
            for coin in coins:
                coin.update()
                if player.rect.colliderect(coin.rect) and not coin.collected:
                    coin.collect()
                    score += 10
            for plat in platforms1:
                plat.draw(screen)
            for block in coin_blocks1:
                block.draw(screen)
            for coin in coins:
                coin.draw(screen)
            for enemy in enemies1:
                enemy.draw(screen)
       
        player.draw(screen)
        score_text = font.render(f"Monedas: {score}", True, (255, 255, 0))
        screen.blit(score_text, (20, 20))
        
        # Cambiar a Pantalla 2 si Peach llega al borde derecho
        if player.rect.x >= WIDTH - 50:
            current_screen = 2
            player.rect.x = 50
            player.rect.y = HEIGHT - 150
        
        if not player.alive and not defeat_played:
            sound_lose.play()
            defeat_played = True

    # --- PANTALLA 2 ---
    elif current_screen == 2 and not win:
        screen.blit(background2, (0, 0))
        for plat in platforms2:
            plat.draw(screen)
        lava.draw(screen)
        flag.update()
        flag.draw(screen)
        if player.alive:
            player.update(platforms2, [], [])
        player.draw(screen)
        score_text = font.render(f"Monedas: {score}", True, (255, 255, 0))
        screen.blit(score_text, (20, 20))
        if player.rect.colliderect(flag.rect):
            win = True
            if not victory_played:
                sound_victory.play()
                victory_played = True

    # --- Victoria ---
    if win:
        # Mantener el fondo de Pantalla 2 visible
        screen.blit(background2, (0, 0))
        for plat in platforms2:
            plat.draw(screen)
        lava.draw(screen)
        flag.draw(screen)
        player.update(platforms2, [], [])
        player.draw(screen)
        victory_text = font.render("¡Ganaste!", True, (255, 255, 0))
        screen.blit(victory_text, (WIDTH//2 - 60, HEIGHT//2 - 20))
    
    # Botón "Volver a Jugar" si Peach muere y no hay victoria
    if not player.alive and not win:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect, border_radius=10)
        text = font.render("Volver a Jugar", True, TEXT_COLOR)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)
    
    pygame.display.flip()

pygame.quit()
