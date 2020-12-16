from collections import defaultdict
input = [18,8,0,5,4,1,20]

test_inputs = [
    [[1,3,2], 1],
    [[2,1,3], 10],
    [[1,2,3], 27],
    [[2,3,1], 78],
    [[3,2,1], 438],
    [[3,1,2], 1836]
]

def number_at_idx(seed, at_idx):
    last_seen_idx = defaultdict(list)
    idx = 0
    for n in seed:
        last_seen_idx[n] = [idx]
        idx += 1
        prev = n

    while idx < at_idx:
        if len(last_seen_idx[prev]) == 1:
            n = 0
        else:
            n = last_seen_idx[prev][-1] - last_seen_idx[prev][-2]

        last_seen_idx[n].append(idx)
        if len(last_seen_idx[n]) > 2:
            last_seen_idx[n].pop(0)
        prev = n
        idx += 1

    return prev
"""
for input in test_inputs:
    result = number_at_idx(input[0], 30000000)
    print("Expected: %d, actual: %d" % (result, input[1]))
"""
print(number_at_idx(input, 30000000))