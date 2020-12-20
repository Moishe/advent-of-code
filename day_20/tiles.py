import json
import pathlib
import re

from collections import defaultdict

lines = [x.rstrip() for x in open(pathlib.Path(__file__).parent.absolute() / 'test_tiles.txt').readlines()]

edge_map = defaultdict(list)
tiles = {}

while lines:
    tile = re.match('Tile ([0-9]+):', lines.pop(0)).group(1)
    print(tile)
    top = lines[0]
    bottom = ''.join(lines[9])
    left = ''.join([x[0] for x in lines[0:10]])
    right = ''.join([x[9] for x in lines[0:10]])

    tiles[tile] = [top, bottom, left, right]
    #tiles[tile].extend([''.join(reversed(x)) for x in tiles[tile]])

    for edge in tiles[tile]:
        edge_map[''.join(reversed(edge))].append(tile)
        edge_map[edge].append(tile)

    lines = lines[11:]

print(json.dumps(tiles, indent=2))
print(json.dumps(edge_map, indent=2))

matches = defaultdict(list)
for (tile, edges) in tiles.items():
    print("Looking for matches to %s" % tile)
    # find matches
    for edge in edges:
        """
        reversed_edge = ''.join(reversed(edge))

        if reversed_edge in edge_map:
            match = edge_map[reversed_edge]
            if tile not in match:
                matches[tile].extend(edge_map[reversed_edge])
        """
        if edge in edge_map:
            match = edge_map[edge]
            for m in match:
                if tile != m:
                    matches[tile].append(m)

print(json.dumps(matches, indent=2))

for (tile, m) in matches.items():
    if len(m) == 2:
        print(tile)