# from static_fireflies_adversarial import FirefliesSimulation
from moving_fireflies_adversarial import FirefliesSimulation
# from static_fireflies import FirefliesSimulation


ff_sim = FirefliesSimulation(period=60, nudge=10, neighbor_distance=100000)
ff_sim.start_simulation()
