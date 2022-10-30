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

    plrs_info = []

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

    def collide_plr(self, plr: Player, plr_info: int):
        # box_mid = Vector2(plr.x + plr.size_x / 2, plr.y + plr.size_y / 2)
        is_left = False
        is_right = False
        is_inside = False

        if self.pos.x < plr.x:
            is_left = True
        elif self.pos.x > plr.x + plr.size_x:
            is_right = True

        if self.pos.y <= plr.y:
            # Pos above player
            if is_right:  # Top right corner closest
                plr_info["closest_point"] = Vector2(plr.x + plr.size_x, plr.y)
                plr_info["normal_vector"] = (
                    self.pos-plr_info["closest_point"]).normalize()
            elif is_left:  # Top left corner
                plr_info["closest_point"] = Vector2(plr.x, plr.y)
                plr_info["normal_vector"] = (
                    self.pos-plr_info["closest_point"]).normalize()
            else:  # top
                plr_info["closest_point"] = Vector2(self.pos.x, plr.y)
                plr_info["normal_vector"] = Vector2(0, -1)
        elif self.pos.y >= plr.y + plr.size_y:
            # Pos below player
            if is_right:    # Bottom right
                plr_info["closest_point"] = Vector2(
                    plr.x + plr.size_x, plr.y + plr.size_y)
                plr_info["normal_vector"] = (
                    self.pos-plr_info["closest_point"]).normalize()
            elif is_left:  # Bottom left
                plr_info["closest_point"] = Vector2(plr.x, plr.y + plr.size_y)
                plr_info["normal_vector"] = (
                    self.pos-plr_info["closest_point"]).normalize()
            else:  # bottom
                plr_info["closest_point"] = Vector2(
                    self.pos.x, plr.y + plr.size_y)
                plr_info["normal_vector"] = Vector2(0, 1)
        else:
            # Pos same level as player
            if is_right:  # right
                plr_info["closest_point"] = Vector2(
                    plr.x + plr.size_x, self.pos.y)
                plr_info["normal_vector"] = Vector2(1, 0)
            elif is_left:  # left
                plr_info["closest_point"] = Vector2(plr.x, self.pos.y)
                plr_info["normal_vector"] = Vector2(-1, 0)
            else:  # inside
                is_inside = True
                print("CODE RED",
                      plr_info["closest_point"], plr_info["normal_vector"])

        dist_sq = self.pos.distance_squared_to(plr_info["closest_point"])

        if (dist_sq <= self.radius ** 2) or is_inside:
            # COLLISION
            self.pos = plr_info["closest_point"] + \
                self.radius * plr_info["normal_vector"]
            self.reflect(plr_info["normal_vector"])

        pygame.draw.line(self.screen, (255, 0, 0), (self.pos.x, self.pos.y),
                         (plr_info["closest_point"].x,
                          plr_info["closest_point"].y))

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
        if len(self.plrs_info) < len(players):
            self.plrs_info += [{"closest_point": Vector2(0, 0),
                               "normal_vector": Vector2(0, 0)}] * \
                (len(players) - len(self.plrs_info))

        for i, plr in enumerate(players):
            self.collide_plr(plr, self.plrs_info[i])
