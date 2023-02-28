import pygame

from scorched_earth import game_constants


class PieceOfEarth(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, color):
        super().__init__()
        self.image = pygame.Surface(
            [
                game_constants.TERRA_BLOCK_X,
                game_constants.TERRA_BLOCK_Y,
            ],
        )
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

    def update(self):
        pass
