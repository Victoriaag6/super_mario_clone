import pygame

class Enemy:
    def __init__(self, x, y, speed=2, frames_folder="assets/goomba/"):
        self.rect = pygame.Rect(x, y, 40, 40)  # Tamaño del enemigo
        self.speed = speed  # Velocidad de movimiento
        self.direction = 1  # 1 = Derecha, -1 = Izquierda
        self.frame_index = 0  # Índice de animación
        self.animation_speed = 0.15  # Velocidad de cambio de frames

        # Cargar sprites de animación (asegúrate de que los nombres coincidan)
        self.frames = [
            pygame.image.load(frames_folder + "frame1.png"),
            pygame.image.load(frames_folder + "frame2.png"),
            pygame.image.load(frames_folder + "frame3.png"),
            pygame.image.load(frames_folder + "frame4.png"),
            pygame.image.load(frames_folder + "frame5.png"),
            pygame.image.load(frames_folder + "frame6.png")
        ]

        self.image = self.frames[0]  # Frame inicial

    def update(self):
        """Actualizar posición y animación del enemigo"""
        self.rect.x += self.speed * self.direction  # Mover el enemigo
        self.frame_index += self.animation_speed  # Avanzar en la animación

        # Resetear la animación cuando llegue al final de los frames
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        
        # Actualizar sprite
        self.image = self.frames[int(self.frame_index)]

    def change_direction(self):
        """Cambiar de dirección cuando choca con un borde"""
        self.direction *= -1

    def draw(self, screen):
        """Dibujar el enemigo en la pantalla"""
        screen.blit(self.image, self.rect.topleft)
