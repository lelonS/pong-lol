import pygame


class Player:
    x: int
    y: int
    life: int
    speed: int
    border_y: int

    def __init__(self, x, y, life, speed):
        self.x = x
        self.y = y
        self.life = life
        self.speed = speed
        self.border_y = 600

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, 10, 60))

    def move(self, direction):
        self.y += direction * self.speed
        if self.y + 60 > self.border_y:
            self.y = self.border_y - 60
        if self.y < 0:
            self.y = 0