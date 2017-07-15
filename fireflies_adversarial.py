from random import sample
from lib.firefly import Firefly, FirefliesSimulation

black = (0, 0, 0)
white = (255, 255, 255)


class NonAdversarialFirefly(Firefly):
    def nudge_clock(self, nudge):
        if self.clock >= (self.period / 2):
            self.clock += nudge
        else:
            self.clock -= nudge


class AdversarialFirefly(Firefly):
    def nudge_clock(self, nudge):
        if self.clock >= (self.period / 2):
            self.clock -= nudge
        else:
            self.clock += nudge


class AdversarialFirefliesSimulation(FirefliesSimulation):
    def __init__(self, n_fireflies=100, n_ad_fireflies=5, period=50, nudge=15, neighbor_distance=50, movement=False):
        FirefliesSimulation.__init__(self, n_fireflies=n_fireflies,
                                     nudge=nudge,
                                     neighbor_distance=neighbor_distance,
                                     movement=movement)

        self.n_ad = n_ad_fireflies

        # Sample the positions of the fireflies
        xs = sample(range(self.canvas_length), self.n)
        ys = sample(range(self.canvas_width), self.n)

        # Create the (normal and adversarial) firefly objects and store them
        for n in range(self.n - self.n_ad):
            self.fireflies.append(NonAdversarialFirefly(x=xs[n], y=ys[n], period=period))
        for n in range(self.n_ad):
            self.fireflies.append(AdversarialFirefly(x=xs[-1 * n], y=ys[-1 * n], period=period))

        # Populate their neighbors
        self.update_firefly_neighbors()


if __name__ == "__main__":
    # Movement is off by default
    ff_sim = AdversarialFirefliesSimulation(period=60, nudge=10, neighbor_distance=150)
    ff_sim.start_simulation()
