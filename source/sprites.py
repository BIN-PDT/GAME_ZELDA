from settings import *
import pygame as pg


class Tile(pg.sprite.Sprite):
    surface = pg.Surface((TILE_SIZE, TILE_SIZE))

    def __init__(self, groups, place, form, image=None):
        super().__init__(groups)

        self.form = form
        self.image = image or Tile.surface
        self.rect = self.image.get_rect(topleft=place)
        if self.form == SpriteForm.OBJECT:
            self.rect.y -= TILE_SIZE
        self.hitbox = self.rect.inflate(0, -10)


class Entity(pg.sprite.Sprite):

    def __init__(self, groups):
        super().__init__(groups)

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
