from settings import *
from utils import *
import pygame as pg
from timers import Timer
from sprites import Entity


class Player(Entity):

    def __init__(self, groups, place, group_obstacle, create_weapon, create_magic):
        super().__init__(groups, group_obstacle)
        # INTERACTION.
        self.create_weapon = create_weapon
        self.create_magic = create_magic
        # ANIMATION.
        self.load_assets()
        self.status = Direction.DOWN
        self.frame_index = 0
        # CORE.
        self.form = SpriteForm.PLAYER
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=place)
        self.hitbox = self.rect.inflate(0, -26)
        # STATS.
        self.stats = {"HP": 100, "EP": 100, "ATK": 10, "MAG": 4, "SPD": 5}
        self.costs = {"HP": 100, "EP": 100, "ATK": 100, "MAG": 100, "SPD": 100}
        self.health = self.stats["HP"]
        self.energy = self.stats["EP"]
        self.speed = self.stats["SPD"]
        self.exp = 0
        # WEAPON.
        self.weapon_index = 0
        self.weapon = WEAPON_TYPES[self.weapon_index]
        # MAGIC.
        self.magic_index = 0
        self.magic = MAGIC_TYPES[self.magic_index]
        # TIMERS.
        self.timers = {
            "attack": Timer(400),
            "switch_weapon": Timer(200),
            "switch_magic": Timer(200),
            "vulnerability": Timer(500),
        }

    def set_exp(self, value):
        self.exp = max(0, self.exp + value)

    def set_health(self, value):
        self.health = max(0, min(self.stats["HP"], self.health + value))

    def set_energy(self, value):
        self.energy = max(0, min(self.stats["EP"], self.energy + value))

    def get_attack_damage(self, form):
        return (
            self.stats["ATK"] + WEAPON_DATA[self.weapon]["damage"]
            if form == SpriteForm.WEAPON
            else self.stats["MAG"] + MAGIC_DATA[self.magic]["strength"]
        )

    def get_stat_by_index(self, index):
        return tuple(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return tuple(self.costs.values())[index]

    def upgrade_stat(self, name):
        self.stats[name] = min(MAX_STATS[name], self.stats[name] * 1.2)
        self.costs[name] *= 1.4
        self.speed = self.stats["SPD"]

    def load_assets(self):
        self.animations = load_image_dict(f"images/player")

    def cooldown(self):
        for timer in self.timers.values():
            timer.update()

    def recovery(self):
        if self.energy < self.stats["EP"]:
            self.set_energy(ENERGY_RECOVERY * self.stats["MAG"])

    def switch_weapon(self):
        self.weapon_index += 1
        if self.weapon_index > len(WEAPON_TYPES) - 1:
            self.weapon_index = 0
        self.weapon = WEAPON_TYPES[self.weapon_index]

    def switch_magic(self):
        self.magic_index += 1
        if self.magic_index > len(MAGIC_TYPES) - 1:
            self.magic_index = 0
        self.magic = MAGIC_TYPES[self.magic_index]

    def input_movement(self, keys):
        if keys[pg.K_LEFT]:
            self.direction.x = -1
            self.status = Direction.LEFT
        elif keys[pg.K_RIGHT]:
            self.direction.x = 1
            self.status = Direction.RIGHT
        else:
            self.direction.x = 0

        if keys[pg.K_UP]:
            self.direction.y = -1
            self.status = Direction.UP
        elif keys[pg.K_DOWN]:
            self.direction.y = 1
            self.status = Direction.DOWN
        else:
            self.direction.y = 0

    def input_attack(self, keys):
        if keys[pg.K_SPACE]:
            weapon = self.create_weapon()
            timer = self.timers["attack"]
            timer.set_bonus_time(WEAPON_DATA[self.weapon]["cooldown"])
            timer.set_command(weapon.kill)
            timer.activate()

        if keys[pg.K_LCTRL]:
            self.create_magic()
            timer = self.timers["attack"]
            timer.set_bonus_time(0)
            timer.set_command(None)
            timer.activate()

    def input_switch(self, keys):
        if keys[pg.K_q] and not self.timers["switch_weapon"].is_active:
            self.switch_weapon()
            self.timers["switch_weapon"].activate()

        if keys[pg.K_e] and not self.timers["switch_magic"].is_active:
            self.switch_magic()
            self.timers["switch_magic"].activate()

    def input(self):
        # INFORMATION.
        keys = pg.key.get_pressed()
        # PROCESS.
        if not self.timers["attack"].is_active:
            self.input_movement(keys)
            self.input_attack(keys)
        self.input_switch(keys)

    def get_status(self):
        # IDLE.
        if self.direction == (0, 0):
            self.status = self.status.split("_")[0] + "_idle"
        # ATTACK.
        if self.timers["attack"].is_active:
            self.direction.update()
            self.status = self.status.split("_")[0] + "_attack"

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += ANIMATION_SPEED
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.cooldown()
        self.recovery()
        self.input()
        self.move()
        self.get_status()
        self.animate()
        self.flicker()
