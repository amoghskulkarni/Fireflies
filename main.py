# from static_fireflies_adversarial import FirefliesSimulation
# from moving_fireflies_adversarial import FirefliesSimulation
# from static_fireflies import FirefliesSimulation
# from moving_fireflies import FirefliesSimulation
from static_fireflies_strogatzian import StrogatzianFirefliesSimulation
# from moving_fireflies_strogatzian import FirefliesSimulation

ff_sim = StrogatzianFirefliesSimulation(period=60, nudge=10, neighbor_distance=150)
ff_sim.start_simulation()
