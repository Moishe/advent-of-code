from collections import defaultdict
import pathlib
import re

f = open(pathlib.Path(__file__).parent.absolute() / 'input.txt')

lines = [x.rstrip() for x in f.readlines()]

mask_string = ''
def apply(mask_mask, mask_value, value):
    global mask_string
    #print("mask: %s" % format(mask_mask, '036b'))
    #print("mval: %s" % format(mask_value, '036b'))
    #print("dest: %s" % format(value, '036b'))
    f = value & ~mask_mask
    #print("nand: %s" % format(f, '036b'))
    f = f | mask_value
    #print("res:  %s" % format(f, '036b'))
    #print()

    value_string = format(value, '036b')
    mask_value_string = format(mask_value, '036b')
    new_string = ''
    idx = 0
    for c in mask_string:
        if c == 'X':
            new_string += value_string[idx]
        else:
            new_string += mask_value_string[idx]
        idx += 1

    if (new_string != format(f, '036b')):
        print("nres: %s" % new_string)
        print(value)
        print("Hmm, something's wrong")
        exit(1)

    return f

sparse_memory_blob = {}
for line in lines:
    if not line:
        continue
    print(line)
    m = re.match(r'^mask = (.*)$', line)
    if m:
        # build mask and overlay
        mask_source = m.groups()[0]
        mask_string = mask_source
        mask_mask = int(mask_source.replace('0', '1').replace('X', '0'), 2)
        mask_value = int(mask_source.replace('X', '0'), 2)
        #print("mask: %s: %s, %s" % (mask_source, bin(mask_mask), bin(mask_value)))
    else:
        (location, value) = [int(x) for x in re.match(r'^mem\[([0-9]+)\] = ([0-9]+)$', line).groups()]
        #print("lv: %d, %d" % (location, value))
        sparse_memory_blob[location] = apply(mask_mask, mask_value, value)

print("Sparse blob: %s" % sparse_memory_blob)
print("Sum: %d" % sum(sparse_memory_blob.values()))
