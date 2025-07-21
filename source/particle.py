from settings import *
from utils import *
from random import choice, randint
import pygame as pg


class Particle(pg.sprite.Sprite):

    def __init__(self, groups, place, images):
        super().__init__(groups)
        # ANIMATION.
        self.animations = images
        self.frame_index = 0
        # CORE.
        self.form = SpriteForm.PARTICLE
        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(center=place)

    def animate(self):
        self.frame_index += ANIMATION_SPEED

        if self.frame_index < len(self.animations):
            self.image = self.animations[int(self.frame_index)]
        else:
            self.kill()

    def update(self):
        self.animate()


class ParticleController:

    def __init__(self):
        self.load_assets()

    def load_assets(self):
        self.animations = load_image_dict("images/particles")
        self.animations["grass"] = list(
            load_image_dict("images/particles/grass").values()
        )

    def create_particles(self, name, place, groups):
        animation = self.animations[name.lower()]
        Particle(groups, place, animation)

    def create_grass_particles(self, place, groups):
        for _ in range(randint(3, 6)):
            offset_place = place - pg.math.Vector2(0, randint(70, 80))
            animation = choice(self.animations["grass"])
            Particle(groups, offset_place, animation)
