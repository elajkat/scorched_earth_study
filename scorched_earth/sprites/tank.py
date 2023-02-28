import math
import pygame

from scorched_earth import game_constants


class Tank(pygame.sprite.Sprite):
    def __init__(self, game_screen, x, height_map, color=game_constants.RED):
        super().__init__()
        self.game_screen = game_screen
        self.height_map = height_map
        self.x = x
        self.y = self.height_map[self._count_x_earth_pos(x)] - 10
        self.color = color
        self.height = 15
        self.width = 25
        self.turret_width = 3
        self.turret_length = int(self.width / 2) + 5
        self.tank_sound = pygame.mixer.Sound(
            'gadgets/sounds/tank_moves.mp3',
        )
        self.turret_sound = pygame.mixer.Sound(
            'gadgets/sounds/tank_turret_moves.mp3',
        )
        self.bullets = []

        self._power = 30
        self._angle = 0
        self._health = 100

        self._active = False
        self._draw(self.x, self.y)

    def _count_x_earth_pos(self, x):
        return x - (x % game_constants.TERRA_BLOCK_X)

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, power):
        self._power = power

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        self._angle = angle

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, health):
        self._health = health

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, active):
        self._active = active

    def _draw(self, x, y):
        self.image = pygame.Surface(
            [self.width, self.height], pygame.SRCALPHA, 32
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        pygame.draw.circle(
            self.image,
            self.color,
            (int(self.width / 2), self.height - int(self.height / 3)),
            int(self.height / 4 * 2),
        )
        pygame.draw.rect(
            self.image,
            self.color,
            pygame.Rect(
                (
                    0,
                    self.height - int(self.height / 3),
                    self.width,
                    int(self.height / 3),
                )
            ),
        )

        t_cntr_x = int(self.width / 2)
        t_cntr_y = int(self.height / 2) - 2
        angle_rad = math.radians(self.angle)
        self.turret_end_x = t_cntr_x + int(
            math.sin(angle_rad) * self.turret_length
        )
        self.turret_end_y = t_cntr_y - int(
            math.cos(angle_rad) * self.turret_length
        )
        pygame.draw.line(
            self.image,
            game_constants.BLACK,
            (t_cntr_x, t_cntr_y),
            (self.turret_end_x, self.turret_end_y),
            self.turret_width,
        )
        self._draw_health_bar()

    def _draw_health_bar(self):
        color_diff = int((255 * self._health) / 100)
        bar_color = (255 - color_diff, 255, 255 - color_diff)
        pygame.draw.line(
            self.image,
            game_constants.BLACK,
            (0, self.height - 3),
            (self.width, self.height - 3),
        )
        pygame.draw.line(
            self.image,
            bar_color,
            (3, self.height - 2),
            (self.width - 3, self.height - 2),
            2,
        )

    def stop_motion(self):
        self.tank_sound.stop()
        self.turret_sound.stop()

    def update(self):
        if self._active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.tank_sound.play()
                self.rect.x -= 1
            if keys[pygame.K_RIGHT]:
                self.tank_sound.play()
                self.rect.x += 1
            if keys[pygame.K_DOWN] and self.power > 1:
                self.power -= 1
            if keys[pygame.K_UP] and self.power < 100:
                self.power += 1
            if keys[pygame.K_w] and self.angle < 91:
                self.turret_sound.play()
                self.angle += 1
                self._draw(self.rect.x, self.rect.y)
            if keys[pygame.K_q] and self.angle >= -90:
                self.turret_sound.play()
                self.angle -= 1
                self._draw(self.rect.x, self.rect.y)
            self.rect.y = (
                self.height_map[self._count_x_earth_pos(self.rect.x)] - 10
            )
            self._draw_health_bar()
