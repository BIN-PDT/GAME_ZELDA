from settings import *
from utils import *
import pygame as pg
from timers import Timer
from sprites import Entity


class Enemy(Entity):

    def __init__(
        self,
        groups,
        name,
        place,
        group_obstacle,
        damage_player,
        create_death_effect,
        increase_experience,
    ):
        super().__init__(groups, group_obstacle)
        # INTERACTION.
        self.damage_player = damage_player
        self.create_death_effect = create_death_effect
        self.increase_experience = increase_experience
        # ANIMATION.
        self.load_assets(name)
        self.status = EnemyStatus.IDLE
        self.frame_index = 0
        # CORE.
        self.form = SpriteForm.ENEMY
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=place)
        self.hitbox = self.rect.inflate(0, -10)
        # STATS.
        stats = MONSTER_DATA[name]
        self.name = name
        self.health = stats["HP"]
        self.attack = stats["ATK"]
        self.speed = stats["SPD"]
        self.exp = stats["EXP"]
        self.resistance = stats["RES"]
        self.notice_radius = stats["NTC_RAD"]
        self.attack_radius = stats["ATK_RAD"]
        self.attack_type = stats["ATK_TYPE"]
        # TIMERS.
        self.timers = {"attack": Timer(750), "vulnerability": Timer(300)}

    def load_assets(self, name):
        self.animations = load_image_dict(f"images/monsters/{name}")

    def cooldown(self):
        for timer in self.timers.values():
            timer.update()

    def get_target(self, player):
        # INFORMATION.
        src_place = pg.math.Vector2(self.rect.center)
        des_place = pg.math.Vector2(player.rect.center)
        # PROCESS.
        direction = des_place - src_place
        distance = direction.magnitude()
        if distance > 0:
            direction = direction.normalize()
        return distance, direction

    def get_status(self, player):
        # INFORMATION.
        distance = self.get_target(player)[0]
        is_attacking = self.timers["attack"].is_active
        # PROCESS.
        if distance <= self.attack_radius and not is_attacking:
            if self.status != EnemyStatus.ATTACK:
                self.frame_index = 0
            self.status = EnemyStatus.ATTACK
        elif distance <= self.notice_radius:
            self.status = EnemyStatus.MOVE
        else:
            self.status = EnemyStatus.IDLE

    def get_action(self, player):
        match self.status:
            case EnemyStatus.ATTACK:
                self.damage_player(self.attack, self.attack_type)
            case EnemyStatus.MOVE:
                self.direction.update(self.get_target(player)[1])
            case EnemyStatus.IDLE:
                self.direction.update()

    def update_action(self, player):
        self.get_status(player)
        self.get_action(player)

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += ANIMATION_SPEED
        if self.frame_index >= len(animation):
            self.frame_index = 0
            # COOLDOWN ATTACK.
            if not self.timers["attack"].is_active:
                self.timers["attack"].activate()

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def check_resistance(self):
        if self.timers["vulnerability"].is_active:
            self.direction *= -self.resistance

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.create_death_effect(self.name, self.rect.center)
            self.increase_experience(self.exp)

    def get_damaged(self, amount):
        if not self.timers["vulnerability"].is_active:
            self.health -= amount
            self.check_death()
            self.timers["vulnerability"].activate()

    def update(self):
        self.cooldown()
        self.check_resistance()
        self.move()
        self.animate()
        self.flicker()
