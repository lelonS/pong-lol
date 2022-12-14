import pygame
from classes.ball import Ball
from classes.player import Player

pygame.init()

WIDTH = 600
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
CLOCK = pygame.time.Clock()


def draw(player1, player2, ball):
    SCREEN.fill((0, 0, 0))
    player1.draw(SCREEN)
    player2.draw(SCREEN)
    ball.draw(SCREEN)


def handle_keys_pressed(player1, player2):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player1.move(-1)
    if keys[pygame.K_s]:
        player1.move(1)
    if keys[pygame.K_o]:
        player2.move(-1)
    if keys[pygame.K_l]:
        player2.move(1)


def main():
    player1 = Player(50, 270, 10, 6)  # spawn player 1
    player2 = Player(550, 270, 10, 6)  # spawn player 2
    ball = Ball(300, 300, 5, screen=SCREEN)
    while True:
        # Frames
        CLOCK.tick(FPS)

        # Draw
        draw(player1, player2, ball)

        # Player movement
        handle_keys_pressed(player1, player2)

        # Ball movement
        ball.move()
        ball.collide([player1, player2])
        pygame.display.update()
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Close the program any way you want
                raise SystemExit


if __name__ == '__main__':
    main()
