import math
import numpy
import pathlib
import re

f = open(pathlib.Path(__file__).parent.absolute() / 'test_input.txt')

directions = {
    'N': [0, -1],
    'S': [0, 1],
    'E': [1, 0],
    'W': [-1, 0]
}

rotations = {
    'R': 90,
    'L': -90,
}

current_direction = directions['E']
position = [0,0]

def rotate(action, angle, current_direction):
    rad = math.radians(angle)
    return [
        int(current_direction[0] * math.cos(rad) - current_direction[1] * math.sin(rad)),
        int(current_direction[0] * math.sin(rad) + current_direction[1] * math.cos(rad))
    ]

m = re.compile('^([A-Z])([0-9]+)$')
for l in f:
    l = l.rstrip()
    g = m.match(l)
    action = g.group(1)
    distance = int(g.group(2))

    print("%s: %d" % (action, distance))

    vector = [0,0]
    if action in rotations:
        current_direction = rotate(action, distance, current_direction)
        print("New direction: %s" % current_direction)
    elif action in directions:
        vector = numpy.multiply(distance, directions[action])
    elif action == 'F':
        vector = numpy.multiply(distance, current_direction)

    print("Moving %s" % vector)
    position = numpy.add(position, vector)

    print("New position: %s" % position)