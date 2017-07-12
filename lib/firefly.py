# File which includes the base class for fireflies

from random import randint

black = (0, 0, 0)
white = (255, 255, 255)


class Firefly:
    def __init__(self, x, y, period):
        self.x = x
        self.y = y
        self.period = period
        self.clock = randint(1, self.period)
        self.last_nudged_at = 0
        self.neighbors = []

    def nudge_clock(self, nudge):
        if self.clock >= (self.period / 2):
            self.clock += nudge
        else:
            self.clock -= nudge

    def set_last_nudged_at(self, sim_time):
        self.last_nudged_at = sim_time

    # Private method to light up the firefly (the display needs to be updated after this is called)
    def light_up(self, game_display):
        for x in range(self.x - 3, self.x + 3):
            for y in range(self.y - 3, self.y + 3):
                game_display.set_at((abs(x), abs(y)), white)

    # Private method to turn off the firefly (the display needs to be updated after this is called)
    def light_off(self, game_display):
        for x in range(self.x - 3, self.x + 3):
            for y in range(self.y - 3, self.y + 3):
                game_display.set_at((abs(x), abs(y)), black)
