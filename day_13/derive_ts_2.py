import pathlib

offsets = [7,13, 19]
offsets = [17,'x',13,19]
#offsets = [2,3,5]
offsets = [67,7,'x',59,61]
offsets = [1789,37,47,1889]
x = 'x'
offsets = [17,x,x,x,x,x,x,x,x,x,x,37,x,x,x,x,x,409,x,29,x,x,x,x,x,x,x,x,x,x,13,x,x,x,x,x,x,x,x,x,23,x,x,x,x,x,x,x,373,x,x,x,x,x,x,x,x,x,41,x,x,x,x,x,x,x,x,19]
indexed_offsets = []
i = 0
for o in offsets:
  if o != 'x':
    indexed_offsets.append((int(o), i % int(o)))
    print("At a multiple of %d I need a remainder of %d" % indexed_offsets[-1])
  i += 1

print(indexed_offsets)
indexed_offsets.reverse()

product = 1
for x in indexed_offsets:
  product *= x[0]
print("Product: %d" % product)
print(indexed_offsets)
multiplier = 1
idx = 0
(step, offset) = indexed_offsets[0]
ts = step - offset
while (ts < 0):
  print(ts)
  ts += step
operations = 0
prev_pct_done = None
for index in range(1, len(indexed_offsets)):
  (n, a) = indexed_offsets[index]
  print("Now searching for %d with a remainder of %d starting at %d, stepping by %d" % (n, a, ts, step))
  while True:
    #print("%d (%d, %d)" % (ts, n, a))
    m = (n - ts % n) % n
    if m == a:
      print("Found %d" % ts)
      step *= n
      break
    ts += step
    if ts > product:
      print("Something's gone wrong, I'm past the product")
      exit(1)
    operations += 1 
    pct_done = round(ts / product * 100, 0)
    if (pct_done != prev_pct_done):
      print("%d" % pct_done)
    prev_pct_done = pct_done

print("Calculated in %d operations" % operations)