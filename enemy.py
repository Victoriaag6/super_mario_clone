import pygame

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = 2
        self.alive = True  # Estado del enemigo

    def update(self):
        if not self.alive:
            return  # No moverse si está muerto
        
        self.rect.x += self.speed
        if self.rect.x > 700 or self.rect.x < 500:
            self.speed *= -1

    def die(self):
        """Eliminar al enemigo cuando Peach lo pisa."""
        self.alive = False

    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)
