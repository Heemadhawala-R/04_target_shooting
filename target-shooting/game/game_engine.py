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

- Task 4: 30-second timed rounds


"""

import random
import time

from game.target import Target
from game.hit_detection import check_hit
from game.renderer import WIDTH, HEIGHT

NUM_TARGETS = 3
TARGET_RADIUS = 28
ROUND_DURATION = 30


class GameEngine:
    def __init__(self):
        self.start_round()

    def start_round(self):
        """Start or restart a 30-second round."""

        self.targets = [
            self._random_target(0),
            self._random_target(1),
            self._random_target(2),
        ]

        self.hits = 0
        self.misses = 0

        self.score = 0
        self.combo = 0

        self.start_time = time.time()
        self.time_left = ROUND_DURATION
        self.round_over = False

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
        """Handle a click only while the round is active."""

        # Don't accept clicks after the round ends
        if self.round_over:
            return

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
        """Update timer and target movement."""

        if self.round_over:
            return

        elapsed = time.time() - self.start_time
        self.time_left = max(0, ROUND_DURATION - int(elapsed))

        if self.time_left <= 0:
            self.time_left = 0
            self.round_over = True
            return

        for target in self.targets:
            target.update(WIDTH, HEIGHT)

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(surface, self.targets)

        renderer.draw_text(
            surface,
            font,
            f"Time: {self.time_left}",
            (10, 10)
        )

        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}",
            (10, 35)
        )

        renderer.draw_text(
            surface,
            font,
            f"Combo: x{self.combo}",
            (10, 60)
        )

        renderer.draw_text(
            surface,
            font,
            f"Hits: {self.hits}  Misses: {self.misses}",
            (10, 85)
        )

        if self.round_over:
            renderer.draw_banner(
                surface,
                font,
                f"ROUND OVER! Score: {self.score} | Press R to Restart"
            )