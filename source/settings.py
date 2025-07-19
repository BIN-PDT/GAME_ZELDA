from enum import StrEnum


# PLAYER DIRECTION.
class Direction(StrEnum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


# SPRITE FORM.
class SpriteForm(StrEnum):
    INVISIBLE = "Invisible"
    GRASS = "Grass"
    OBJECT = "Object"
    PLAYER = "Player"
    WEAPON = "Weapon"
    MAGIC = "Magic"
    ENEMY = "Enemy"


# DIMENSION.
WIDTH, HEIGTH = 1280, 720
TILE_SIZE = 64
ANIMATION_SPEED = 0.15
# MAP DATA.
LAYOUT_PATHS = {
    "Grass": "map/Grass.csv",
    "Object": "map/Objects.csv",
    "Entity": "map/Entities.csv",
    "Boundary": "map/FloorBlocks.csv",
}
GRAPHIC_PATHS = {
    "Grass": "images/grass",
    "Object": "images/objects",
}
# WEAPON DATA.
WEAPON_DATA = {
    "axe": {"cooldown": 300, "damage": 20, "image": "images/weapons/axe/full.png"},
    "sai": {"cooldown": 100, "damage": 10, "image": "images/weapons/sai/full.png"},
    "sword": {"cooldown": 150, "damage": 15, "image": "images/weapons/sword/full.png"},
    "lance": {"cooldown": 400, "damage": 30, "image": "images/weapons/lance/full.png"},
    "rapier": {"cooldown": 50, "damage": 5, "image": "images/weapons/rapier/full.png"},
}
WEAPON_TYPES = tuple(WEAPON_DATA.keys())
