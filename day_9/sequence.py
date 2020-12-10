import copy
import json
from collections import defaultdict

f = open('input.txt')

window = []
window_size = 25

def calc_map_sums(window):
  map_sums = [[]] * (window_size - 1)
  for i in range(0, window_size):      
    for j in range(0, i):
      map_sums[j].append(window[i] + window[j])
  return map_sums

idx = 0
map_sums = None
for l in f:
  v = int(l.rstrip())
  if idx > window_size:
    values = [item for sublist in map_sums for item in sublist]

    if v not in values:
      print("Unfound %d at %d" % (v, idx))
      exit(1)

  window.append(int(v))
  #print(window)
  if len(window) == window_size:
    if map_sums:
      map_sums.pop(0)
      map_sums.append([])
      i = 0
      for s in map_sums:
        s.append(window[i] + window[-1])
        i += 1
    else:
      map_sums = calc_map_sums(window)

    print(map_sums)
    print(window)

    window.pop(0)

  idx += 1
