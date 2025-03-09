import pygame

# Constantes
GRAVITY = 0.5
JUMP_POWER = -10
SPEED = 5
ANIMATION_SPEED = 0.15
DEATH_ANIMATION_SPEED = 10  # Retraso entre frames de muerte

class Player:
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        
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
            "dead": [
                pygame.image.load("assets/peach/killed1.png"),
                pygame.image.load("assets/peach/killed2.png"),
                pygame.image.load("assets/peach/killed3.png"),
                pygame.image.load("assets/peach/killed4.png"),
                pygame.image.load("assets/peach/killed.png"),
            ]
        }
        
        self.image = self.sprites["idle"][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity_y = 0
        self.on_ground = False
        self.frame_index = 0
        self.direction = "right"  # Dirección inicial
        self.alive = True  # Estado del personaje

        # Variables para animación de muerte
        self.is_dying = False
        self.death_frame = 0
        self.death_timer = 0

    def update(self, platforms, enemies):
        """Actualizar estado del personaje y manejar animaciones"""
        if self.is_dying:
            self.death_animation()
            return
        
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
        
        # Verificar colisiones con enemigos
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                if self.velocity_y > 0 and self.rect.bottom - enemy.rect.top < 10:  # Peach cae sobre el enemigo
                    self.velocity_y = JUMP_POWER  # Rebote tras eliminar al enemigo
                    enemy.die()
                else:
                    self.die()

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
    
    def die(self):
        """Manejar la muerte del personaje con animación."""
        self.is_dying = True
        self.death_frame = 0
        self.death_timer = 0

    def death_animation(self):
        """Ejecuta la animación de muerte cuadro a cuadro."""
        self.death_timer += 1
        if self.death_timer % DEATH_ANIMATION_SPEED == 0:
            if self.death_frame < len(self.sprites["dead"]) - 1:
                self.death_frame += 1
            else:
                self.alive = False  # Marcamos como muerto al final de la animación
        
        self.image = self.sprites["dead"][self.death_frame]

    def reset(self):
        """Reinicia el personaje tras la muerte"""
        self.rect.topleft = (self.start_x, self.start_y)
        self.velocity_y = 0
        self.on_ground = False
        self.alive = True
        self.is_dying = False
        self.death_frame = 0
        self.death_timer = 0
        self.image = self.sprites["idle"][0]

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
