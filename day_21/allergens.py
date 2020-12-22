import json
import pathlib
import re

from collections import defaultdict

lines = [x.rstrip() for x in open(pathlib.Path(__file__).parent.absolute() / 'test_input.txt').readlines()]

all_allergens = set()
all_ingredients = set()
pairs = []
for line in lines:
    (ingredients, allergens) = re.match(r'^([a-z ]+) \(contains ([a-z, ]+)\)$', line).groups()
    ingredient_list = set(ingredients.split(' '))
    allergens_list = set(allergens.split(', '))
    pairs.append((ingredient_list, allergens_list))
    all_allergens.update(allergens_list)
    all_ingredients.update(ingredient_list)

ingredient_lines = [x[0].copy() for x in pairs]

ips = defaultdict(set)
aps = defaultdict(set)
while (ingredients, allergens) in pairs:
    for ingredient in ingredients:
        for allergen in allergens:
            ips[ingredient].add(allergen)
            aps[allergen].add(ingredient)

print(ips, aps)
exit(0)

new_pairs = []
for (idx, (ingredients, allergens)) in enumerate(pairs):
    for potential_match in range(idx, len(pairs)):
        (match_ingredients, match_allergens) = pairs[potential_match]
        ingredient_matches = ingredients.intersection(match_ingredients)
        allergen_matches = allergens.intersection(match_allergens)
        new_pairs.append((ingredient_matches, allergen_matches))

        print(len(ingredient_matches), len(allergen_matches))
        if len(ingredient_matches) == 1 and len(allergen_matches) == 1:
            ingredient = list(ingredient_matches)[0]
            allergen = list(allergen_matches)[0]
            print("%s contains %s" % (ingredient, allergen))
            all_ingredients.discard(ingredient)

            for pair in pairs:
                pair[0].discard(ingredient)
                pair[1].discard(allergen)
pairs = new_pairs

print(all_ingredients)

s = 0
for ingredient_line in ingredient_lines:
    s += len(ingredient_line.intersection(all_ingredients))

print("%d appearances" % s)