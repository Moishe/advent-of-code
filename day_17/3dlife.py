import time

xlat = {
    True: '#',
    False: '.'
}

def set_from_2d_grid(grid):
    board_set = set()
    y = 0
    for row in grid:
        x = 0
        for el in row:
            if el == '#':
                board_set.add((x,y,0,0))
            x += 1
        y += 1

    return board_set

def grid_from_set(board_set):
    elements = list(board_set)
    bounds = []
    for i in range(4):
        coordinates = [x[i] for x in elements]
        bounds.append([min(coordinates), max(coordinates) + 1])

    grid = []
    for w in range(bounds[3][0], bounds[3][1]):        
        w_slice = []
        for z in range(bounds[2][0], bounds[2][1]):
            z_slice = []
            for y in range(bounds[1][0], bounds[1][1]):
                row = []
                for x in range(bounds[0][0], bounds[0][1]):
                    row.append(xlat[(x,y,z,w) in board_set])
                z_slice.append(row)
            w_slice.append(z_slice)
        grid.append(w_slice)
    return grid

def cell_neighbors(cell):
    ns = set()

    for x in range(-1,2):
        for y in range(-1,2):
            for z in range(-1,2):
                for w in range(-1,2):
                    if x != 0 or y != 0 or z != 0 or w != 0:
                        ns.add((cell[0] + x, cell[1] + y, cell[2] + z, cell[3] + w))

    return ns

def all_neighbors(board_set):
    neighbor_set = set()
    for cell in list(board_set):
        neighbor_set.update(cell_neighbors(cell))
    return neighbor_set

def generation(board_set):
    to_evaluate = all_neighbors(board_set)
    new_board_set = set()

    for cell in list(to_evaluate):
        cn = cell_neighbors(cell)
        on = cn.intersection(board_set)
        n = len(on)
        if cell in board_set:
            if n == 2 or n == 3:
                new_board_set.add(cell)
        else:
            if n == 3:
                new_board_set.add(cell)

    return new_board_set

def print_board(board_set):
    grid = grid_from_set(board_set)
    for w_slice in grid:
        print("=== W ====")
        for z_slice in w_slice:
            print("  === Z ===")
            for row in z_slice:
                print("    %s" % ''.join(row))

test_board = set_from_2d_grid([
    '.#.',
    '..#',
    '###',
])

board = set_from_2d_grid([
    '..#..##.',
    '#.....##',
    '##.#.#.#',
    '..#...#.',
    '.###....',
    '######..',
    '.###..#.',
    '..#..##.'   
])

for i in range(15):
    start = time.time()
    #print("generation: %d" % (i + 1))
    board = generation(board)
    end = time.time()
    print("After %d generations: on: %d, duration: %s" % (i + 1, len(board), "{:.2f}".format(end - start)))
    #print_board(board)

print("On cells: %d" % len(board))