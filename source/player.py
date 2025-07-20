from settings import *
from utils import *
import pygame as pg
from timers import Timer
from sprites import Entity


class Player(Entity):

    def __init__(
        self, groups, place, group_obstacle, create_weapon, cancel_weapon, create_magic
    ):
        super().__init__(groups)

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
        self.health = self.stats["HP"]
        self.energy = self.stats["EP"]
        self.speed = self.stats["SPD"]
        self.exp = 0
        # MOVEMENT.
        self.direction = pg.math.Vector2()
        # COLLISION.
        self.group_obstacle = group_obstacle
        # ATTACK.
        self.is_attacking = False
        self.attack_cooldown = 400
        # WEAPON.
        self.create_weapon = create_weapon
        self.cancel_weapon = cancel_weapon
        self.weapon_index = 0
        self.weapon = WEAPON_TYPES[self.weapon_index]
        self.can_switch_weapon = True
        # MAGIC.
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = MAGIC_TYPES[self.magic_index]
        self.can_switch_magic = True
        # TIMERS.
        self.timers = {
            "attack": Timer(None, command=self.refresh_attack),
            "switch_weapon": Timer(200, command=self.refresh_switch_weapon),
            "switch_magic": Timer(200, command=self.refresh_switch_magic),
        }

    def load_assets(self):
        self.animations = load_image_dict(f"images/player")

    def refresh_attack(self):
        self.is_attacking = False
        self.cancel_weapon()

    def refresh_switch_weapon(self):
        self.can_switch_weapon = True

    def refresh_switch_magic(self):
        self.can_switch_magic = True

    def cooldown(self):
        for timer in self.timers.values():
            timer.update()

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

    def input(self):
        keys = pg.key.get_pressed()

        if not self.is_attacking:
            # MOVEMENT.
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
            # ATTACK.
            if keys[pg.K_SPACE]:
                self.is_attacking = True
                timer = self.timers["attack"]
                weapon_cooldown = WEAPON_DATA[self.weapon]["cooldown"]
                timer.set_duration(self.attack_cooldown + weapon_cooldown)
                timer.activate()
                self.create_weapon()

            if keys[pg.K_LCTRL]:
                self.is_attacking = True
                timer = self.timers["attack"]
                timer.set_duration(self.attack_cooldown)
                timer.activate()
                self.create_magic()
        # SWITCH.
        if keys[pg.K_q] and self.can_switch_weapon:
            self.can_switch_weapon = False
            self.timers["switch_weapon"].activate()
            self.switch_weapon()

        if keys[pg.K_e] and self.can_switch_magic:
            self.can_switch_magic = False
            self.timers["switch_magic"].activate()
            self.switch_magic()

    def get_status(self):
        # IDLE.
        if self.direction == (0, 0):
            self.status = self.status.split("_")[0] + "_idle"
        # ATTACK.
        if self.is_attacking:
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
        self.input()
        self.get_status()
        self.animate()
        self.move()
