import simpy
from random import seed, randint
seed(23)


class EV:
    def __init__(self, env):
        self.env = env
        self.drive_proc = env.process(self.drive(env))

    def drive(self, env):
        while True:
            # Drive for 20-40 min
            yield env.timeout(randint(20, 40))
            print "1", env.now

            # Park for 1 hour
            print('Start parking at', env.now)
            # self.charging = env.process(self.bat_ctrl(env))
            yield env.process(self.bat_ctrl(env))
            print "2", env.now
            # self.parking = env.timeout(60)
            # yield self.charging | self.parking
            # if not self.charging.triggered:
                # Interrupt charging if not already done.
                # self.charging.interrupt('Need to go!')
            print('Stop parking at', env.now)

    def bat_ctrl(self, env):
        print('Bat. ctrl. started at', env.now)
        try:
            print "3", env.now
            yield env.timeout(randint(60, 90))
            print "4", env.now
            print('Bat. ctrl. done at', env.now)
        except simpy.Interrupt as i:
            # Onoes! Got interrupted before the charging was done.
            print('Bat. ctrl. interrupted at', env.now, 'msg:',
                  i.cause)

env = simpy.Environment()
ev = EV(env)
env.run(until=100)