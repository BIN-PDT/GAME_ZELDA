from settings import *
from utils import *
from random import choice
import pygame as pg
from ui import UI
from camera import CameraGroup
from sprites import Tile
from player import Player
from weapon import Weapon


class Level:

    def __init__(self):
        self.screen = pg.display.get_surface()
        # GROUP.
        self.group_visible = CameraGroup()
        self.group_obstacle = pg.sprite.Group()
        # ATTACK.
        self.current_weapon = None
        # USER INTERFACE.
        self.ui = UI()
        # SETUP.
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
                                groups=(self.group_visible, self.group_obstacle),
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
                            if col == "394":
                                self.player = Player(
                                    groups=self.group_visible,
                                    place=place,
                                    group_obstacle=self.group_obstacle,
                                    create_weapon=self.create_weapon,
                                    cancel_weapon=self.cancel_weapon,
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
        self.current_weapon = Weapon(self.group_visible, self.player)

    def cancel_weapon(self):
        if self.current_weapon:
            self.current_weapon.kill()
            self.current_weapon = None

    def create_magic(self):
        style = self.player.magic
        strength = MAGIC_DATA[style]["strength"]
        cost = MAGIC_DATA[style]["cost"]

    def run(self):
        self.group_visible.update()
        self.group_visible.draws()
        self.ui.display()
