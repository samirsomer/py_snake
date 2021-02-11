import pygame
import random
from enum import Enum
from collections import namedtuple
from config import *

pygame.init()
font = pygame.font.Font("./resources/fonts/ARIALI.TTF", 25)
# or
# font = pygame.font.SysFont("arial", 25)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple("Point", "x, y")

# RGB Colors
RED = COLORS["RED"]
WHITE = COLORS["WHITE"]
BLACK = COLORS["BLACK"]
BLUE1 = COLORS["BLUE1"]
BLUE2 = COLORS["BLUE2"]
# Variables
BLOCK_SIZE = OPTIONS["BLOCK_SIZE"]
SPEED = OPTIONS["GAME_SPEED"]


class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - (2 * BLOCK_SIZE), self.head.y),
        ]

        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        # move snake
        self._move(self.direction)
        self.snake.insert(0, self.head)
        # check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
        # place new food or move snake
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        # update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # return game over and score

        return game_over, self.score

    def _is_collision(self):
        # if it hits  boundries
        if (
            self.head.x > self.w - BLOCK_SIZE
            or self.head.x < 0
            or self.head.y > self.h - BLOCK_SIZE
            or self.head.y < 0
        ):
            return True
        # if it hits itself
        if self.head in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(BLACK)
        for point in self.snake:
            pygame.draw.rect(
                self.display,
                BLUE1,
                pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE),
            )
            pygame.draw.rect(
                self.display, BLUE1, pygame.Rect(point.x + 4, point.y + 4, 12, 12)
            )
        pygame.draw.rect(
            self.display,
            RED,
            pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE),
        )

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == direction.UP:
            y -= BLOCK_SIZE
        elif direction == direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x, y)


if __name__ == "__main__":
    game = SnakeGame()

    # game loop
    while True:
        game_over, score = game.play_step()

        # break if game over
        if game_over:
            break

    print("Final Score: {}".format(score))

    pygame.quit()