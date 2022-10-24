import pygame
from pygame import Vector2


class Ball:
    pos: Vector2
    direction: Vector2
    velocity: float
    radius: int = 8
    border_x: int = 600
    border_y: int = 600

    def __init__(self, x: float, y: float, speed: float) -> None:
        self.pos = Vector2(x, y)
        self.direction = Vector2(1, 2).normalize()
        self.velocity = speed

    def move(self):
        self.pos += self.velocity * self.direction

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255),
                           (self.pos.x, self.pos.y), self.radius)

    def reflect(self, normal_vector):
        self.direction = self.direction.reflect(normal_vector)

    def collide(self, players):
        if self.pos.y - self.radius <= 0:
            self.reflect(Vector2(0, 1))
            # print("Hit top")
        if self.pos.x + self.radius >= self.border_x:
            self.reflect(Vector2(-1, 0))
            # print("Hit right")
        if self.pos.y + self.radius >= self.border_y:
            self.reflect(Vector2(0, -1))
            # print("Hit bottom")
        if self.pos.x - self.radius <= 0:
            self.reflect(Vector2(1, 0))
            # print("Hit left")
