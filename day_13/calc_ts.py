import pathlib

f = open(pathlib.Path(__file__).parent.absolute() / 'input.txt')

lines = f.readlines()

ts = int(lines[0].rstrip())
in_service = [int(x) for x in filter(lambda x: x != 'x', lines[1].rstrip().split(','))]
mods = [(x - (ts % x), x) for x in in_service]
mods.sort()
print("Answer: %d" % (mods[0][0] * mods[0][1]))
for bus in in_service:
  print("%d: %d" % (bus, bus - (ts % bus)))