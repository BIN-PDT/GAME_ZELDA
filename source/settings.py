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
