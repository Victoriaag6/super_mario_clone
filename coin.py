import pygame

class Coin:
    def __init__(self, x, y, size=(20, 20), frames_folder="assets/coin/", bounce=False):
        """Inicializa la moneda animada con opción de rebote"""
        self.rect = pygame.Rect(x, y, *size)  # Tamaño ajustado
        self.frame_index = 0
        self.animation_speed = 0.15
        self.size = size
        self.bounce = bounce  # Define si la moneda rebota al salir
        self.bounce_timer = 0
        self.bounce_height = 15  # Altura del rebote

        # Cargar y escalar los frames de la moneda
        self.frames = [
            pygame.transform.scale(pygame.image.load(frames_folder + "frame1.png"), size),
            pygame.transform.scale(pygame.image.load(frames_folder + "frame2.png"), size),
            pygame.transform.scale(pygame.image.load(frames_folder + "frame3.png"), size),
            pygame.transform.scale(pygame.image.load(frames_folder + "frame4.png"), size),
            pygame.transform.scale(pygame.image.load(frames_folder + "frame5.png"), size),
            pygame.transform.scale(pygame.image.load(frames_folder + "frame6.png"), size),
            pygame.transform.scale(pygame.image.load(frames_folder + "frame7.png"), size),
            pygame.transform.scale(pygame.image.load(frames_folder + "frame8.png"), size),
        ]

        self.image = self.frames[0]  # Imagen inicial
        self.collected = False  # Estado de recolección

    def update(self):
        """Actualiza la animación de la moneda y maneja el rebote."""
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

        # Efecto de rebote si fue generada desde un bloque
        if self.bounce and self.bounce_timer < 10:
            self.rect.y -= 2  # Mueve la moneda hacia arriba
            self.bounce_timer += 1
        elif self.bounce and self.bounce_timer >= 10:
            self.bounce = False  # Desactiva el rebote después de un tiempo

    def draw(self, screen):
        """Dibuja la moneda en pantalla."""
        if not self.collected:
            screen.blit(self.image, self.rect.topleft)

    def collect(self):
        """Marca la moneda como recogida."""
        self.collected = True
