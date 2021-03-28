import numpy as np
import constants as const

class Body:
    #Constructor for body
    def __init__(self, name, c, m, radius, d):
        #Sets name, colour, mass, and radius
        self.name = name
        self.c = c
        self.m = m
        self.radius = radius
        self.d = d

        #Initial position set to distance from sun
        self.r = np.array([d, 0])

        #Bool to check is body has completed an orbit
        self.orbited = False

        #Approximates initial velocity based on distance from sun
        #Innacurate since realistically other bodies will have an effect on this
        if d != 0:
            self.v = np.array([0, np.sqrt(const.G*const.MassOfSun/d)])
        #If d == 0 then this is the sun, so assume sun starts with initial velocity of 0
        #Again inaccurate but good enough
        else:
            self.v = np.array([0, 0])
    
    #Applies algorithm that calculates acceleration to find a(0) and a(0 - dt)
    def get_init_accn(self, bodies):
        acc = np.array([0, 0])
        
        #Loops over bodies
        for body in bodies:
            #Ignores self
            if body.name != self.name:
                #Applies formula
                acc = acc + body.m/np.sqrt((self.r - body.r)[0]**2 +(self.r - body.r)[1]**2)**3 * (self.r - body.r)

        acc = acc * -const.G
        self.a_prev = acc
        self.a_curr = acc

    #Updates position using the Beeman method
    def update_position(self, time):
        #Stores y coord before position update
        y_before = self.r[1]

        #Calculates new position
        self.r = self.r + self.v*const.dt + (4*self.a_curr - self.a_prev)*(const.dt**2)*1/6

        #If the body has not yet completed an orbit and it is not the sun
        if not self.orbited and self.name != 'Sun':
            #If the body crosses y axis from below, an orbit has been completed
            if y_before < 0 and self.r[1] > 0:
                print(f'{self.name} has completed an orbit after {time/60/60/24/365} Earth years')
                self.orbited = True

    #Calculates a(t+dt) from gravitational force law
    def get_next_accn(self, bodies):
        acc = np.array([0.0, 0.0])

        #Loops over bodies
        for body in bodies:
            #Planet not affected by itself so ignores
            if body.name != self.name:
                #Applies formula
                acc = acc + body.m/np.sqrt((self.r - body.r)[0]**2 +(self.r - body.r)[1]**2)**3 * (self.r - body.r)
        self.a_next = acc * -const.G

    #Updates velocity using Beeman
    def update_velocity(self):
        self.v = self.v + 1/6*(2*self.a_next + 5*self.a_curr - self.a_prev) * const.dt

    #Updates accelerations
    def update_accn(self):
        a_curr_copy = self.a_curr
        self.a_prev = a_curr_copy
        self.a_curr = self.a_next

    #Calculates kinectic energy of the body
    def get_ek(self):
        return 1/2 * self.m * (self.v[0]**2 + self.v[1]**2)

    #Calculates potential energy between this body and all other bodies
    def get_eu(self, bodies):
        u = 0
        for body in bodies:
            if body.name != self.name:
                u += (self.m * body.m)/np.sqrt((self.r - body.r)[0]**2 +(self.r - body.r)[1]**2)
        return u * const.G
