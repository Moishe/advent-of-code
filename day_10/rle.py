import re

f = open('input.txt')

sequence = []
for l in f:
  sequence.append(int(l.rstrip()))

sequence.sort()
sequence.append(max(sequence) + 3)
print(sequence)

prev = 0
sequences = []
sequence_length = 0
for i in sequence:
  if i == prev + 1:
    in_sequence = True
    sequence_length += 1
  else:
    in_sequence = False
    sequences.append(sequence_length)
    sequence_length = 0
  prev = i

sequences = [x - 1 for x in sequences]
sequences = list(filter(lambda x: x > 0, sequences))
print(sequences)

m = max(sequences)
translate_table = {}
for p in range(1, m + 1):
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
  translate_table[p] = (2 ** p) - skip

print(translate_table)
r = 1
for i in sequences:
  print("Multiplying %d by %d (translated from %d)" % (r, translate_table[i], i))
  r *= translate_table[i]

print("The result is %d" % r)