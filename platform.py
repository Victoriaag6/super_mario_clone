import pygame

class Platform:
    def __init__(self, x, y, width, height, texture_path="assets/brick.jpg"):
        self.rect = pygame.Rect(x, y, width, height)
        self.texture = pygame.image.load(texture_path).convert()  # Cargar imagen optimizada

        # Escalar la textura al tamaño de la plataforma
        self.texture = pygame.transform.scale(self.texture, (width, height))

    def draw(self, screen):
        """Dibuja la plataforma con la textura ajustada al tamaño exacto"""
        screen.blit(self.texture, self.rect.topleft)
