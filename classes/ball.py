import pygame
from pygame import Vector2


class Ball:
    pos: Vector2
    direction: Vector2
    velocity: float
    radius: int = 10

    def __init__(self, x: float, y: float, speed: float) -> None:
        self.x = x
        self.y = y
        self.direction = Vector2().normalize()
        self.velocity = speed

    def update_pos(self):
        self.pos += self.velocity * self.direction

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255),
                           (self.pos.x, self.pos.y), self.radius)
