f = open('input.txt')

steps = []
for l in f:
  steps.append(int(l.rstrip()))

mx = max(steps) + 3
c = len(steps) + 1

print ("a + 3b = %d" % mx)
print ("a + b = %d" % c)

b = (mx - c) / 2
print ("b = (%d - %d) / 2 = %d" % (mx, c, b))

a = c - b
print ("a = %d - %d = %d" % (c, b, a))

print("Solution: a * b = %d" % (a * b))