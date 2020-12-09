f = open('input.txt')

seats = None
sum = 0
for l in f:
  l = l.rstrip()
  if l:
    if seats == None:
      seats = set(l)
    else:
      seats = seats.intersection(set(l))
  else:
    sum += len(seats)
    seats = None

sum += len(seats)

print("Looks like %d" % sum)