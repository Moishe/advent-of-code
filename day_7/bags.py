import json
import re

from collections import defaultdict

def canonical_bag(bag):
  return bag.replace('bags', 'bag')

f = open('input.txt')
matcher = re.compile('^(.*) contain (.*)$')
contained_matcher = re.compile(' ?([0-9]+) ([^\.]+)\.?')

should_log = [
  #'contained_by', 
  'contains']

reverse_lookup = defaultdict(list)
container_lookup = defaultdict(list)

for l in f:
  l = l.rstrip()
  m = matcher.match(l)
  if m:
    container = canonical_bag(m.group(1))
    contains = m.group(2).split(',')
    contained_bags = {}
    for contained in contains:
      m = contained_matcher.match(contained)
      if m:
        quantity = int(m.group(1))
        bag = canonical_bag(m.group(2))
        contained_bags[bag] = quantity
        reverse_lookup[bag].append(container)
      else:
        if contained != 'no other bags.':
          print("Didn't match %s" % contained)
    container_lookup[container] = contained_bags
  else:
    print("Didn't match %s" % l)

def log_depth(depth, s, f):
  global should_log
  if f in should_log:
    print("%s %s" % (' ' * depth, s))

def bags_can_contain(bag, current_set=set(), depth=0):
  bag = canonical_bag(bag)
  log_depth(depth, "Looking for %s" % bag, 'contained_by')
  if bag not in reverse_lookup:
    log_depth(depth, "Nothing can contain %s" % bag,  'contained_by')
    return current_set
  else:
    log_depth(depth, "%s can contain %s" % (json.dumps(reverse_lookup[bag]), bag), 'contained_by')
    for container in reverse_lookup[bag]:
      current_set.add(container)
      current_set = current_set.union(bags_can_contain(container, current_set, depth + 1))
    log_depth(depth, "list: %s" % (json.dumps(list(current_set))),  'contained_by')
    return current_set

def bag_must_contain(bag, depth=0):
  if not container_lookup[bag]:
    log_depth(depth, "%s contains nothing else" % bag, 'contains')
    return 0

  total = 0
  log_depth(depth, "Checking %s" % bag, 'contains')
  for must_contain in container_lookup[bag]:
    log_depth(depth, "Must contain %d %s" % (container_lookup[bag][must_contain], must_contain), 'contains')
    bags_and_children = container_lookup[bag][must_contain] * (1 + bag_must_contain(must_contain, depth + 1))
    total += bags_and_children
    log_depth(depth, "That's %d bags and children" % bags_and_children, 'contains')
  log_depth(depth, "Final Total: %d" % total, 'contains')
  return total


bag = 'shiny gold bag'
containing_bags = bags_can_contain(bag)
print("%d bags can contain %s" % (len(containing_bags), bag))

print(json.dumps(container_lookup, indent=2))
contained_bags = bag_must_contain(bag)
print("%s bag must contain %d other bags" % (bag, contained_bags))