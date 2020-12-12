import math
import numpy
import pathlib
import re

f = open(pathlib.Path(__file__).parent.absolute() / 'input.txt')

directions = {
    'N': [0, 1],
    'S': [0, -1],
    'E': [1, 0],
    'W': [-1, 0]
}

rotations = {
    'R': -1,
    'L': 1,
}

ship_position = [0,0]
waypoint = [10, 1]

def rotate(action, angle, current_direction):
    rad = math.radians(angle)
    return [
        int(round(current_direction[0] * math.cos(rad) - current_direction[1] * math.sin(rad))),
        int(round(current_direction[0] * math.sin(rad) + current_direction[1] * math.cos(rad)))
    ]

m = re.compile('^([A-Z])([0-9]+)$')
for l in f:
    l = l.rstrip()
    g = m.match(l)
    action = g.group(1)
    distance = int(g.group(2))

    print("Ship Position:  %s" % ship_position)
    print("Waypoint: %s" % waypoint)
    print("%s: %d" % (action, distance))

    if action in rotations:
        waypoint = rotate(action, rotations[action] * distance, waypoint)
    elif action in directions:
        vector = numpy.multiply(distance, directions[action])
        waypoint = numpy.add(waypoint, vector)
    elif action == 'F':
        # move the ship                
        vector = numpy.multiply(distance, waypoint)
        ship_position = numpy.add(ship_position, vector)

print("New position: %s" % ship_position)
print("Sum: %d" % (sum([abs(x) for x in ship_position])))