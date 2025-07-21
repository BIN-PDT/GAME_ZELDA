from settings import *
from utils import *
from random import choice
import pygame as pg
from ui import UI
from camera import CameraGroup
from sprites import Tile
from player import Player
from enemy import Enemy
from weapon import Weapon
from particle import ParticleController
from magic import MagicController


class Level:

    def __init__(self):
        self.screen = pg.display.get_surface()
        # GROUP.
        self.group_visible = CameraGroup()
        self.group_obstacle = pg.sprite.Group()
        self.group_attack = pg.sprite.Group()
        self.group_attackable = pg.sprite.Group()
        # SETUP.
        self.ui = UI()
        self.particle_controller = ParticleController()
        self.magic_controller = MagicController(self.particle_controller)
        self.load_map()

    def load_map(self):
        layouts = {key: load_layout(path) for key, path in LAYOUT_PATHS.items()}
        graphic = {key: load_image_list(path) for key, path in GRAPHIC_PATHS.items()}

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col == "-1":
                        continue

                    place = col_index * TILE_SIZE, row_index * TILE_SIZE
                    match style:
                        case "Grass":
                            Tile(
                                groups=(
                                    self.group_visible,
                                    self.group_obstacle,
                                    self.group_attackable,
                                ),
                                place=place,
                                form=SpriteForm.GRASS,
                                image=choice(graphic[style]),
                            )
                        case "Object":
                            Tile(
                                groups=(self.group_visible, self.group_obstacle),
                                place=place,
                                form=SpriteForm.OBJECT,
                                image=graphic[style][int(col)],
                            )
                        case "Entity":
                            if col != "394":
                                Enemy(
                                    groups=(self.group_visible, self.group_attackable),
                                    name=MONSTER_ID[int(col)],
                                    place=place,
                                    group_obstacle=self.group_obstacle,
                                    damage_player=self.damage_player,
                                    create_death_effect=self.create_death_effect,
                                )
                            else:
                                self.player = Player(
                                    groups=self.group_visible,
                                    place=place,
                                    group_obstacle=self.group_obstacle,
                                    create_weapon=self.create_weapon,
                                    create_magic=self.create_magic,
                                )
                                self.group_visible.set_player(self.player)
                                self.ui.set_player(self.player)
                        case "Boundary":
                            Tile(
                                groups=self.group_obstacle,
                                place=place,
                                form=SpriteForm.INVISIBLE,
                            )

    def create_weapon(self):
        return Weapon((self.group_visible, self.group_attack), self.player)

    def create_magic(self):
        style = self.player.magic
        strength = MAGIC_DATA[style]["strength"]
        cost = MAGIC_DATA[style]["cost"]

        if style == "heal":
            self.magic_controller.cast_heal(
                self.player, cost, strength, self.group_visible
            )
        else:
            self.magic_controller.cast_fire(
                self.player, cost, (self.group_visible, self.group_attack)
            )

    def damage_player(self, amount, form):
        if not self.player.timers["vulnerability"].is_active:
            self.player.health -= amount
            self.player.timers["vulnerability"].activate()
            self.particle_controller.create_particles(
                form, self.player.rect.center, self.group_visible
            )

    def check_player_attack(self):
        for attack_sprite in self.group_attack.sprites():
            attacked_sprites = pg.sprite.spritecollide(
                attack_sprite, self.group_attackable, False
            )

            for sprite in attacked_sprites:
                if sprite.form == SpriteForm.GRASS:
                    sprite.kill()
                    self.particle_controller.create_grass_particles(
                        sprite.rect.center, self.group_visible
                    )
                else:
                    sprite.get_damage(self.player.get_attack_damage(attack_sprite.form))

    def create_death_effect(self, place, form):
        self.particle_controller.create_particles(place, form, self.group_visible)

    def run(self):
        self.group_visible.update()
        self.check_player_attack()
        self.group_visible.draws()
        self.ui.display()
