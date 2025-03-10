import pygame
from coin import Coin

class CoinBlock:
    def __init__(self, x, y, width=40, height=40):
        """Inicializa el bloque que suelta monedas"""
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load("assets/coinBlock.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hit_count = 0  # Para evitar múltiples monedas saliendo

    def hit(self):
        """Genera una moneda si el bloque no ha sido golpeado antes"""
        if self.hit_count == 0:
            self.hit_count += 1
            return Coin(self.rect.x + 10, self.rect.y - 30, bounce=True)  # Moneda rebota al salir
        return None

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
