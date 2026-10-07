"""
GameEngine: owns the targets and handles player clicks.

Starter version: a few static targets that respawn elsewhere when
clicked (correctly or not, depending on the hit-detection bug) - no
movement, no score/combo, no timer yet. That's Tasks 2-4.
"""

"""
Task 2:
- Targets move continuously
- Targets have different movement speeds/patterns
- Targets bounce off the edges

Task 3:
- Score increases with consecutive hits
- Combo multiplier increases with consecutive hits
- A miss resets the combo

"""

import random

from game.target import Target
from game.hit_detection import check_hit
from game.renderer import WIDTH, HEIGHT

NUM_TARGETS = 3
TARGET_RADIUS = 28


class GameEngine:
    def __init__(self):
        self.targets = [
            self._random_target(0),
            self._random_target(1),
            self._random_target(2),
        ]

        self.hits = 0
        self.misses = 0

        # Task 3: scoring and combo
        self.score = 0
        self.combo = 0

    def _random_target(self, movement_type=None):
        x = random.randint(
            TARGET_RADIUS + 10,
            WIDTH - TARGET_RADIUS - 10
        )

        y = random.randint(
            TARGET_RADIUS + 10,
            HEIGHT - TARGET_RADIUS - 10
        )

        if movement_type is None:
            movement_type = random.randint(0, 2)

        # Different movement speeds/patterns
        if movement_type == 0:
            speed_x = 2
            speed_y = 1

        elif movement_type == 1:
            speed_x = -3
            speed_y = 2

        else:
            speed_x = 1
            speed_y = -3

        return Target(
            x,
            y,
            radius=TARGET_RADIUS,
            speed_x=speed_x,
            speed_y=speed_y
        )

    def handle_click(self, pos):
        target = check_hit(self.targets, pos)

        if target is not None:
            self.hits += 1

            self.combo += 1

            self.score += 10 * self.combo

            self.targets.remove(target)

            self.targets.append(self._random_target())

        else:
            
            self.misses += 1

            self.combo = 0

    def update(self):
        """Move all targets."""

        for target in self.targets:
            target.update(WIDTH, HEIGHT)

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(surface, self.targets)

        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}",
            (10, 10)
        )

        renderer.draw_text(
            surface,
            font,
            f"Combo: x{self.combo}",
            (10, 35)
        )

        renderer.draw_text(
            surface,
            font,
            f"Hits: {self.hits}  Misses: {self.misses}",
            (10, 60)
        )