import json
import pathlib
import re

from collections import defaultdict

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
    '0: 2 1 4 3',
    '1: 3 1 | 3 2',
    '4: 5 | 5 4',
    '5: 2',
    '2: "a"',
    '3: "b"',
]
testlines = [
    'abab',
    'abbbab'
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
    new_rule = ['or']
    for clause in rule:
        new_clause = ['and']
        for el in clause:
            if type(el) is int:
                if el == rule_idx:
                    new_el = el
                else:
                    new_el = expand_rule(rule_map[el], el, rule_map)
            else:
                new_el = el
            new_clause.append(new_el)
        new_rule.append(new_clause)
    if len(new_rule) == 1 and len(new_rule[0]) == 1:
        return new_rule[0][0]
    return new_rule

def debug_print(s):
    #print(s)
    pass

def match_2(s, idx, ruleset, depth=0):
    global expanded_ruleset

    debug_print("%s Matching %s against %s" % (' ' * depth, s[idx:], ruleset))

    matches = False
    local_ruleset = ruleset.copy()
    operation = local_ruleset.pop(0)
    if operation == 'or':
        for el in local_ruleset:
            debug_print("%s Checking: %s %s" % (' ' * depth, el, s))
            if type(el) is str:
                if el == s[idx]:
                    return (True, idx + 1)
            elif type(el) is int:
                print("Okay I dunno now")
                exit(1)
            else:
                (new_match, new_idx) = match_2(s, idx, el, depth + 1)
                if new_match:
                    return (True, new_idx)
        return (matches, idx)
    else:
        for el in local_ruleset:
            if type(el) is str:
                if idx >= len(s):
                    return (False, 0)
                if not el == s[idx]:
                    debug_print("%s Matches (%s, %s)" % (' ' * depth, False, el))
                    return (False, idx)
                idx += 1
            elif type(el) is int:
                print("Recursing: %d" % (idx))
                (new_match, new_idx) = match_2(s, idx, expanded_ruleset[el], depth + 1)
                print("Done recursing: %s: %d,%d" % (new_match, new_idx, idx))
                if not new_match:
                    debug_print("%s Matches (%s, %s)" % (' ' * depth, False, el))
                    return (False, idx)
                else:
                    idx = new_idx
            else:
                (new_match, new_idx) = match_2(s, idx, el, depth + 1)
                if not new_match:
                    debug_print("%s Matches (%s, %s)" % (' ' * depth, False, el))
                    return (False, idx)
                else:
                    idx = new_idx
        return (True, idx)

"""
testlines = [
    'ababbb',
    'bababa',
    'abbbab',
    'aaabbb',
    'aaaabbb',
]
"""
f = open(pathlib.Path(__file__).parent.absolute() / 'test-rules.txt')
input = [x.rstrip() for x in f.readlines()]

f = open(pathlib.Path(__file__).parent.absolute() / 'test-lines.txt')
testlines = [x.rstrip() for x in f.readlines()]

testlines = [
    'babbbbaabbbbbabbbbbbaabaaabaaa'
]

rule_map = {}

for line in input:
    m = re.match(r'^([0-9]+): (.+)$', line)
    (rule_number, rule) = m.groups()
    rule_map[int(rule_number)] = array_from_rule(rule)

expanded_ruleset = defaultdict(list)
for (idx, rule) in rule_map.items():
    expanded_ruleset[idx] = expand_rule(rule, 0, rule_map)

total = 0
for testline in testlines:
    (result, idx) = match_2(testline, 0, expanded_ruleset[0])
    matches = result and idx == len(testline)
    if matches:
        total += 1
    print("%s: %s (%d, %d)" % (testline, matches, idx, len(testline)))

print("Total: %d" % total)