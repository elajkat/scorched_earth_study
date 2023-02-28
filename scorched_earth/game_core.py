import pygame
import random

from scorched_earth import game_constants
from scorched_earth.sprites import blast as blast_mod
from scorched_earth.sprites import bullet as bullet_mod
from scorched_earth.sprites import tank as tank_mod
from scorched_earth.sprites import terrain as terrain_mod


class Game(object):
    def __init__(self, game_screen, clock, tank_colors):
        self.game_screen = game_screen
        self.clock = clock
        self.tank_colors = tank_colors
        self.done = False
        self.active_tank = 0

        self.base_tck = 60

        self.game_over = False

        self.all_sprites_list = pygame.sprite.Group()
        self.bullets_list = pygame.sprite.Group()
        self.tanks = []
        self.tanks_group = pygame.sprite.Group()
        self.blast_list = pygame.sprite.Group()
        self.earth_blocks = pygame.sprite.Group()

        self.height_map = {}
        self._draw_terrain()

        # TODO(lajoskatona): ugly dependence on 2 tanks/players
        for index, color in enumerate(self.tank_colors):
            if index == 0:
                x_pos = random.randint(
                    30, int(game_constants.SCREEN_WIDTH / 3)
                )
            if index == 1:
                x_pos = random.randint(
                    game_constants.SCREEN_WIDTH
                    - int(game_constants.SCREEN_WIDTH / 3),
                    game_constants.SCREEN_WIDTH - 30,
                )
            tank = tank_mod.Tank(
                self.game_screen,
                x_pos,
                self.height_map,
                color=color,
            )
            self.all_sprites_list.add(tank)
            self.tanks.append(tank)
            self.tanks_group.add(tank)
        self.tanks[self.active_tank].active = True

        # TODO(lajoskatona): Fix this for tank list for example...
        self.font = pygame.font.Font('freesansbold.ttf', 12)
        # TODO(lajoskatona): list perhaps?
        self.text1 = self.font.render('Kicsi tank ', True, self.tank_colors[0])
        self.text2 = self.font.render('', True, self.tank_colors[1])
        self.text1_rect = self.text1.get_rect()
        self.text1_rect.topleft = (10, 5)
        self.text2_rect = self.text2.get_rect()
        self.text1_rect.topleft = (
            int(game_constants.SCREEN_WIDTH / 2) + 10,
            5,
        )
        self.cannon_sound = pygame.mixer.Sound(
            'gadgets/sounds/cannon-shot-14799.mp3',
        )
        self.explosion_sound = pygame.mixer.Sound(
            'gadgets/sounds/mixkit-bomb-explosion-in-battle-2800.wav',
        )
        self.final_explosion_sound = pygame.mixer.Sound(
            'gadgets/sounds/mixkit-car-explosion-debris-1562.wav',
        )

    def _draw_terrain(self):
        height = random.randint(1, game_constants.SCREEN_HEIGHT / 2)
        for x_coord in range(
            0, game_constants.SCREEN_WIDTH, game_constants.TERRA_BLOCK_X
        ):
            change_dir = random.randint(1, 12)
            if change_dir < 3:
                height = height - random.randint(4, 10)
            if 3 <= change_dir < 7:
                height = height - random.randint(1, 4)
            if 7 <= change_dir >= 9:
                height = height + random.randint(1, 4)
            if change_dir > 9:
                height = height + random.randint(4, 10)
            for y_coord in range(0, height, game_constants.TERRA_BLOCK_Y):
                self.height_map[x_coord] = (
                    game_constants.SCREEN_HEIGHT - height
                )
                color = self._terrain_color_picker(height, y_coord)
                piece = terrain_mod.PieceOfEarth(
                    x_coord,
                    game_constants.SCREEN_HEIGHT - y_coord,
                    color,
                )
                self.earth_blocks.add(piece)
                self.all_sprites_list.add(piece)

    def _terrain_color_picker(self, max_height, y):
        percent = (y / max_height) * 100
        if percent > 95:
            # Return some greenish
            return (0, random.randint(150, 200), 0)
        # Return some Brown:
        else:
            return game_constants.BROWN_SHADES[
                int(percent / len(game_constants.BROWN_SHADES))
            ]

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    bullet_x = (
                        self.tanks[self.active_tank].rect.x
                        + 2 * self.tanks[self.active_tank].turret_end_x
                    )
                    bullet_y = (
                        self.tanks[self.active_tank].rect.y
                        + self.tanks[self.active_tank].turret_end_y
                    )
                    new_bullet = bullet_mod.Bullet(
                        start_x=bullet_x,
                        start_y=bullet_y,
                        velocity=self.tanks[self.active_tank].power,
                        angle=self.tanks[self.active_tank].angle,
                    )
                    self.tanks[self.active_tank].bullets.append(new_bullet)
                    self.all_sprites_list.add(new_bullet)
                    self.bullets_list.add(new_bullet)
                    self.cannon_sound.play()
                    self._change_active_tank()
            if event.type == pygame.KEYUP:
                self.tanks[self.active_tank].stop_motion()

        return False

    def _change_active_tank(self):
        self.tanks[self.active_tank].active = False
        self.active_tank = 0 if self.active_tank else 1
        self.tanks[self.active_tank].active = True

    def run_logic(self):
        if not self.game_over:
            self.all_sprites_list.update()
            for bullet in self.bullets_list:
                tank_hit_list = pygame.sprite.spritecollide(
                    bullet, self.tanks_group, dokill=False
                )
                for tank_hit in tank_hit_list:
                    self.explosion_sound.play()
                    bullet_blast = blast_mod.Blast(
                        x=bullet.rect.x, y=bullet.rect.y
                    )
                    self.blast_list.add(bullet_blast)
                    self.all_sprites_list.add(bullet_blast)
                    bullet.kill()
                    tank_hit.health -= 20
                    if tank_hit.health <= 0:
                        self.final_explosion_sound.play()
                        tank_blast = blast_mod.Blast(
                            x=tank_hit.x, y=tank_hit.y, radius=30
                        )
                        self.blast_list.add(tank_blast)
                        self.all_sprites_list.add(tank_blast)
                        tank_hit.kill()
                terrain_hits = pygame.sprite.spritecollide(
                    bullet,
                    self.earth_blocks,
                    dokill=True,
                )
                for terrain_hit in terrain_hits:
                    self.explosion_sound.play()
                    hit_x = bullet.rect.x
                    terrain_blast = blast_mod.Blast(
                        x=hit_x,
                        y=bullet.rect.y,
                    )
                    self.blast_list.add(terrain_blast)
                    self.all_sprites_list.add(terrain_blast)
                    self.height_map[
                        self._count_x_earth_pos(hit_x)
                    ] -= game_constants.TERRA_BLOCK_Y
                    for tank in self.tanks:
                        tank.height_map = self.height_map
                    bullet.kill()
                    terrain_hit.kill()
                if (
                    bullet.rect.y < -10
                    or bullet.rect.y > game_constants.SCREEN_HEIGHT + 10
                ):
                    bullet.kill()
                if (
                    bullet.rect.x < -10
                    or bullet.rect.x > game_constants.SCREEN_WIDTH + 10
                ):
                    bullet.kill()
        for blast in self.blast_list:
            terrain_hits = pygame.sprite.spritecollide(
                blast,
                self.earth_blocks,
                dokill=True,
            )
            for t_hit in terrain_hits:
                t_hit.kill()
                # TODO(lajoskatona): kill terrain above the hit...
                # TODO(lajoskatona): change height-map accordingly

    def _count_x_earth_pos(self, x):
        return x - (x % game_constants.TERRA_BLOCK_X)

    def display_frame(self, screen):
        """Display everything to the screen for the game."""
        screen.fill(game_constants.WHITE)

        if self.game_over:
            pass
        else:
            self.all_sprites_list.draw(screen)
            self.text1 = self.font.render(
                'Tank1 %s  %s   %s'
                % (
                    self.tanks[0].power,
                    self.tanks[0].angle,
                    self.tanks[0].health,
                ),
                True,
                self.tank_colors[0],
            )
            self.text2 = self.font.render(
                'Tank2 %s  %s   %s '
                % (
                    self.tanks[1].power,
                    self.tanks[1].angle,
                    self.tanks[1].health,
                ),
                True,
                self.tank_colors[1],
            )
            screen.blit(self.text1, self.text1_rect)
            screen.blit(self.text2, self.text2_rect)

        pygame.display.flip()

    def game_loop(self):
        while not self.done:
            self.done = self.process_events()
            self.run_logic()
            self.display_frame(self.game_screen)
            self.clock.tick(self.base_tck)
        exit()
