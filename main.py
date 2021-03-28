from system import SolarSystem
from body import Body
import constants as const
import numpy as np

def main():
    #Empty array
    bodies = []

    #Opens csv file containing body information
    f = open('bodies.csv', 'r')

    #Reads file line by line
    for line in f:
        #Splits lines at commas
        a = line.split(', ')

        #Adds a new body to array
        bodies.append(Body(a[0], a[1], float(a[2]), float(a[3]), float(a[4])))

    #Creates a new system that runs for 4000 frames
    system = SolarSystem(bodies, 4000)

    #Adds a satellite to system

    #Flies past Mars, returns to orbit sun
    system.add_satellite('Earth', np.array([-9998,-2984.9]), 'Sattelite 1', 5, 10000, 'Mars')
    
    #Gets propelled in a random direction once close to Mars
    #system.add_satellite('Earth', np.array([-9997.8,-2986]), 'Sattelite 2', 5, 10000, 'Mars')

    #Closest I can get to mars with 2dp of precision, propelled at high velocity
    #system.add_satellite('Earth', np.array([-9997.53,-2985.98]), 'Sattelite 3', 5, 10000, 'Mars')

    #Simulates system
    system.show()

main()
