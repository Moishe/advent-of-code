import json
import pathlib
import re

input = [
    '0: 4 1 5',
    '1: 2 3 | 3 2',
    '2: 4 4 | 5 5',
    '3: 4 5 | 5 4',
    '4: "a"',
    '5: "b"',
]
"""
input = [
    '0: 1 2',
    '1: "a"',
    '2: 1 3 | 3 1',
    '3: "b"'
]
"""

input = [
    '0: 1 2',
    '1: 3 1 2 | 3 2',
    '2: "a"',
    '3: "b"',
]
def array_from_rule(rule):
    rule_array = []
    clauses = rule.split('|')
    for clause in clauses:
        clause_array = []
        elements = clause.split(' ')
        for el in elements:
            if el:                
                clause_array.append(eval(el))
        rule_array.append(clause_array)

    return rule_array

def expand_rule(rule, rule_idx, rule_map):
    new_rule = []
    for clause in rule:
        new_clause = []
        for el in clause:
            if type(el) is int:
                if el == rule_idx:
                    new_el = "[!]"
                else:
                    new_el = expand_rule(rule_map[el], el, rule_map)
            else:
                new_el = el
            new_clause.append(new_el)
        new_rule.append(new_clause)
    if len(new_rule) == 1 and len(new_rule[0]) == 1:
        return new_rule[0][0]
    return new_rule

def match(s, ruleset, parent, depth=0):
    print("%s Trying to match %s to %s" % (' ' * depth, s, ruleset))
    idx = 0
    matches = False
    if type(ruleset[0]) == list:
        for el in ruleset:
            print("%s OR %s / %s" % (' ' * depth, el,s))
            matches |= match(s[idx:], el, ruleset, depth + 1)
    else:
        for el in ruleset:
            print("%s AND %s / %s" % (' ' * depth, el,s[idx]))

            if el == '[!]':
                print("%s Recursing" % (' ' * depth))
                if not match(s[idx:], parent, None, depth + 1):
                    return False
                #print("felt recursive, might delete later %s, %s, %s" % (m, s[idx:], ruleset))
                # not sure what to *do* with this
            elif s[idx] != el:                
                return False
            idx += 1

    return matches

rule_map = {}

#f = open(pathlib.Path(__file__).parent.absolute() / 'rules.txt')
#input = [x.rstrip() for x in f.readlines()]

for line in input:
    m = re.match(r'^([0-9]+): (.+)$', line)
    (rule_number, rule) = m.groups()
    rule_map[int(rule_number)] = array_from_rule(rule)

print(json.dumps(rule_map, indent=1))

expanded_ruleset = expand_rule(rule_map[0], 0, rule_map)
print(expanded_ruleset)

print(match('bbaaa', expanded_ruleset, None))
exit(1)

f = open(pathlib.Path(__file__).parent.absolute() / 'testlines.txt')
testlines = [x.rstrip() for x in f.readlines()]
