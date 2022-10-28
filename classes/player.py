import pygame


class Player:
    x: int
    y: int
    life: int
    speed: int
    border_y: int
    size_x = 10
    size_y = 60

    closest_point = pygame.Vector2(1, 1)
    normal_vector = pygame.Vector2(1, 1)

    def __init__(self, x, y, life, speed):
        self.x = x
        self.y = y
        self.life = life
        self.speed = speed
        self.border_y = 600

        self.closest_point = pygame.Vector2(1, 1)
        self.normal_vector = pygame.Vector2(1, 1)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255),
                         (self.x, self.y, self.size_x, self.size_y))

    def move(self, direction):
        self.y += direction * self.speed
        if self.y + self.size_y > self.border_y:
            self.y = self.border_y - self.size_y
        if self.y < 0:
            self.y = 0
