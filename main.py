from fireflies_continuous import FirefliesSimulation

ff_sim = FirefliesSimulation(100, period=30, nudge=5, neighbor_distance=100)
ff_sim.start_simulation()
