import json
import re

f = open('input.txt')

code = []
idx = 0
ips_to_change = []
for l in f:
  l = l.rstrip()
  (instruction, direction, value) = re.match('^([a-z]{3}) (.)([0-9]+)$', l).groups()
  #print("%s %s%s" % (instruction, direction, value))
  code.append([idx, instruction, direction, int(value), False])
  if instruction != 'acc':
    ips_to_change.append(idx)
  idx += 1

#print(json.dumps(code, indent=2))

opposite = {'nop': 'jmp', 'jmp': 'nop'}

#print("IPs to change: %s" % (json.dumps(ips_to_change)))

for ip_to_change in ips_to_change:
  #print("Changing code at %d" % ip_to_change)
  accumulator = 0
  ip = 0
  for idx in range(0, len(code)):
    code[idx][4] = False

  while ip < len(code) and not code[ip][4]:
    (idx, instruction, direction, value, visited) = code[ip]

    if ip == ip_to_change:
      #print("!!! CHANGING %s to %s" % (instruction, opposite[instruction]))
      instruction = opposite[instruction]

    code[ip][4] = True
    if instruction == 'nop':
      ip += 1
    elif instruction == 'jmp':
      if direction == '+':
        ip += value
      else:
        ip -= value
    elif instruction == 'acc':
      if direction == '+':
        accumulator += value
      else:
        accumulator -= value
      ip += 1
    #print("New ip/accumulator: %d, %d" % (ip, accumulator))

  if ip == len(code):
    print('Success!')
    break
  else:
    pass
    #print('Loop detected, trying again.')

print("Accumulator at loop point: %d" % accumulator)