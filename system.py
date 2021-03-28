from body import Body
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import constants as const
import numpy as np
from satellite import Satellite

class SolarSystem:
    #Constructor function, takes in list of bodies for the system
    def __init__(self, bodies, n):
        #Sets array of bodies
        self.bodies = bodies

        #Initialises acceleration for all bodies
        for body in self.bodies:
            body.get_init_accn(self.bodies)

        #Starts system time
        self.time = 0

        #Array to store energy readings
        self.energies = []

        #Sets number of frames simulation is to run for
        self.n = n

        #Empty array for patches
        self.patches = []

        #Satellite count
        self.satellite_count = 0

        #Loops over bodies
        for body in self.bodies:
            #Handles sun separately, similar to the above
            #Adds patches for all bodies to patches array
            if body.name == 'Sun':
                self.patches.append(plt.Circle(body.r/const.PixelToKM, 
                                            radius=body.radius/const.PixelToKM, 
                                            color = body.c, 
                                            animated = True))
            else:
                self.patches.append(plt.Circle(body.r/const.PixelToKM/const.DistScaleFactor, 
                                            radius = body.radius/const.PixelToKM*const.SizeScaleFactor, 
                                            color = body.c, 
                                            animated = True))

    def add_satellite(self, body_name, vi, s_name, r, m, target, d=0):
        """
        Adds a satellite to the system a distance from the surface of a specific body

        body_name: name of body the satellite starts at
        vi: velocity of satellite
        s_name: name of satellite
        r: radius of satellite
        m: mass of satellite
        target: name of body satellite is aiming for
        d: extra added distance from body, use when adding more than one satellite to body
        """

        #Loops over bodies selecting the specified starting body
        for body in self.bodies:
            if body.name == body_name:
                #Creates a new satellite with the given parameters
                s = Satellite(s_name, 'green', m, r, body.d - 2*body.radius - d, vi, target)

                #Calculates initial acceleration of satellite
                s.get_init_accn(self.bodies)

                #Adds satellite to system bodies and a circle to the patches for animation
                self.bodies.append(s)
                self.patches.append(plt.Circle(s.r/const.PixelToKM/const.DistScaleFactor, 
                                        radius = s.radius/const.PixelToKM*const.SatelliteScaleFactor, 
                                        color = s.c, 
                                        animated = True))

                #Increment satellite couint and then break
                self.satellite_count += 1
                break
    
    #Init function for animation
    def init(self):
        return self.patches

    #Updates every body in the system, called once per timestep
    def update(self):
        for body in self.bodies:
            body.update_position(self.time)
        for body in self.bodies:
            body.get_next_accn(self.bodies)
        for body in self.bodies:
            body.update_velocity()
        for body in self.bodies:
            body.update_accn()

    #Animate function
    def animate(self, i):
        #Updates bodies
        self.update()

        #Increments time
        self.time += const.dt

        #Appends system energy to energies array
        self.energies.append(self.get_system_energy())
        
        #Loops over bodies
        for i in range(len(self.bodies)):
            #Sun has to be handled seperately due to scaling
            if self.bodies[i].name != 'Sun':
                #Updates patch position to position of body, scaled appropriately
                self.patches[i].center = self.bodies[i].r/const.PixelToKM/const.DistScaleFactor
            else:
                #Sun is scaled differently so that other bodies are visible
                self.patches[i].center = self.bodies[i].r/const.PixelToKM

        return self.patches

    #Calculates total energy in the system
    def get_system_energy(self):
        K = 0
        U = 0
        for body in self.bodies:
            K += body.get_ek()
            U += body.get_eu(self.bodies)
        U /= 2
        return K + U

    #Function called once to start animation
    def show(self):
        #Gets figure and axes
        fig = plt.figure(figsize=(10, 10))
        ax = plt.axes()

        #Sets limits so that all bodies are shown
        ax.set_xlim(-16000, 16000)
        ax.set_ylim(-16000, 16000)

        #Background colour
        ax.set_facecolor((51/255, 51/255, 51/255))
        
        #Adds patches to axes
        for patch in self.patches:
            ax.add_patch(patch)

        #Starts animation
        anim = FuncAnimation(fig, 
                            self.animate, 
                            init_func = self.init, 
                            frames = self.n, 
                            repeat = False, 
                            interval = 1, 
                            blit = True)
        plt.show()

        #Loops over all satellites in system (these will be last bodies in array)
        for i in range(1, self.satellite_count + 1):
            s = self.bodies[-i]
            
            #Prints distance of each satellite from its target and the time required to achieve this
            print(f'Minimum distance to {s.name} from {s.target} achieved is {min(s.distances)/1000} km')
            print(f'This is achieved after {s.distances.index(min(s.distances)) * const.dt / 60 / 60 / 24} earth days')

        #Saves energies to csv file
        np.array(self.energies).tofile('energies.csv', sep=',')

        #Plots energy graph at end of simulation
        fig = plt.figure(figsize=(10, 10))
        ax = plt.axes()
        plt.title('Energy of system over time')
        plt.xlabel('time (s)')
        plt.ylabel('energy (J)')
        plt.plot(np.linspace(0, self.n*const.dt, self.n), self.energies)
        ax.set_ylim(0, max(self.energies)*2)
        plt.savefig('unzoomed.png')
        plt.show()

        #Plots zoomed energy graph
        fig = plt.figure(figsize=(10, 10))
        ax = plt.axes()
        plt.title('Energy of system over time')
        plt.xlabel('time (s)')
        plt.ylabel('energy (J)')
        plt.savefig('zoomed.png')
        plt.plot(np.linspace(0, self.n*const.dt, self.n), self.energies)
        plt.show()