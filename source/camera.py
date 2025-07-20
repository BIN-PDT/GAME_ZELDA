from settings import *
from utils import *
import pygame as pg


class CameraGroup(pg.sprite.Group):

    def __init__(self):
        super().__init__()
        # CORE.
        self.screen = pg.display.get_surface()
        self.offset = pg.math.Vector2()
        self.player = None
        self.load_assets()
        # DERIVED.
        self.HALF_SIZE = pg.math.Vector2(self.screen.size) // 2

    def load_assets(self):
        self.background = load_image("images/tilemap/ground.png", False)

    def set_player(self, player):
        self.player = player

    def draws(self):
        self.offset = self.player.rect.center - self.HALF_SIZE

        self.screen.blit(self.background, -self.offset)
        for sprite in sorted(self.sprites(), key=lambda e: e.rect.centery):
            offset_place = sprite.rect.topleft - self.offset
            self.screen.blit(sprite.image, offset_place)

    def update_enemies(self):
        for sprite in filter(lambda e: e.form == SpriteForm.ENEMY, self.sprites()):
            sprite.update_action(self.player)

    def update(self):
        super().update()
        self.update_enemies()
