import pygame

# Constantes
GRAVITY = 0.5
JUMP_POWER = -10
SPEED = 5
ANIMATION_SPEED = 0.15

class Player:
    def __init__(self, x, y):
        # Cargar sprites desde la carpeta assets/peach/
        self.sprites = {
            "idle": [pygame.image.load("assets/peach/stand1.png")],
            "walk_right": [
                pygame.image.load("assets/peach/moveRight1.png"),
                pygame.image.load("assets/peach/moveRight2and4.png"),
                pygame.image.load("assets/peach/moveRight3.png"),
                pygame.image.load("assets/peach/moveRight2and4.png"),
                pygame.image.load("assets/peach/moveRight5.png"),
                pygame.image.load("assets/peach/moveRight6.png"),
                pygame.image.load("assets/peach/moveRight7.png")
            ],
            "walk_left": [
                pygame.image.load("assets/peach/moveLeft1.png"),
                pygame.image.load("assets/peach/moveLeft2and4.png"),
                pygame.image.load("assets/peach/moveLeft3.png"),
                pygame.image.load("assets/peach/moveLeft2and4.png"),
                pygame.image.load("assets/peach/moveLeft5.png"),
                pygame.image.load("assets/peach/moveLeft6.png"),
                pygame.image.load("assets/peach/moveLeft7.png")
            ],
            "jump": [pygame.image.load("assets/peach/jum.png")],
            "fall": [pygame.image.load("assets/peach/fallDown.png")],
            "fall_left": [pygame.image.load("assets/peach/left_falldown.png")],
            "dead": [pygame.image.load("assets/peach/killed.png")]
        }
        
        self.image = self.sprites["idle"][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity_y = 0
        self.on_ground = False
        self.frame_index = 0
        self.direction = "right"  # Dirección inicial

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.rect.x -= SPEED
            self.direction = "left"
            self.frame_index += ANIMATION_SPEED
        elif keys[pygame.K_RIGHT]:
            self.rect.x += SPEED
            self.direction = "right"
            self.frame_index += ANIMATION_SPEED
        else:
            self.frame_index = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = JUMP_POWER
            self.on_ground = False

        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Verificar colisiones con plataformas
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                self.rect.y = platform.rect.top - self.rect.height
                self.velocity_y = 0
                self.on_ground = True

        # Determinar sprite a usar
        if not self.on_ground:
            if self.direction == "left":
                self.image = self.sprites["fall_left"][0]
            else:
                self.image = self.sprites["jump"][0] if self.velocity_y < 0 else self.sprites["fall"][0]
        else:
            if keys[pygame.K_LEFT]:
                self.frame_index %= len(self.sprites["walk_left"])
                self.image = self.sprites["walk_left"][int(self.frame_index)]
            elif keys[pygame.K_RIGHT]:
                self.frame_index %= len(self.sprites["walk_right"])
                self.image = self.sprites["walk_right"][int(self.frame_index)]
            else:
                self.image = self.sprites["idle"][0]

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)