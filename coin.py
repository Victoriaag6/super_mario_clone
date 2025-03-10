import pygame

class Coin:
    def __init__(self, x, y, bounce=False):
        """Inicializa la moneda animada, con efecto de rebote si es generada desde un bloque"""
        self.rect = pygame.Rect(x, y, 20, 20)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.collected = False  # Estado de recolección
        self.bouncing = bounce  # Si es una moneda que salió de un bloque
        self.velocity_y = -8 if bounce else 0  # Rebote inicial solo si viene de un bloque

        # Cargar los frames de la moneda
        self.frames = [
            pygame.image.load("assets/coin/frame1.png"),
            pygame.image.load("assets/coin/frame2.png"),
            pygame.image.load("assets/coin/frame3.png"),
            pygame.image.load("assets/coin/frame4.png"),
        ]
        self.image = self.frames[0]

    def update(self):
        """Actualiza la animación de la moneda y simula su caída si fue generada desde un bloque"""
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

        if self.bouncing:
            self.rect.y += self.velocity_y
            self.velocity_y += 0.5  # Simula la caída
            if self.velocity_y > 5:  # Detiene la caída cuando toca el suelo
                self.bouncing = False

    def draw(self, screen):
        """Dibuja la moneda en pantalla si no ha sido recogida"""
        if not self.collected:
            screen.blit(self.image, self.rect.topleft)

    def collect(self):
        """Marca la moneda como recogida"""
        self.collected = True
