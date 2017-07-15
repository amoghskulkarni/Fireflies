# File which includes the base class for fireflies

import pygame
from math import sqrt
from time import sleep, strftime
from numpy import mean, std
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

    def update_clock(self):
        # Increment the clock
        self.clock += 1

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
    def __init__(self, n_fireflies=100, nudge=15, neighbor_distance=50, movement=False):
        # Save the parameters of the simulation
        self.canvas_length = 800                # Default is 800
        self.canvas_width = 800                 # Default is 800
        self.space = None

        self.movement = movement
        self.time = 0
        self.nudge_duration = nudge

        self.n = n_fireflies
        self.fireflies = []
        self.neighbor_distance = neighbor_distance

    def visualization_init(self):
        # Initialize pygame library
        pygame.init()
        self.space = pygame.display.set_mode((self.canvas_length, self.canvas_width))
        pygame.display.set_caption('Fireflies')
        self.space.fill(black)        # Set the background color as black

    # Private method to update firefly clocks
    def update_firefly_clocks(self):
        for firefly in self.fireflies:
            # Increment the clock
            firefly.update_clock()

    # Private method to make the fireflies flash
    # This method returns the references of fireflies which flashed in this simulation time step
    def flash_fireflies(self):
        flashed = []
        for firefly in self.fireflies:
            # If the firefly's clock reached period, it's time to shine
            if firefly.clock >= firefly.period:
                # Reset the clock
                firefly.clock = 0

                flashed.append(firefly)
        return flashed

    # Private method to make the flashed fireflies visualize
    def visualize_flashed_fireflies(self, flashed):
        for firefly in flashed:
            # Spread the light (will be turned off outside this function)
            firefly.light_up(self.space)
        pygame.display.update()

    # Private method to nudge the clocks
    def do_local_communication(self, flashed):
        for firefly in flashed:
            # Nudge every neighbor that is not nudged at this time step
            for neighbor in firefly.neighbors:
                if neighbor.last_nudged_at != self.time:
                    neighbor.nudge_clock(self.nudge_duration)

                    if neighbor.clock < 0:
                        neighbor.clock = 0

                    neighbor.set_last_nudged_at(self.time)

    # Private method to update firefly positions
    # This will try to move the firefly to a new position,
    # but won't move it if there's one already there
    def update_firefly_positions(self):
        x_factor = int(self.canvas_length / 200)
        y_factor = int(self.canvas_width / 200)
        moved = 0
        for firefly in self.fireflies:
            old_x = firefly.x
            old_y = firefly.y
            x_op = randint(0, 1)
            y_op = randint(0, 1)
            if x_op == 1:
                # x + x-factor
                new_x = old_x + x_factor if old_x + x_factor <= self.canvas_length else old_x
            else:
                # x - x-factor
                new_x = old_x - x_factor if old_x - x_factor >= 0 else old_x
            if y_op == 1:
                # y + y-factor
                new_y = old_y + y_factor if old_y + y_factor <= self.canvas_width else old_y
            else:
                # y - y-factor
                new_y = old_y - y_factor if old_y - y_factor >= 0 else old_y
            other_firefly_present = False
            for other_firefly in self.fireflies:
                # If there's some other firefly in the new position, stay where you are
                if other_firefly.x == new_x and other_firefly.y == new_y:
                    other_firefly_present = True
                    break
            if not other_firefly_present:
                # print "({0}, {1}) changed position to ({2}, {3})".format(old_x, old_y, new_x, new_y)
                firefly.x = new_x
                firefly.y = new_y
                moved += 1
        # print "{0} fireflies moved @{1}".format(moved, self.time)

    # Private method to update firefly neighbors
    def update_firefly_neighbors(self):
        for firefly in self.fireflies:
            firefly.neighbors = []

        for firefly1 in self.fireflies:
            for firefly2 in self.fireflies:
                x1 = firefly1.x
                y1 = firefly1.y
                x2 = firefly2.x
                y2 = firefly2.y
                if firefly1 != firefly2 and sqrt((x2 - x1)**2 + (y2 - y1)**2) < self.neighbor_distance:
                    firefly1.neighbors.append(firefly2)

    def move_fireflies(self):
        self.update_firefly_positions()
        self.update_firefly_neighbors()

    # To start the simulation
    def start_simulation(self, until=10000000, visualize=False):
        filename = "logs/log__" + strftime("%d%m%Y_%H%M%S") + ".csv"
        param_string = "total fireflies:{0}, neighbor distance:{1}, nudge:{2}\n".format(
            self.n, self.neighbor_distance, self.nudge_duration
        )

        # Init the visualization
        if visualize:
            self.visualization_init()

        with open(filename, 'a+') as f:
            f.write(param_string)
            f.write("---------------------------------------------------\n")
            f.write("iteration,mean,std,num\n")
            while self.time < until:
                # Update the clocks
                self.update_firefly_clocks()

                # Make the fireflies flash
                flashed = self.flash_fireflies()

                # Make them appear on the canvas
                if visualize:
                    self.visualize_flashed_fireflies(flashed)

                # Do the local communication i.e. nudge the clocks
                self.do_local_communication(flashed)

                # Turn off the lights of the fireflies
                if visualize:
                    # Wall-clock time between every simulation step
                    self.wait()

                    # Set the background color as black
                    self.space.fill(black)
                    pygame.display.update()

                if self.movement:
                    if self.time % 10 == 0:
                        self.move_fireflies()

                # Increment the time
                self.time += 1

                curr_mean, curr_std = self.get_sim_stats()
                f.write("{0},{1},{2},{3}\n".format(self.time, curr_mean, curr_std, len(flashed)))
                f.flush()

                if not visualize:
                    if self.time % 1000 == 0:
                        print "{0}: Degree of synchronization = ...".format(self.time)

    # Get simulation stats
    def get_sim_stats(self):
        curr_clocks = [firefly.clock for firefly in self.fireflies]
        return mean(curr_clocks), std(curr_clocks)

    # Duration of every simulation step
    @staticmethod
    def wait():
        sleep(0.1)

    # Exit the simulation
    @staticmethod
    def exit_simulation():
        pygame.quit()
