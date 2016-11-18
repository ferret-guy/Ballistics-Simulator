import math
import numpy
from scipy.integrate import odeint
import matplotlib.pyplot as plt


class BallisticObject:
    """Trajectory simulation ODEs and other information
    from USNA: https://www.usna.edu/Users/mecheng/ratcliff/EM375/labs/07Project/ProjectileTheory.pdf"""

    def __init__( self, posY=0, velI=0, angI=0, refArea=0, projMass=0, airDen=1.225, accG=9.8066, Cd=0):
        """All inputs in standard si units
        (Kg/m/s/rad ect...)"""
        self.posY = posY
        self.velI = velI
        self.velX = (math.cos(angI) * velI)
        self.velY = (math.sin(angI) * velI)
        self.accG = accG
        self.DragF = Cd * refArea * airDen / 2 / projMass
        # Initial state space for ODEs
        # x, xdot, y, ydot
        self.initialConditions = numpy.zeros(4)
        self.initialConditions[0] = 0
        self.initialConditions[1] = self.velX
        self.initialConditions[2] = self.posY
        self.initialConditions[3] = self.velY

    def set_angle(self, angle, velI=None):
        """Set the angle for the simulation, optionally
         allowing the vel to be reset"""
        if velI is None:
            velI = self.velI
        self.velX = (math.cos(angle) * velI)
        self.velY = (math.sin(angle) * velI)

    def traj_func(self, state, time):
        """ODE function for projectile motion"""
        f = numpy.zeros(4)
        f[0] = state[1]
        f[1] = -self.DragF * math.sqrt(state[1]**2 + state[3]**2) * state[1]
        f[2] = state[3]
        f[3] = -self.accG - self.DragF * math.sqrt(state[1]**2 + state[3]**2) * state[3]
        return f

    def run_sim(self, startT=0, stopT=None, timeStep=0.001, testStep=1):
        """Function to run sim either until the object hits the ground or for a specified time
        This depends on weather stopT is set to a value
        startT: Start time for the simulation
        stopT: Stop time for the simulation (leave blank to run until the ground)
        timeStep: reported time steps for the simulation
        testStep: amount of time to run for each iteration while waiting until you hit the ground
        """

        # If stopT is not none we are just going to run for the specified time
        if stopT is not None:
            t = numpy.arange(startT, stopT, timeStep)
            return odeint(self.traj_func, self.initialConditions, t)

        # otherwise we are going to run until our y coordinate is less than 0
        t = numpy.arange(startT, startT + testStep, timeStep)
        ret = odeint(self.traj_func, self.initialConditions, t)

        while ret[-1][2] > 0:
            startT += testStep
            t = numpy.arange(startT, startT + testStep, timeStep)
            ret = numpy.concatenate((ret, odeint(self.traj_func, ret[-1], t)))

        return filter(lambda x: x[2] > 0, ret)

    def run_and_dispaly(self):
        """Function to run and display the output"""
        arr = self.run_sim()
        plt.plot(zip(*arr)[0], zip(*arr)[2], '-', linewidth=2)
        plt.xlim([0, max(zip(*arr)[0])])
        plt.ylim([0, (max(zip(*arr)[2]) * 1.1)])
        plt.xlabel('x pos (m)')
        plt.ylabel('y pos (m)')
        plt.suptitle('Projectile Position Graph', fontsize=14, fontweight='bold')
        plt.savefig('data.png')
        plt.show()
