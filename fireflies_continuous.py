import pygame
from random import sample, randint
from math import sqrt
from time import sleep, strftime
from numpy import mean, std

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


class FirefliesSimulation:
    def __init__(self, number_of_fireflies, period=50, nudge=15, neighbor_distance=50, until=10000000):
        # Save the parameters of the simulation
        self.canvas_length = 800                # Default is 800
        self.canvas_width = 800                 # Default is 800
        self.time = 0
        self.until = until
        self.n = number_of_fireflies
        self.fireflies = []

        self.neighbor_distance = neighbor_distance
        self.nudge_duration = nudge

        # Sample the positions of the fireflies
        xs = sample(range(self.canvas_length), self.n)
        ys = sample(range(self.canvas_width), self.n)

        # Create the firefly objects and store them
        for n in range(self.n):
            self.fireflies.append(Firefly(x=xs[n], y=ys[n], period=period))

        # Populate their neighbors
        for firefly1 in self.fireflies:
            for firefly2 in self.fireflies:
                x1 = firefly1.x
                y1 = firefly1.y
                x2 = firefly2.x
                y2 = firefly2.y
                if firefly1 != firefly2 and sqrt((x2 - x1)**2 + (y2 - y1)**2) < self.neighbor_distance:
                    firefly1.neighbors.append(firefly2)

        # Initialize pygame library
        pygame.init()
        self.space = pygame.display.set_mode((self.canvas_length, self.canvas_width))
        pygame.display.set_caption('Fireflies')
        self.space.fill(black)        # Set the background color as black

    # Private method to update firefly clocks
    def __update_firefly_clocks(self):
        flash_counter = 0
        for firefly in self.fireflies:
            # Increment the clock
            firefly.clock += 1

            # If the firefly's clock reached period, it's time to shine
            if firefly.clock > firefly.period:
                flash_counter += 1

                # Spread the light (will be turned off outside this function)
                firefly.light_up(self.space)

                # Nudge every neighbor that is not nudged at this time step
                for neighbor in firefly.neighbors:
                    if neighbor.last_nudged_at != self.time:
                        neighbor.nudge_clock(self.nudge_duration)
                        neighbor.set_last_nudged_at(self.time)

                # Reset the clock
                firefly.clock = 0

            if firefly.clock < 0:
                firefly.clock = 0

        pygame.display.update()
        return flash_counter

    def get_sync_measure(self):
        curr_clocks = [firefly.clock for firefly in self.fireflies]
        return mean(curr_clocks), std(curr_clocks)

    # To start the simpy simulation
    def start_simulation(self):
        filename = "logs/log__" + strftime("%d%m%Y_%H%M%S") + ".csv"
        param_string = "fireflies:{0}, neighbor distance:{1}, nudge:{2}\n".format(
            self.n, self.neighbor_distance, self.nudge_duration
        )
        with open(filename, 'a+') as f:
            f.write(param_string)
            f.write("---------------------------------------------------\n")
            f.write("iteration,mean,std,num\n")
            while self.time < self.until:
                # Update the clocks
                num_flashed = self.__update_firefly_clocks()

                # Wall-clock time between every simulation step
                sleep(0.1)

                # Turn off the lights of the fireflies
                self.space.fill(black)  # Set the background color as black
                pygame.display.update()

                # Increment the time
                self.time += 1

                curr_mean, curr_std = self.get_sync_measure()
                f.write("{0},{1},{2},{3}\n".format(self.time, curr_mean, curr_std, num_flashed))
                f.flush()

    # Exit the simulation
    @staticmethod
    def exit_simulation():
        pygame.quit()
