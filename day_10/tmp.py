import re

for p in range(2, 10):
  f = '0%db' % p
  skip = 0
  print("formatting %s" % f)
  for i in range(0,2 ** p):
    s = format(i, f)
    m = re.findall('000', s)
    if len(m):
      #print("*%s" % s)
      skip += 1
    else:
      pass
      #print(" %s" % s)

  print("%d,%d,%d" % (p, skip, (2**p)-skip))
