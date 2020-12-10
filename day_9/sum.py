import copy
import json
from collections import defaultdict

f = open('input.txt')
target = 1309761972

#f = open('test_input.txt')
#target = 127

first = 0
window = []
total = 0
for l in f:
  d = int(l.rstrip())
  total += d
  window.append(d)
  while total > target and len(window) > 1:
    total -= window.pop(0)

  if (total == target):
    print("Found it: %s" % window)
    print("solution is %d" % (min(window) + max(window)))
    exit(1)
