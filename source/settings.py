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
    ENEMY = "Enemy"
    PARTICLE = "Particle"


# ENEMY STATUS.
class EnemyStatus(StrEnum):
    IDLE = "idle"
    MOVE = "move"
    ATTACK = "attack"


# DIMENSION.
WIDTH, HEIGTH = 1280, 720
TILE_SIZE = 64
ANIMATION_SPEED = 0.15
ENERGY_RECOVERY = 0.005
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
# COLORS.
WATER_COLOR = "#71DDEE"
TEXT_COLOR = "#EEEEEE"
TEXT_COLOR_ACTIVE = "#111111"
BORDER_COLOR = "#111111"
BORDER_COLOR_ACTIVE = "GOLD"
# UI.
UI_FONT = "font/joystix.ttf"
UI_FONT_SIZE = 18
BAR_HEIGHT = 20
HP_BAR_WIDTH = 200
EP_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
HP_COLOR = "RED"
EP_COLOR = "BLUE"
UI_BG_COLOR = "#222222"
# MENU.
MENU_BG_COLOR = "#222222"
MENU_BG_COLOR_ACTIVE = "#EEEEEE"
MENU_BAR_COLOR = "#EEEEEE"
MENU_BAR_COLOR_ACTIVE = "#111111"
# WEAPON DATA.
WEAPON_PREVIEW_PLACE = 10, 620
WEAPON_DATA = {
    "axe": {"cooldown": 300, "damage": 20, "image": "images/weapons/axe/full.png"},
    "sai": {"cooldown": 100, "damage": 10, "image": "images/weapons/sai/full.png"},
    "sword": {"cooldown": 150, "damage": 15, "image": "images/weapons/sword/full.png"},
    "lance": {"cooldown": 400, "damage": 30, "image": "images/weapons/lance/full.png"},
    "rapier": {"cooldown": 50, "damage": 5, "image": "images/weapons/rapier/full.png"},
}
WEAPON_TYPES = tuple(WEAPON_DATA.keys())
# MAGIC DATA.
MAGIC_PREVIEW_PLACE = 80, 630
MAGIC_DATA = {
    "flame": {"strength": 5, "cost": 20, "image": "images/magics/flame/full.png"},
    "heal": {"strength": 20, "cost": 10, "image": "images/magics/heal/full.png"},
}
MAGIC_TYPES = tuple(MAGIC_DATA.keys())
# PLAYER DATA.
MAX_STATS = {"HP": 300, "EP": 140, "ATK": 20, "MAG": 10, "SPD": 10}
# ENEMY DATA.
MONSTER_ID = {390: "bamboo", 391: "spirit", 392: "raccoon", 393: "squid"}
MONSTER_DATA = {
    "squid": {
        "HP": 100,
        "ATK": 20,
        "SPD": 3,
        "EXP": 100,
        "RES": 3,
        "NTC_RAD": 360,
        "ATK_RAD": 80,
        "ATK_TYPE": "slash",
        "ATK_SOUND": "audio/attack/slash.wav",
    },
    "raccoon": {
        "HP": 300,
        "ATK": 40,
        "SPD": 2,
        "EXP": 250,
        "RES": 3,
        "NTC_RAD": 400,
        "ATK_RAD": 120,
        "ATK_TYPE": "claw",
        "ATK_SOUND": "audio/attack/claw.wav",
    },
    "spirit": {
        "HP": 100,
        "ATK": 8,
        "SPD": 4,
        "EXP": 110,
        "RES": 3,
        "NTC_RAD": 350,
        "ATK_RAD": 60,
        "ATK_TYPE": "thunder",
        "ATK_SOUND": "audio/attack/fireball.wav",
    },
    "bamboo": {
        "HP": 70,
        "ATK": 6,
        "SPD": 3,
        "EXP": 120,
        "RES": 3,
        "NTC_RAD": 300,
        "ATK_RAD": 50,
        "ATK_TYPE": "leaf",
        "ATK_SOUND": "audio/attack/slash.wav",
    },
}
