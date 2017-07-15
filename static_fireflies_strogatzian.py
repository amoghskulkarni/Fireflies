from random import sample
from lib.firefly import Firefly, FirefliesSimulation

black = (0, 0, 0)
white = (255, 255, 255)


class StrogatzianFirefly(Firefly):
    def nudge_clock(self, nudge):
        # delta = (self.period + 0.1) - self.clock
        # self.clock += (0.1 * delta * nudge)
        self.clock += nudge

    def update_clock(self):
        delta = (self.period + 1) - self.clock
        self.clock += (0.1 * delta)


class StrogatzianFirefliesSimulation(FirefliesSimulation):
    def __init__(self, n_fireflies=100, period=50, nudge=15, neighbor_distance=50, movement=False):
        FirefliesSimulation.__init__(self, n_fireflies=n_fireflies,
                                     nudge=nudge,
                                     neighbor_distance=neighbor_distance,
                                     movement=movement)

        # Sample the positions of the fireflies
        xs = sample(range(self.canvas_length), self.n)
        ys = sample(range(self.canvas_width), self.n)

        # Create the firefly objects and store them
        for n in range(self.n):
            self.fireflies.append(StrogatzianFirefly(x=xs[n], y=ys[n], period=period))

        # Populate their neighbors
        self.update_firefly_neighbors()
