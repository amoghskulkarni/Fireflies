import pygame
from random import sample, randint, randrange
from math import sqrt
from time import sleep
from numpy import mean, std

const_black = (0, 0, 0)
const_white = (255, 255, 255)


class FirefliesSimulation:
    def __init__(self, number_of_fireflies, period=50, nudge=15, neighbor_distance=50, until=10000000):
        # Save the parameters of the simulation
        self.time = 0
        self.until = until
        self.n = number_of_fireflies
        self.p = period
        # self.blink_duration = 1
        self.canvas_length = 800                # Default is 1600
        self.canvas_width = 800                 # Default is 800
        self.nudge_duration = nudge
        self.neighbor_distance = neighbor_distance
        self.fireflies_clocks = {}
        self.neighbors = {}
        self.last_nudged_at = {}

        # Initialize the positions of fireflies
        xs = sample(range(self.canvas_length), self.n)
        ys = sample(range(self.canvas_width), self.n)
        self.fireflies_positions = zip(xs, ys)

        # Initialize the neighbors dictionary
        for x, y in self.fireflies_positions:
            self.neighbors[(x, y)] = []
        for x1, y1 in self.fireflies_positions:
            for x2, y2 in self.fireflies_positions:
                if (x1, y1) != (x2, y2) and sqrt((x2 - x1)**2 + (y2 - y1)**2) < self.neighbor_distance:
                    self.neighbors[(x1, y1)].append((x2, y2))
        neighbor_counts = [len(self.neighbors[i]) for i in self.neighbors]
        print "Average neighbors:", sum(neighbor_counts) / float(len(neighbor_counts))

        # Initialize time of every firefly
        for x, y in self.fireflies_positions:
            self.fireflies_clocks[(x, y)] = randint(1, self.p)
            self.last_nudged_at[(x, y)] = 0

        # Initialize pygame library
        pygame.init()
        self.space = pygame.display.set_mode((self.canvas_length, self.canvas_width))
        pygame.display.set_caption('Fireflies')
        self.space.fill(const_black)        # Set the background color as black

    # Private method to update firefly clocks
    def __update_firefly_clocks(self):
        flash_counter = 0
        for x, y in self.fireflies_positions:
            # Increment the clock
            self.fireflies_clocks[(x, y)] += 1
            # If the firefly's clock reached period, it's time to shine
            if self.fireflies_clocks[(x, y)] > self.p:
                flash_counter += 1
                # Spread the light (will be turned off outside this function)
                self.__light_up_firefly(self.space, x, y)

                # Nudge every neighbor that is not nudged at this time step
                for neighbor in self.neighbors[(x, y)]:
                    if self.last_nudged_at[neighbor] != self.time:
                        if self.fireflies_clocks[neighbor] >= (self.p / 2):
                            self.fireflies_clocks[neighbor] += self.nudge_duration
                        else:
                            self.fireflies_clocks[neighbor] -= self.nudge_duration
                        self.last_nudged_at[neighbor] = self.time

                # Reset the clock
                self.fireflies_clocks[(x, y)] = 0

            if self.fireflies_clocks[(x, y)] < 0:
                self.fireflies_clocks[(x, y)] = 0

        pygame.display.update()
        return flash_counter

    # Private method to light up the firefly
    @staticmethod
    def __light_up_firefly(game_display, location_x, location_y):
        for x in range(location_x - 3, location_x + 3):
            for y in range(location_y - 3, location_y + 3):
                game_display.set_at((abs(x), abs(y)), const_white)

    # Private method to turn off the firefly
    @staticmethod
    def __turn_off_firefly(game_display, location_x, location_y):
        for x in range(location_x - 3, location_x + 3):
            for y in range(location_y - 3, location_y + 3):
                game_display.set_at((abs(x), abs(y)), const_black)
        pygame.display.update()

    def get_sync_measure(self):
        curr_clocks = [value for key, value in self.fireflies_clocks.iteritems()]
        return mean(curr_clocks), std(curr_clocks)

    # To start the simpy simulation
    def start_simulation(self):
        with open("log.csv", 'a+') as f:
            f.write("iteration,mean,std,num\n")
            while self.time < self.until:
                # Update the clocks
                num_flashed = self.__update_firefly_clocks()

                # Wall-clock time between every simulation step
                sleep(0.1)

                # Turn off the lights of the fireflies
                self.space.fill(const_black)  # Set the background color as black
                pygame.display.update()

                # Increment the time
                self.time += 1

                curr_mean, curr_std = self.get_sync_measure()
                f.write("{0},{1},{2},{3}\n".format(self.time, curr_mean, curr_std, num_flashed))

    # Exit the simulation
    @staticmethod
    def exit_simulation():
        pygame.quit()
