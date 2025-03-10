import pygame
from coin import Coin

class CoinBlock:
    def __init__(self, x, y, width=40, height=40):
        """Inicializa el bloque con un máximo de monedas disponibles"""
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load("assets/coinBlock.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.max_coins = 5  # El bloque puede soltar hasta 5 monedas
        self.coins_left = self.max_coins  # Contador de monedas restantes
        self.used = False  # Indica si el bloque ha sido golpeado completamente

    def hit(self):
        """Genera una moneda si hay monedas disponibles"""
        if self.coins_left > 0:
            self.coins_left -= 1
            return Coin(self.rect.x + 10, self.rect.y - 30, bounce=True)  # La moneda rebota al salir
        else:
            self.used = True  # El bloque queda vacío después de soltar todas sus monedas
        return None

    def draw(self, screen):
        """Dibuja el bloque en pantalla"""
        screen.blit(self.image, self.rect.topleft)
