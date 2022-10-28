import random
import pygame
from pygame import Vector2
from classes.player import Player


class Ball:
    pos: Vector2
    direction: Vector2
    velocity: float
    radius: int = 8
    border_x: int = 600
    border_y: int = 600

    # closest_point: Vector2 = Vector2(0, 0)
    # normal_vector: Vector2 = Vector2(1, -1)

    screen = None

    def __init__(self, x: float, y: float, speed: float, screen=None) -> None:
        self.pos = Vector2(x, y)
        self.direction = Vector2(1, 0).normalize()
        self.velocity = speed
        self.screen = screen

    def move(self):
        self.pos += self.velocity * self.direction

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255),
                           (self.pos.x, self.pos.y), self.radius)

    def reflect(self, normal_vector):
        self.direction = self.direction.reflect(normal_vector)

    def get_closest_from_inside(plr):
        pass

    def collide_plr(self, plr: Player):
        # self.closest_point = Vector2(0, 0)
        # box_mid = Vector2(plr.x + plr.size_x / 2, plr.y + plr.size_y / 2)
        is_left = False
        is_right = False
        is_inside = False
        # normal_vector = Vector2(0, 0)

        if self.pos.x < plr.x:
            is_left = True
        elif self.pos.x > plr.x + plr.size_x:
            is_right = True

        # print(self.pos, plr.x, plr.y)
        if self.pos.y <= plr.y:
            # Pos above player
            if is_right:  # Top right corner closest
                plr.closest_point = Vector2(plr.x + plr.size_x, plr.y)
                plr.normal_vector = Vector2(1, -1)
            elif is_left:  # Top left corner
                plr.closest_point = Vector2(plr.x, plr.y)
                plr.normal_vector = Vector2(-1, -1)
            else:  # top
                plr.closest_point = Vector2(self.pos.x, plr.y)
                plr.normal_vector = Vector2(0, -1)
        elif self.pos.y >= plr.y + plr.size_y:
            # Pos below player
            if is_right:    # Bottom right
                plr.closest_point = Vector2(
                    plr.x + plr.size_x, plr.y + plr.size_y)
                plr.normal_vector = Vector2(1, 1)
            elif is_left:  # Bottom left
                plr.closest_point = Vector2(plr.x, plr.y + plr.size_y)
                plr.normal_vector = Vector2(-1, 1)
            else:  # bottom
                plr.closest_point = Vector2(self.pos.x, plr.y + plr.size_y)
                plr.normal_vector = Vector2(0, 1)
        else:
            # Pos same level as player
            if is_right:  # right
                plr.closest_point = Vector2(plr.x + plr.size_x, self.pos.y)
                plr.normal_vector = Vector2(1, 0)
            elif is_left:  # left
                plr.closest_point = Vector2(plr.x, self.pos.y)
                plr.normal_vector = Vector2(-1, 0)
            else:  # inside
                # Vector2(self.pos.x, plr.y + plr.size_y) # POS INSIDE PLR?
                # self.velocity += plr.speed
                is_inside = True
                print("CODE RED", plr.closest_point, plr.normal_vector)

        if (self.pos.distance_squared_to(plr.closest_point) <= self.radius ** 2) or is_inside:
            # COLLISION
            # self.velocity += 0.1
            self.pos = plr.closest_point + self.radius * plr.normal_vector
            self.reflect(plr.normal_vector +
                         Vector2(random.randint(-1, 1)/100, random.randint(-1, 1)/100))

        pygame.draw.line(self.screen, (255, 0, 0), (self.pos.x,
                         self.pos.y), (plr.closest_point.x, plr.closest_point.y))

    def collide(self, players):
        # Walls
        # Top
        if self.pos.y - self.radius <= 0:
            self.pos.y = self.radius
            self.reflect(Vector2(0, 1))
            # print("Hit top")
        # Right
        if self.pos.x + self.radius >= self.border_x:
            self.pos.x = self.border_x - self.radius
            self.reflect(Vector2(-1, 0))
            # print("Hit right")
        # Bottom
        if self.pos.y + self.radius >= self.border_y:
            self.pos.y = self.border_y - self.radius
            self.reflect(Vector2(0, -1))
            # print("Hit bottom")
        # Left
        if self.pos.x - self.radius <= 0:
            self.pos.x = self.radius
            self.reflect(Vector2(1, 0))
            # print("Hit left")

        # Players
        for plr in players:
            self.collide_plr(plr)
