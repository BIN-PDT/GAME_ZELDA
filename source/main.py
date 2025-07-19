from settings import *
import sys, pygame as pg
from level import Level


class Game:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGTH))
        pg.display.set_caption("Zelda")
        self.clock = pg.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            self.handle_event()
            self.handle_logic()

    def handle_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def handle_logic(self):
        self.screen.fill("BLACK")
        self.level.run()
        pg.display.update()
        self.clock.tick(60)


if __name__ == "__main__":
    Game().run()
