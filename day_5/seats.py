from functools import reduce

def seat_to_id(seat):
  print(seat)
  return int(seat.replace('B', '1').replace('F', '0').replace('R', '1').replace('L', '0'), 2)

f = open('input.txt')
values = []
for l in f:
  values.append(l.rstrip())

for z in range(0, 100000):
  ids = [int(x.replace('B', '1').replace('F', '0').replace('R', '1').replace('L', '0'), 2) for x in values]

  min_id = min(ids)
  max_id = max(ids)
  acc_idx = reduce(lambda x,y: x ^ y, range(min_id, max_id+1))
  acc = reduce(lambda x,y: x ^ y, ids)
"""
ids.sort()
prev = -1
acc = 0
first = ids[0]
last = ids[:-1]
for id in ids:
  if prev != -1 and prev != id - 1:
    print("It's probably %d" % (id -1))
  acc = acc ^ id
  prev = id
"""