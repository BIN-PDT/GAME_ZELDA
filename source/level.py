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

    def damage_player(self, amount, form):
        if not self.player.timers["vulnerability"].is_active:
            self.player.health -= amount
            self.player.timers["vulnerability"].activate()

    def check_player_attack(self):
        for attack_sprite in self.group_attack.sprites():
            attacked_sprites = pg.sprite.spritecollide(
                attack_sprite, self.group_attackable, False
            )

            for sprite in attacked_sprites:
                if sprite.form == SpriteForm.GRASS:
                    sprite.kill()
                else:
                    sprite.get_damage(self.player.get_attack_damage(attack_sprite.form))

    def run(self):
        self.group_visible.update()
        self.check_player_attack()
        self.group_visible.draws()
        self.ui.display()
