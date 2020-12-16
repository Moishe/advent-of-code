import json
import pathlib
import re

restrictions = [
    'class: 1-3 or 5-7',
    'row: 6-11 or 33-44',
    'seat: 13-40 or 45-50',
]

restrictions = [
    'class: 0-1 or 4-19',
    'row: 0-5 or 8-19',
    'seat: 0-13 or 16-19'
]

your_ticket = '7,1,14'
your_ticket = '11,12,13'

nearby_tickets = [
    '7,3,47',
    '40,4,50',
    '55,2,20',
    '38,6,12',
]
nearby_tickets = [
    '3,9,18',
    '15,1,5',
    '5,14,9'
]
restrictions = [x.rstrip() for x in open(pathlib.Path(__file__).parent.absolute() / 'restrictions.txt').readlines()]
your_ticket = open(pathlib.Path(__file__).parent.absolute() / 'your_ticket.txt').readlines()[0].rstrip()
nearby_tickets = open(pathlib.Path(__file__).parent.absolute() / 'nearby_tickets.txt').readlines()

restriction_regex = r'^([a-z ]+): ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)$'

restrictions_dict = {}

for line in restrictions:
    m = re.match(restriction_regex, line)
    if m:
        restrictions_dict[m.group(1)] = [int(x) for x in m.groups()[1:]]
    else:
        print("hmm, can't parse %s" % line)
        exit(1)

def satisfies(restrictions, value):
    return (value >= restrictions[0] and value <= restrictions[1]) or (value >= restrictions[2] and value <= restrictions[3])

def get_possibilities(ticket):
    global restrictions_dict
    possibilities = []
    for i in range(len(ticket)):
        possibilities.append(set(restrictions_dict.keys()))

    # for each possibility, remove the possibility that if it doesn't satisfy your ticket
    for i in range(len(ticket)):
        for (c, r) in restrictions_dict.items():
            if not satisfies(r, ticket[i]):
                print("  no: %d satisfies %s (%s)" % (ticket[i], r, c))
                possibilities[i].discard(c)
            else:
                print(" yes: %d satisfies %s (%s)" % (ticket[i], r, c))

    return possibilities

your_ticket_values = [int(x) for x in your_ticket.split(',')]

global_possibilities = []
for i in range(len(your_ticket_values)):
    global_possibilities.append(set(restrictions_dict.keys()))

r = 0
for ticket in nearby_tickets:
    ticket_values = [int(x) for x in ticket.split(',')]
    p = get_possibilities(ticket_values)

    is_valid_ticket = True
    for i in range(len(ticket_values)):
        if p[i] == set():
            is_valid_ticket = False
            break

    if is_valid_ticket:
        print(p)
        # intersect all the sets
        for i in range(len(p)):
            global_possibilities[i] &= p[i]

in_doubt = True
while in_doubt:
    in_doubt = False
    print("===")
    for i in range(len(global_possibilities)):
        if len(global_possibilities[i]) == 1:
            print("%s is unambiguous" % global_possibilities[i])
            for j in range(0, len(global_possibilities)):
                if i != j:
                    global_possibilities[j].discard(list(global_possibilities[i])[0])
        else:
            #print("%s is ambiguous (%d)" % (global_possibilities[i], len(global_possibilities[i])))
            in_doubt = True

result = 1
for i in range(len(global_possibilities)):
    c = list(global_possibilities[i])[0]
    if c.startswith('departure'):
        print("%s: %d" % (c, your_ticket_values[i]))
        result *= your_ticket_values[i]

print(result)