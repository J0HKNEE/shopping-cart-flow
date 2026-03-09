import random
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Tuple

import pygame

# --- Constants & Configuration (PEP 8) ---
BLOCK_SIZE = 20
SPEED = 15
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Colors (Expressed as RGB Tuples)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (200, 0, 0)
COLOR_GREEN_LIGHT = (0, 255, 0)
COLOR_GREEN_DARK = (0, 150, 0)


class Direction(Enum):
    """Enumeration for movement to prevent logic errors."""

    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


@dataclass(frozen=True)
class Point:
    """Immutable coordinate point (The Data Model)."""

    x: int
    y: int


class SnakeGame:
    def __init__(self, width: int = SCREEN_WIDTH, height: int = SCREEN_HEIGHT):
        self.w = width
        self.h = height

        # Initialize display
        pygame.init()
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake: Engineered Edition")
        self.clock = pygame.time.Clock()

        # Initial Game State
        self.direction = Direction.RIGHT
        self.head = Point(self.w // 2, self.h // 2)
        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - (2 * BLOCK_SIZE), self.head.y),
        ]

        self.score = 0
        self.food: Optional[Point] = None
        self._place_food()

    def _place_food(self) -> None:
        """Helper to place food randomly on the grid."""
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self) -> Tuple[bool, int]:
        """The core game loop step (Logic & Event Handling)."""
        # 1. Collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN

        # 2. Move
        self._move(self.direction)
        self.snake.insert(0, self.head)

        # 3. Check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # 4. Place new food or move tail
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # 5. Update UI and clock
        self._update_ui()
        self.clock.tick(SPEED)

        return game_over, self.score

    def _is_collision(self) -> bool:
        """Check boundaries and self-intersection."""
        # Hits boundary
        if (
            self.head.x > self.w - BLOCK_SIZE
            or self.head.x < 0
            or self.head.y > self.h - BLOCK_SIZE
            or self.head.y < 0
        ):
            return True
        # Hits itself
        if self.head in self.snake[1:]:
            return True
        return False

    def _update_ui(self) -> None:
        """Render the current state (The View)."""
        self.display.fill(COLOR_BLACK)

        # Draw Snake
        for pt in self.snake:
            pygame.draw.rect(
                self.display,
                COLOR_GREEN_DARK,
                pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE),
            )
            pygame.draw.rect(
                self.display,
                COLOR_GREEN_LIGHT,
                pygame.Rect(pt.x + 4, pt.y + 4, 12, 12),
            )

        # Draw Food
        pygame.draw.rect(
            self.display,
            COLOR_RED,
            pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE),
        )

        # Draw Score (using Pygame font)
        font = pygame.font.SysFont("arial", 25)
        text = font.render(f"Score: {self.score}", True, COLOR_WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction: Direction) -> None:
        """Update the head position based on direction."""
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)


if __name__ == "__main__":
    game = SnakeGame()

    # Game Loop
    while True:
        game_over, score = game.play_step()
        if game_over:
            break

    print(f"Final Score: {score}")
    pygame.quit()
