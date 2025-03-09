import pygame

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = 2

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 700 or self.rect.x < 500:
            self.speed *= -1

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
