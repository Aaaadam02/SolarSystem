import numpy as np
import constants as const
from body import Body

#Subclass of Body for satellites
class Satellite(Body):
    #Constructor function
    def __init__(self, name, c, m, radius, d, vi, target):
        #Calls the Body constructor function
        super(Satellite, self).__init__(name, c, m, radius, d)

        #Adds given velocity to inital velocity of satellite
        self.v += vi

        #Empty array to store distance from target planet at each time step
        self.distances = []
        self.target = target

    #Calculates a(t+dt) from gravitational force law
    def get_next_accn(self, bodies):
        acc = np.array([0.0, 0.0])

        #Loops over bodies
        for body in bodies:
            #Planet not affected by itself so ignores
            if body.name != self.name:
                #If body is target, append distance from target to array
                if body.name == self.target:
                    self.distances.append(np.sqrt((self.r - body.r)[0]**2 +(self.r - body.r)[1]**2))
                
                #Apply formula
                acc = acc + body.m/np.sqrt((self.r - body.r)[0]**2 +(self.r - body.r)[1]**2)**3 * (self.r - body.r)

        self.a_next = acc * -const.G