f = open('input.txt')
i = 0
for l in f:
  print('  rgchInput[%d] = "%s";' % (i, l.rstrip()))
  i += 1
