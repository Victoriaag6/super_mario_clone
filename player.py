import pygame

# Constantes
GRAVITY = 0.5
JUMP_POWER = -15  # Aumentamos la altura del salto
SPEED = 5
ANIMATION_SPEED = 0.15
DEATH_ANIMATION_SPEED = 10  # Retraso entre frames de muerte

class Player:
    def __init__(self, x, y, size=(60, 80)):
        self.start_x = x
        self.start_y = y
        self.size = size

        # Cargar y escalar sprites
        self.sprites = {
            "idle": [self.scale_image("assets/peach/stand1.png")],
            "walk_right": [
                self.scale_image("assets/peach/moveRight1.png"),
                self.scale_image("assets/peach/moveRight2and4.png"),
                self.scale_image("assets/peach/moveRight3.png"),
                self.scale_image("assets/peach/moveRight2and4.png"),
                self.scale_image("assets/peach/moveRight5.png"),
                self.scale_image("assets/peach/moveRight6.png"),
                self.scale_image("assets/peach/moveRight7.png")
            ],
            "walk_left": [
                self.scale_image("assets/peach/moveLeft1.png"),
                self.scale_image("assets/peach/moveLeft2and4.png"),
                self.scale_image("assets/peach/moveLeft3.png"),
                self.scale_image("assets/peach/moveLeft2and4.png"),
                self.scale_image("assets/peach/moveLeft5.png"),
                self.scale_image("assets/peach/moveLeft6.png"),
                self.scale_image("assets/peach/moveLeft7.png")
            ],
            "jump": [self.scale_image("assets/peach/jum.png")],
            "fall": [self.scale_image("assets/peach/fallDown.png")],
            "fall_left": [self.scale_image("assets/peach/left_falldown.png")],
            "dead": [
                self.scale_image("assets/peach/killed1.png"),
                self.scale_image("assets/peach/killed2.png"),
                self.scale_image("assets/peach/killed3.png"),
                self.scale_image("assets/peach/killed4.png"),
            ]
        }

        # Añadir sprites de victoria
        self.sprites["win"] = [
            self.scale_image("assets/peach/win1and6.png"),
            self.scale_image("assets/peach/win2and7.png"),
            self.scale_image("assets/peach/win3.png"),
            self.scale_image("assets/peach/win4.png"),
            self.scale_image("assets/peach/win5.png"),
            self.scale_image("assets/peach/win1and6.png"),
            self.scale_image("assets/peach/win2and7.png")
        ]

        self.image = self.sprites["idle"][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity_y = 0
        self.on_ground = False
        self.frame_index = 0
        self.direction = "right"
        self.alive = True

        # Variables para la animación de muerte
        self.is_dying = False
        self.death_frame = 0
        self.death_timer = 0

        # Variables para la animación de victoria
        self.is_winning = False
        self.win_frame = 0
        self.win_timer = 0

    def scale_image(self, path):
        """Carga y escala una imagen al tamaño de Peach"""
        image = pygame.image.load(path)
        return pygame.transform.scale(image, self.size)

    def update(self, platforms, coin_blocks, enemies):
        """Actualizar estado del personaje"""
        if self.is_dying:
            self.death_animation()
            return

        if self.is_winning:
            self.win_animation()
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
                if self.velocity_y > 0:  # Solo aterriza si cae desde arriba
                    self.rect.y = platform.rect.top - self.rect.height
                    self.velocity_y = 0
                    self.on_ground = True
                else:  # Evita atravesar la plataforma desde abajo
                    self.rect.y = platform.rect.bottom
                    self.velocity_y = GRAVITY

        # Verificar colisiones con enemigos
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect) and enemy.alive:
                if self.velocity_y > 0 and self.rect.bottom - enemy.rect.top < 10:
                    self.velocity_y = JUMP_POWER  # Rebota tras pisar al enemigo
                    enemy.die()
                else:
                    self.die()

        # Determinar sprite
        if not self.on_ground:
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
        """Inicia la animación de muerte"""
        self.is_dying = True
        self.death_frame = 0
        self.death_timer = 0
        self.velocity_y = 0  # Detiene el movimiento

    def death_animation(self):
        """Ejecuta la animación de muerte cuadro a cuadro."""
        self.death_timer += 1
        if self.death_timer % DEATH_ANIMATION_SPEED == 0:
            if self.death_frame < len(self.sprites["dead"]) - 1:
                self.death_frame += 1
            else:
                self.alive = False  # Marcamos como muerto al final de la animación

        self.image = self.sprites["dead"][self.death_frame]

    def win(self):
        """Inicia la animación de victoria"""
        self.is_winning = True
        self.win_frame = 0
        self.win_timer = 0
        self.velocity_y = 0  # Detiene el movimiento

    def win_animation(self):
        """Ejecuta la animación de victoria cuadro a cuadro."""
        self.win_timer += 1
        if self.win_timer % DEATH_ANIMATION_SPEED == 0:
            self.win_frame = (self.win_frame + 1) % len(self.sprites["win"])

        self.image = self.sprites["win"][self.win_frame]

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
