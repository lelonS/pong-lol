from math import atan, degrees
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

    def __init__(self, x: float, y: float, speed: float) -> None:
        self.pos = Vector2(x, y)
        self.direction = Vector2(1, 0).normalize()
        self.velocity = speed

    def move(self):
        self.pos += self.velocity * self.direction

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255),
                           (self.pos.x, self.pos.y), self.radius)

    def reflect(self, normal_vector):
        self.direction = self.direction.reflect(normal_vector)

    def collide_plr(self, plr: Player):
        dist_x = abs(self.pos.x - (plr.x + plr.size_x / 2))
        dist_y = abs(self.pos.y - (plr.y + plr.size_y / 2))
        # Check if inside box
        if dist_x > plr.size_x/2 + self.radius:
            return
        if dist_y > plr.size_y/2 + self.radius:
            return
        # Check closest edge

        dist_up = abs(self.pos.y - plr.y)
        dist_down = abs(self.pos.y - (plr.y + plr.size_y))
        dist_right = abs(self.pos.x - (plr.x + plr.size_x))
        dist_left = abs(self.pos.x - plr.x)

        current_lowest = dist_up
        current_surface = Vector2(0, -1)
        new_x = self.pos.x
        new_y = plr.y - self.radius

        if dist_down < current_lowest:
            current_lowest = dist_down
            current_surface = Vector2(0, 1)
            new_x = self.pos.x
            new_y = plr.y + plr.size_y + self.radius
        if dist_right < current_lowest:
            current_lowest = dist_right
            current_surface = Vector2(1, 0)
            new_x = plr.x + plr.size_x + self.radius
            new_y = self.pos.y
        if dist_left < current_lowest:
            current_lowest = dist_left
            current_surface = Vector2(-1, 0)
            new_x = plr.x - self.radius
            new_y = self.pos.y

        # CORNER TESTS
        # sin(corner_deg) = plr.size_y / plr.size_x
        box_mid = Vector2(plr.x + plr.size_x / 2, plr.y + plr.size_y / 2)
        deg = Vector2(1, 0).angle_to(self.pos - box_mid)
        interval_deg = 7
        corner_deg = degrees(atan(plr.size_y / plr.size_x))
        corners = [corner_deg, 180 - corner_deg,
                   180 + corner_deg, 360 - corner_deg]

        hit_corner = False
        deg_normal = deg % 360

        print(corners, deg, deg_normal)
        for corner in corners:
            if (corner - interval_deg) % 360 <= deg_normal <= (corner + interval_deg) % 360:
                hit_corner = True
                break
        if hit_corner:
            self.direction = (self.pos - box_mid).normalize()
            # TODO POS STUFF
            print("HIT CORNER")
        else:
            self.pos = Vector2(new_x, new_y)  # WIP?
            self.reflect(current_surface)

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
