import pygame

class Enemy:
    def __init__(self, x, y, speed=2, size=(30, 30), frames_folder="assets/goomba/"):
        """Inicializa el enemigo con animación"""
        # Guardar posición inicial para poder hacer reset
        self.start_x = x
        self.start_y = y
        
        self.rect = pygame.Rect(x, y, *size)
        self.speed = speed
        self.direction = -1  # -1 significa que empieza moviéndose a la izquierda
        self.alive = True  # Estado del enemigo
        self.frame_index = 0
        self.animation_speed = 0.15

        # Cargar y escalar los frames de movimiento
        self.frames = [
            pygame.transform.scale(pygame.image.load(frames_folder + "frame1.png"), size),
            pygame.transform.scale(pygame.image.load(frames_folder + "frame2.png"), size),
            pygame.transform.scale(pygame.image.load(frames_folder + "frame3.png"), size),
            pygame.transform.scale(pygame.image.load(frames_folder + "frame4.png"), size),
            pygame.transform.scale(pygame.image.load(frames_folder + "frame5.png"), size),
            pygame.transform.scale(pygame.image.load(frames_folder + "frame6.png"), size),
        ]

        # Cargar y escalar los frames de muerte al mismo tamaño
        self.death_frames = [
            pygame.transform.scale(pygame.image.load(frames_folder + "dead1.png"), size),
            pygame.transform.scale(pygame.image.load(frames_folder + "dead2.png"), size),
            pygame.transform.scale(pygame.image.load(frames_folder + "dead3.png"), size),
        ]

        self.image = self.frames[0]  # Imagen inicial
        self.death_index = 0
        self.death_timer = 0

    def update(self, platforms):
        """Actualizar la posición y animación del enemigo"""
        if self.alive:
            # Mover al enemigo
            old_x = self.rect.x
            self.rect.x += self.speed * self.direction

            # Verificar si sale de la pantalla (0, WIDTH)
            if self.rect.left < 0 or self.rect.right > 800:
                # Regresar a la posición anterior y cambiar de dirección
                self.rect.x = old_x
                self.change_direction()

            # Animación de caminar
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            self.image = self.frames[int(self.frame_index)]
        else:
            self.death_animation()

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.direction == 1 and self.rect.right > platform.rect.right:
                    self.rect.right = platform.rect.right
                    self.direction = -1
                elif self.direction == -1 and self.rect.left < platform.rect.left:
                    self.rect.left = platform.rect.left
                    self.direction = 1

    def change_direction(self):
        """Invierte la dirección cuando choca con un límite"""
        self.direction *= -1

    def die(self):
        """Inicia la animación de muerte"""
        self.alive = False
        self.death_index = 0
        self.death_timer = 0

    def death_animation(self):
        """Ejecuta la animación de muerte"""
        self.death_timer += 1
        if self.death_timer % 10 == 0:  # Cambia de frame cada 10 ciclos
            if self.death_index < len(self.death_frames) - 1:
                self.death_index += 1
            else:
                self.image = self.death_frames[-1]  # Mantiene el último frame

        self.image = self.death_frames[self.death_index]

    def draw(self, screen):
        """Dibuja el enemigo en pantalla"""
        screen.blit(self.image, self.rect.topleft)

    def reset(self):
        """Revive el enemigo cuando el juego se reinicia"""
        self.alive = True
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.image = self.frames[0]
        self.death_index = 0
        self.death_timer = 0
        self.direction = -1
