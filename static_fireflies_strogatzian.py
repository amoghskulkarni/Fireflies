import pygame
from random import sample
from math import sqrt
from time import sleep, strftime
from numpy import mean, std
from lib.firefly import Firefly

black = (0, 0, 0)
white = (255, 255, 255)


class StrogatzianFirefly(Firefly):
    def nudge_clock(self, nudge):
        self.clock += nudge

    def update_clock(self):
        


class FirefliesSimulation:
    def __init__(self, n_fireflies=100, period=50, nudge=15, neighbor_distance=50):
        # Save the parameters of the simulation
        self.canvas_length = 800                # Default is 800
        self.canvas_width = 800                 # Default is 800
        self.time = 0
        self.n = n_fireflies
        self.fireflies = []

        self.neighbor_distance = neighbor_distance
        self.nudge_duration = nudge

        # Sample the positions of the fireflies
        xs = sample(range(self.canvas_length), self.n)
        ys = sample(range(self.canvas_width), self.n)

        # Create the firefly objects and store them
        for n in range(self.n):
            self.fireflies.append(StrogatzianFirefly(x=xs[n], y=ys[n], period=period))

        # Populate their neighbors
        self.__update_firefly_neighbors()

    def __visualization_init(self):
        # Initialize pygame library
        pygame.init()
        self.space = pygame.display.set_mode((self.canvas_length, self.canvas_width))
        pygame.display.set_caption('Fireflies')
        self.space.fill(black)        # Set the background color as black

    # Private method to update firefly clocks
    def __update_firefly_clocks(self):
        for firefly in self.fireflies:
            # Increment the clock
            firefly.update_clock()

    # Private method to make the fireflies flash
    def __flash_fireflies(self):
        flashed = []
        for firefly in self.fireflies:
            # If the firefly's clock reached period, it's time to shine
            if firefly.clock >= firefly.period:
                # Reset the clock
                firefly.clock = 0

                flashed.append(firefly)
        return flashed

    # Private method to make the flashed fireflies visualize
    def __visualize_flashed_fireflies(self, flashed):
        for firefly in flashed:
            # Spread the light (will be turned off outside this function)
            firefly.light_up(self.space)
        pygame.display.update()

    # Private method to nudge the clocks
    def __do_local_communication(self, flashed):
        for firefly in flashed:
            # Nudge every neighbor that is not nudged at this time step
            for neighbor in firefly.neighbors:
                if neighbor.last_nudged_at != self.time:
                    neighbor.nudge_clock(self.nudge_duration)

                    if neighbor.clock < 0:
                        neighbor.clock = 0

                    neighbor.set_last_nudged_at(self.time)

    # Private method to update firefly neighbors
    def __update_firefly_neighbors(self):
        for firefly in self.fireflies:
            firefly.neighbors = []

        for firefly1 in self.fireflies:
            for firefly2 in self.fireflies:
                x1 = firefly1.x
                y1 = firefly1.y
                x2 = firefly2.x
                y2 = firefly2.y
                if firefly1 != firefly2 and sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) < self.neighbor_distance:
                    firefly1.neighbors.append(firefly2)

    # To start the simulation
    def start_simulation(self, until=10000000, visualize=True):
        filename = "logs/log__" + strftime("%d%m%Y_%H%M%S") + ".csv"
        param_string = "total fireflies:{0}, neighbor distance:{1}, nudge:{2}\n".format(
            self.n, self.neighbor_distance, self.nudge_duration
        )

        # Init the visualization
        if visualize:
            self.__visualization_init()

        with open(filename, 'a+') as f:
            f.write(param_string)
            f.write("---------------------------------------------------\n")
            f.write("iteration,mean,std,num\n")
            while self.time < until:
                # Update the clocks
                self.__update_firefly_clocks()

                # Make the fireflies flash
                flashed = self.__flash_fireflies()

                # Make them appear on the canvas
                if visualize:
                    self.__visualize_flashed_fireflies(flashed)

                # Do the local communication i.e. nudge the clocks
                self.__do_local_communication(flashed)

                # Turn off the lights of the fireflies
                if visualize:
                    # Wall-clock time between every simulation step
                    self.__wait()

                    # Set the background color as black
                    self.space.fill(black)
                    pygame.display.update()

                # Increment the time
                self.time += 1

                curr_mean, curr_std = self.get_sim_stats()
                f.write("{0},{1},{2},{3}\n".format(self.time, curr_mean, curr_std, len(flashed)))
                f.flush()

    # Get simulation stats
    def get_sim_stats(self):
        curr_clocks = [firefly.clock for firefly in self.fireflies]
        return mean(curr_clocks), std(curr_clocks)

    # Duration of every simulation step
    @staticmethod
    def __wait():
        sleep(0.1)

    # Exit the simulation
    @staticmethod
    def exit_simulation():
        pygame.quit()
