import pygame
import simpy
from random import sample, randint, random
from math import sqrt

const_black = (0, 0, 0)
const_white = (255, 255, 255)


class FirefliesSimulation:
    def __init__(self, number_of_fireflies, period=20, nudge=2, neighbor_distance=50):
        # Save the parameters of the simulation
        self.n = number_of_fireflies
        self.p = period
        self.blink_duration = 1
        self.canvas_length = 1600               # Default is 1600
        self.canvas_width = 800                 # Default is 800
        self.nudge = nudge
        self.neighbor_distance = neighbor_distance
        self.message_pipes = {}
        self.messages = {}
        self.next_blink_at = {}
        self.neighbors = {}

        # Initialize pygame library
        pygame.init()
        self.space = pygame.display.set_mode((self.canvas_length, self.canvas_width))
        pygame.display.set_caption('Fireflies')

        # Set the background color as black
        self.space.fill(const_black)

        # Initialize the positions of fireflies
        xs = sample(range(self.canvas_length), self.n)
        ys = sample(range(self.canvas_width), self.n)
        self.fireflies_positions = zip(xs, ys)

        # Initialize SimPy environment
        self.simpy_env = simpy.rt.RealtimeEnvironment(factor=0.1)
        for x, y in self.fireflies_positions:
            random_start = randint(1, period)
            self.simpy_env.process(self.__firefly_control(x, y, random_start))
            self.message_pipes[(x, y)] = simpy.Store(self.simpy_env)
            self.messages[(x, y)] = 0

        # Initialize the neighbors dictionary
        for x, y in self.fireflies_positions:
            self.neighbors[(x, y)] = []
        for x1, y1 in self.fireflies_positions:
            for x2, y2 in self.fireflies_positions:
                if (x1, y1) != (x2, y2) and sqrt((x2 - x1)**2 + (y2 - y1)**2) < self.neighbor_distance:
                    self.neighbors[(x1, y1)].append((x2, y2))

    def __firefly_control(self, x, y, init):
        # Every firefly waits for random duration
        yield self.simpy_env.process(self.__firefly(x, y, init))
        self.next_blink_at[(x, y)] = self.simpy_env.now + self.p

        while True:
            firefly_blink = self.simpy_env.process(self.__firefly(x, y, self.next_blink_at[(x, y)] - self.simpy_env.now))
            yield self.message_pipes[(x, y)].get() | firefly_blink
            if self.message_pipes[(x, y)].items > 0:
                # If the event is triggered, nudge the clock, create another event
                # And set the next_blink at (next_blink - nudge)
                for i in range(len(self.message_pipes[(x, y)].items)):
                    flush = self.message_pipes[(x, y)].get()
                    if self.next_blink_at[(x, y)] - self.nudge > self.simpy_env.now:
                        self.next_blink_at[(x, y)] -= self.nudge

            if firefly_blink.triggered:
                self.next_blink_at[(x, y)] = self.simpy_env.now + self.p

    def __firefly(self, x, y, wait):
        # Wait for the longer duration (period)
        yield self.simpy_env.timeout(wait)

        # Light up
        self.__light_up_firefly(self.space, x, y)
        pygame.display.update()

        # Wait for a brief duration (blink)
        yield self.simpy_env.timeout(self.blink_duration)

        # Turn off the light
        self.__turn_off_firefly(self.space, x, y)
        pygame.display.update()

        # Trigger the events of neighbors
        for neighbor in self.neighbors[(x, y)]:
            self.message_pipes[neighbor].put(self.messages[neighbor])
            self.messages[neighbor] += 1

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

    # To start the simpy simulation
    def start_simulation(self):
        self.simpy_env.run()

    # Exit the simulation
    @staticmethod
    def exit_simulation():
        pygame.quit()
