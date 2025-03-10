import pygame

class Enemy:
    def __init__(self, x, y, speed=2, size=(30, 30), frames_folder="assets/goomba/"):
        """Inicializa el enemigo con animación y movimiento"""
        self.rect = pygame.Rect(x, y, *size)
        self.speed = speed
        self.direction = -1  # Comienza moviéndose hacia la izquierda
        self.alive = True  # Estado del enemigo
        self.size = size

        # Cargar los frames de animación normales
        self.frames = [
            pygame.transform.scale(pygame.image.load(frames_folder + "frame1.png"), size),
            pygame.transform.scale(pygame.image.load(frames_folder + "frame2.png"), size),
            pygame.transform.scale(pygame.image.load(frames_folder + "frame3.png"), size),
            pygame.transform.scale(pygame.image.load(frames_folder + "frame4.png"), size),
            pygame.transform.scale(pygame.image.load(frames_folder + "frame5.png"), size),
            pygame.transform.scale(pygame.image.load(frames_folder + "frame6.png"), size),
        ]

        # Cargar animación de muerte
        self.dead_frames = [
            pygame.transform.scale(pygame.image.load(frames_folder + "dead1.png"), size),
            pygame.transform.scale(pygame.image.load(frames_folder + "dead2.png"), size),
            pygame.transform.scale(pygame.image.load(frames_folder + "dead3.png"), size),
        ]

        self.frame_index = 0
        self.animation_speed = 0.1
        self.image = self.frames[0]  # Usar el primer frame

        # Variables para la animación de muerte
        self.is_dying = False
        self.death_frame = 0
        self.death_timer = 0
        self.death_speed = 10  # Velocidad de la animación de muerte

    def update(self):
        """Mueve y actualiza la animación del enemigo"""
        if self.is_dying:
            self.death_animation()
            return

        if self.alive:
            self.rect.x += self.speed * self.direction

            # Actualizar animación
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            self.image = self.frames[int(self.frame_index)]  # Mantener tamaño original

    def die(self):
        """Mata al enemigo y activa la animación de muerte"""
        self.is_dying = True
        self.death_frame = 0
        self.death_timer = 0
        self.speed = 0  # Detener movimiento

    def death_animation(self):
        """Ejecuta la animación de muerte cuadro a cuadro."""
        self.death_timer += 1
        if self.death_timer % self.death_speed == 0:
            if self.death_frame < len(self.dead_frames) - 1:
                self.death_frame += 1
            else:
                self.alive = False  # Desaparece tras la animación
        
        self.image = self.dead_frames[self.death_frame]

    def change_direction(self):
        """Cambia la dirección del enemigo cuando llega al borde"""
        self.direction *= -1

    def draw(self, screen):
        """Dibuja el enemigo si está vivo"""
        if self.alive or self.is_dying:
            screen.blit(self.image, self.rect.topleft)
