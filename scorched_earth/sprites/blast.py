import pygame
import random

from scorched_earth import game_constants


class Blast(pygame.sprite.Sprite):
    def __init__(self, x, y, radius=10):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = radius
        self.current_radius = self.radius / 2
        self.color = game_constants.RED
        self.image = pygame.Surface(
            [2 * self.radius, 2 * self.radius], pygame.SRCALPHA, 32
        )
        pygame.draw.circle(
            self.image,
            self.color,
            (int(self.radius), int(self.radius)),
            self.current_radius,
        )
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        if self.current_radius <= self.radius:
            self.current_radius += 1
            self.color = (255, random.randint(0, 255), random.randint(0, 255))
            pygame.draw.circle(
                self.image,
                self.color,
                (int(self.radius / 2), int(self.radius / 2)),
                self.current_radius,
            )
            return
        if self.current_radius == self.radius:
            self.color = game_constants.WHITE
            pygame.draw.circle(
                self.image,
                self.color,
                (int(self.radius / 2), int(self.radius / 2)),
                self.current_radius,
            )
        self.kill()
