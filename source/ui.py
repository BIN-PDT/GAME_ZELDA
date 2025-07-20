from settings import *
from utils import *
import pygame as pg


class UI:

    def __init__(self):
        self.screen = pg.display.get_surface()
        self.font = pg.font.Font(UI_FONT, UI_FONT_SIZE)
        self.load_assets()
        # BAR SETUP.
        self.hp_rect = pg.Rect(10, 10, HP_BAR_WIDTH, BAR_HEIGHT)
        self.ep_rect = pg.Rect(10, 35, EP_BAR_WIDTH, BAR_HEIGHT)

    def load_assets(self):
        self.weapon_graphic = [load_image(e["image"]) for e in WEAPON_DATA.values()]
        self.magic_graphic = [load_image(e["image"]) for e in MAGIC_DATA.values()]

    def set_player(self, player):
        self.player = player

    def draw_bar(self, current, maximum, bg_rect, color):
        # INFORMATION.
        current_rect = bg_rect.copy()
        current_rect.width = current * bg_rect.width / maximum
        # DRAW.
        pg.draw.rect(self.screen, UI_BG_COLOR, bg_rect, border_radius=5)
        pg.draw.rect(self.screen, color, current_rect, border_radius=5)
        pg.draw.rect(self.screen, UI_BORDER_COLOR, bg_rect, 3, border_radius=5)

    def draw_exp(self):
        # INFORMATION.
        text = str(int(self.player.exp))
        text_surf = self.font.render(text, False, TEXT_COLOR)
        text_rect = text_surf.get_rect(bottomright=(WIDTH - 20, HEIGTH - 20))
        bg_rect = text_rect.inflate(20, 20)
        # DRAW.
        pg.draw.rect(self.screen, UI_BG_COLOR, bg_rect, border_radius=5)
        self.screen.blit(text_surf, text_rect)
        pg.draw.rect(self.screen, UI_BORDER_COLOR, bg_rect, 3, border_radius=5)

    def draw_option_box(self, place, can_switch):
        # INFORMATION.
        bg_rect = pg.Rect(place, (ITEM_BOX_SIZE, ITEM_BOX_SIZE))
        boder_color = UI_BORDER_COLOR if can_switch else UI_BORDER_COLOR_ACTIVE
        # DRAW.
        pg.draw.rect(self.screen, UI_BG_COLOR, bg_rect, border_radius=5)
        pg.draw.rect(self.screen, boder_color, bg_rect, 3, border_radius=5)
        return bg_rect

    def preview_attack(self, graphic, place, index, can_switch):
        # INFORMATION.
        bg_rect = self.draw_option_box(place, can_switch)
        attack_surf = graphic[index]
        attack_rect = attack_surf.get_rect(center=bg_rect.center)
        # DRAW.
        self.screen.blit(attack_surf, attack_rect)

    def display(self):
        self.draw_bar(
            self.player.health, self.player.stats["HP"], self.hp_rect, HP_COLOR
        )
        self.draw_bar(
            self.player.energy, self.player.stats["EP"], self.ep_rect, EP_COLOR
        )
        self.draw_exp()
        self.preview_attack(
            self.weapon_graphic,
            WEAPON_PREVIEW_PLACE,
            self.player.weapon_index,
            self.player.can_switch_weapon,
        )
        self.preview_attack(
            self.magic_graphic,
            MAGIC_PREVIEW_PLACE,
            self.player.magic_index,
            self.player.can_switch_magic,
        )
