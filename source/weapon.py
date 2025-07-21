from settings import *
from utils import *
import pygame as pg


class Weapon(pg.sprite.Sprite):

    def __init__(self, groups, player):
        super().__init__(groups)
        # CORE.
        self.form = SpriteForm.WEAPON
        direction = player.status.split("_")[0]
        self.image = load_image(f"images/weapons/{player.weapon}/{direction}.png")
        match direction:
            case Direction.LEFT:
                self.rect = self.image.get_rect(
                    midright=player.rect.midleft + pg.math.Vector2(0, 16)
                )
            case Direction.RIGHT:
                self.rect = self.image.get_rect(
                    midleft=player.rect.midright + pg.math.Vector2(0, 16)
                )
            case Direction.UP:
                self.rect = self.image.get_rect(
                    midbottom=player.rect.midtop + pg.math.Vector2(-10, 0)
                )
            case Direction.DOWN:
                self.rect = self.image.get_rect(
                    midtop=player.rect.midbottom + pg.math.Vector2(-10, 0)
                )
