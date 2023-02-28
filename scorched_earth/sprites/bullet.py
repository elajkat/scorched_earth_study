import math
import pygame

from scorched_earth import game_constants


class Bullet(pygame.sprite.Sprite):
    GRAVITY = -9.8  # Earth

    def __init__(self, start_x, start_y, velocity, angle):
        super().__init__()
        self.image = pygame.Surface([4, 4])
        pygame.draw.circle(self.image, game_constants.RED, (2, 2), 2)
        self.rect = self.image.get_rect()
        self.start_x = start_x
        self.start_y = start_y
        self.rect.x = start_x
        self.rect.y = start_y
        self.angle = angle

        # Physics
        self.start_time = pygame.time.get_ticks()  # "now" in milliseconds
        self.velocity = velocity
        # Note: convert Degrees toRadians
        self.angle_rad = math.radians(self.angle)

    def update(self):
        time_now = pygame.time.get_ticks()
        if self.velocity > 0:
            time_change = time_now - self.start_time
            if time_change > 0:
                # fudge for metres/second to pixels/millisecond
                time_change /= 100.0
                # re-calculate the displacement
                # x
                displacement_x = (
                    self.velocity * time_change * math.sin(self.angle_rad)
                )
                # y
                half_gravity_time_squared = (
                    self.GRAVITY * time_change * time_change / 2.0
                )
                displacement_y = (
                    self.velocity * time_change * math.cos(self.angle_rad)
                    + half_gravity_time_squared
                )

                # reposition sprite (subtract y, because in pygame 0 is
                # screen-top)
                self.rect.center = (
                    self.start_x + int(displacement_x),
                    self.start_y - int(displacement_y),
                )
