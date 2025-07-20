from pygame.time import get_ticks


class Timer:
    def __init__(self, duration, repeat=False, command=None):
        self.duration = duration
        self.bonus_time = 0
        self.start_time = 0
        self.repeat = repeat
        self.is_active = False
        self.command = command

    def set_bonus_time(self, duration):
        self.bonus_time = duration

    def set_command(self, command):
        self.command = command

    def activate(self):
        self.is_active = True
        self.start_time = get_ticks()

    def deactivate(self):
        self.is_active = False
        self.start_time = 0
        if self.repeat:
            self.activate()

    def update(self):
        if self.is_active:
            if get_ticks() - self.start_time >= self.duration + self.bonus_time:
                if self.command:
                    self.command()
                self.deactivate()
