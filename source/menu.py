from settings import *
import pygame as pg
from timers import Timer


class Item:

    def __init__(self, font, place, size, index):
        self.font = font
        # CORE.
        self.rect = pg.Rect(place, size)
        self.index = index

    def upgrade(self, player):
        # INFORMATION.
        item_name = tuple(player.stats.keys())[self.index]
        item_cost = player.costs[item_name]
        # PROCESS.
        if player.exp >= item_cost and player.stats[item_name] < MAX_STATS[item_name]:
            player.set_exp(-item_cost)
            player.upgrade_stat(item_name)

    def draw_title(self, screen, name, cost, is_selected):
        # INFORMATION.
        color = TEXT_COLOR_ACTIVE if is_selected else TEXT_COLOR
        offset = pg.math.Vector2(0, 20)

        name_surf = self.font.render(name, False, color)
        name_rect = name_surf.get_rect(midtop=self.rect.midtop + offset)
        cost_surf = self.font.render(str(int(cost)), False, color)
        cost_rect = cost_surf.get_rect(midbottom=self.rect.midbottom - offset)
        # PROCESS
        screen.blit(name_surf, name_rect)
        screen.blit(cost_surf, cost_rect)

    def draw_value(self, screen, value, max_value, is_selected):
        # INFORMATION.
        color = TEXT_COLOR_ACTIVE if is_selected else TEXT_COLOR
        offset = pg.math.Vector2(0, 60)
        top_place = self.rect.midtop + offset
        bot_place = self.rect.midbottom - offset

        rel_place = value * (bot_place.y - top_place.y) / max_value
        mark = pg.Rect(top_place.x - 15, bot_place.y - rel_place - 5, 30, 10)
        # PROCESS.
        pg.draw.line(screen, color, top_place, bot_place, 5)
        pg.draw.rect(screen, color, mark, border_radius=2)

    def display(self, screen, selected_index, name, value, max_value, cost):
        # INFORMATION.
        is_selected = self.index == selected_index
        bg_color = MENU_BG_COLOR_ACTIVE if is_selected else MENU_BG_COLOR
        # PROCESS
        pg.draw.rect(screen, bg_color, self.rect, border_radius=5)
        pg.draw.rect(screen, BORDER_COLOR, self.rect, 3, border_radius=5)
        self.draw_title(screen, name, cost, is_selected)
        self.draw_value(screen, value, max_value, is_selected)


class Menu:

    def __init__(self, player):
        self.screen = pg.display.get_surface()
        self.font = pg.font.Font(UI_FONT, UI_FONT_SIZE)
        # CORE.
        self.player = player
        self.item_names = tuple(player.stats.keys())
        self.item_costs = tuple(player.costs.values())
        self.max_values = tuple(MAX_STATS.values())
        # SELECTION.
        self.selection_index = 0
        self.selection_timer = Timer(300)
        # SETUP.
        self.load_items()

    def set_selection_index(self, value):
        self.selection_index = max(0, min(len(self.item_names) - 1, value))

    def load_items(self):
        # INFORMATION.
        item_quantity = len(self.item_names)
        size = WIDTH // (item_quantity + 1), HEIGTH * 0.8
        padding = (WIDTH - size[0] * item_quantity) // (item_quantity + 1)
        # PROCESS.
        self.items = []
        for index in range(item_quantity):
            place = padding + index * (size[0] + padding), HEIGTH * 0.1
            self.items.append(Item(self.font, place, size, index))

    def cooldown(self):
        self.selection_timer.update()

    def input(self):
        keys = pg.key.get_pressed()

        if not self.selection_timer.is_active:
            if keys[pg.K_LEFT]:
                self.set_selection_index(self.selection_index - 1)
                self.selection_timer.activate()
            elif keys[pg.K_RIGHT]:
                self.set_selection_index(self.selection_index + 1)
                self.selection_timer.activate()

            if keys[pg.K_SPACE]:
                self.items[self.selection_index].upgrade(self.player)
                self.selection_timer.activate()

    def update(self):
        self.cooldown()
        self.input()

    def display(self):
        for index, item in enumerate(self.items):
            item.display(
                screen=self.screen,
                selected_index=self.selection_index,
                name=self.item_names[index],
                value=self.player.get_stat_by_index(index),
                max_value=self.max_values[index],
                cost=self.player.get_cost_by_index(index),
            )
