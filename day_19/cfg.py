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

clause_count = 0
clauses_with_recursion = []
def ruleset_to_regex(ruleset):
    global clause_count, clauses_with_recursion
    print("Parsing: %s" % (ruleset))
    regex_clauses = []
    for clause in ruleset:
        next_el_plus = False
        regex = ""
        for el in clause:
            if type(el) is list:
                regex += ruleset_to_regex(el)
            elif el == '[!]':
                regex += '+'
                next_el_plus = True
                clauses_with_recursion.append(clause_count)
            else:
                regex += el
                if next_el_plus:
                    regex += '+'
                    next_el_plus = False
        clause_count += 1
        regex_clauses.append(regex)

    return "(" + "|".join(regex_clauses) + ")"

def match(s, ruleset):
    print("Trying to match %s to %s" % (s, ruleset))
    idx = 0
    matches = False
    for el in ruleset:
        print("%s / %s" % (el,s[idx]))
        if type(el) == list:
            print("It's an or clause, checking %s" % el)
            matches |= match(s[idx:], el)
        else:
            print("It's a sequence of characters, checking %s" % el)
            if el == '[!]':
                print("Recursing")
                if not match(s[idx:], ruleset):
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

print(match('bbaaa', expanded_ruleset))
exit(1)
regex = "^" + ruleset_to_regex(expanded_ruleset) + "$"
print(regex)

f = open(pathlib.Path(__file__).parent.absolute() / 'testlines.txt')
testlines = [x.rstrip() for x in f.readlines()]

#testlines = ['bbaaa', 'babaa', 'bbbaaaa']
matches = 0
print(clauses_with_recursion)
for line in testlines:
    m = re.match(regex, line)
    if m:
        matches += 1
 #       print("%s matches (%s)" % (line, [str(x) for x in m.groups()]))
 #   else:
 #       print("%s does not match" % line)

print("%d match" % matches)