"""
Target: a circular target the player clicks on. (x, y) is the CENTER
of the circle - this matters for how it's drawn vs. how it's hit-tested.
"""
import pygame
class Target:
    def __init__(
        self,
        x,
        y,
        radius=28,
        color=(230, 90, 70),
        speed_x=2,
        speed_y=2,
    ):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self, width, height):
        """Move the target and bounce it off the edges."""

        self.x += self.speed_x
        self.y += self.speed_y

        if self.x - self.radius <= 0:
            self.x = self.radius
            self.speed_x *= -1

        elif self.x + self.radius >= width:
            self.x = width - self.radius
            self.speed_x *= -1

        if self.y - self.radius <= 0:
            self.y = self.radius
            self.speed_y *= -1

        elif self.y + self.radius >= height:
            self.y = height - self.radius
            self.speed_y *= -1

    def get_bounding_rect(self):
        """Return a rectangle around the target."""

        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2,
        )