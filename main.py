from moving_fireflies_adversarial import FirefliesSimulation

ff_sim = FirefliesSimulation(100, period=30, nudge=5, neighbor_distance=10000)
ff_sim.start_simulation()
