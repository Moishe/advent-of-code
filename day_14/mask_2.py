from collections import defaultdict
import pathlib
import re

f = open(pathlib.Path(__file__).parent.absolute() / 'input.txt')

lines = [x.rstrip() for x in f.readlines()]

def fan_out_memset(location, degrees_of_freedom, value):
    global sparse_memory_blob
    locations = []
    for i in range(pow(2, len(degrees_of_freedom))):
        this_location = location
        for x in range(len(degrees_of_freedom)):
            p = pow(2, degrees_of_freedom[x])
            if pow(2,x) & i:
                this_location |= p
            else:
                this_location &= ~p
        locations.append(this_location)
    values = zip(locations, [value] * len(locations))
    sparse_memory_blob.update(values)
            

sparse_memory_blob = {}
for line in lines:
    if not line:
        continue
    print(line)
    m = re.match(r'^mask = (.*)$', line)
    if m:
        # build mask and overlay
        mask_source = m.groups()[0]
        mask_mask = int(mask_source.replace('1', '0').replace('X', '1'), 2)
        degrees_of_freedom = []
        idx = len(mask_source) - 1
        for c in mask_source:
            if c == 'X':
                degrees_of_freedom.append(idx)
            idx -= 1

        mask_value = int(mask_source.replace('X', '0'), 2)
        #print("mask: %s: %s, %s" % (mask_source, bin(mask_mask), bin(mask_value)))
    else:
        (location, value) = [int(x) for x in re.match(r'^mem\[([0-9]+)\] = ([0-9]+)$', line).groups()]
        location = location | mask_value
        fan_out_memset(location, degrees_of_freedom, value)

print("Sparse blob: %s" % sparse_memory_blob)
print("Sum: %d" % sum(sparse_memory_blob.values()))
