from settings import *
from math import sin
import pygame as pg


class Tile(pg.sprite.Sprite):
    surface = pg.Surface((TILE_SIZE, TILE_SIZE))

    def __init__(self, groups, place, form, image=None):
        super().__init__(groups)
        # CORE.
        self.form = form
        self.image = image or Tile.surface
        self.rect = self.image.get_rect(topleft=place)
        if self.form == SpriteForm.OBJECT:
            self.rect.y -= TILE_SIZE
        self.hitbox = self.rect.inflate(0, -10)


class Entity(pg.sprite.Sprite):

    def __init__(self, groups, group_obstacle):
        super().__init__(groups)
        # MOVEMENT.
        self.direction = pg.math.Vector2()
        # COLLISION.
        self.group_obstacle = group_obstacle

    def collide(self, direction):
        if direction == "H":
            for sprite in self.group_obstacle.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    else:
                        self.hitbox.right = sprite.hitbox.left
        else:
            for sprite in self.group_obstacle.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    else:
                        self.hitbox.bottom = sprite.hitbox.top

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * self.speed
        self.collide("H")
        self.hitbox.y += self.direction.y * self.speed
        self.collide("V")

        self.rect.center = self.hitbox.center

    def flicker(self):
        self.image.set_alpha(
            255
            * (
                sin(pg.time.get_ticks()) > 0
                if self.timers["vulnerability"].is_active
                else 1
            )
        )
