from settings import *
from random import randint
import pygame as pg


class MagicController:

    def __init__(self, particle_controller):
        self.particle_controller = particle_controller

    def cast_heal(self, player, cost, strength, groups):
        if player.energy >= cost:
            player.set_energy(-cost)
            player.set_health(strength)
            # PARTICLE.
            place = player.rect.center
            self.particle_controller.create_particles("aura", place, groups)
            self.particle_controller.create_particles("heal", place, groups)

    def cast_fire(self, player, cost, groups):
        if player.energy >= cost:
            player.set_energy(-cost)
            # PARTICLE.
            match player.status.split("_")[0]:
                case Direction.LEFT:
                    direction = pg.math.Vector2(-1, 0)
                case Direction.RIGHT:
                    direction = pg.math.Vector2(1, 0)
                case Direction.UP:
                    direction = pg.math.Vector2(0, -1)
                case Direction.DOWN:
                    direction = pg.math.Vector2(0, 1)

            for index in range(1, 6):
                place = player.rect.center + direction * (index * TILE_SIZE)
                place += (
                    randint(-TILE_SIZE // 3, TILE_SIZE // 3),
                    randint(-TILE_SIZE // 3, TILE_SIZE // 3),
                )
                self.particle_controller.create_particles("flame", place, groups)
