import copy

f = open('/Users/moishe/src/advent-of-code/day_11/input.txt')

board = []
y_size = 0
for l in f:
  x_size = len(l.rstrip())
  board.extend(list(l.rstrip()))
  y_size += 1

def idx_from_x_y(x, y):
  global x_size, y_size
  return y * x_size + x

def count_neighbors(x, y, board):
  global x_size, y_size
  c = 0
  for dx in [-1,0,1]:
    for dy in [-1,0,1]:
      if dx == 0 and dy == 0:
        continue
      # walk the board in this direction until you see something
      xx = x + dx
      yy = y + dy
      while xx >= 0 and xx < x_size and yy >= 0 and yy < y_size:
        v = board[idx_from_x_y(xx,yy)]
        if v == 'L':
          break
        if v == '#':
          c += 1
          break
        xx += dx
        yy += dy

  """
  previous algo  
  for dy in range(max(0, y - 1), min(y_size, y + 2)):
    for dx in range(max(0, x - 1), min(x_size, x + 2)):
      if dx == x and dy == y:
        continue
      idx = idx_from_x_y(dx, dy)
      if board[idx] == '#':
        c += 1
  """
  return c

def print_board_neighbor_count(board):
  global x_size, y_size
  for y in range(y_size):
    l = []
    for x in range(x_size):
      l.append(str(count_neighbors(x, y, board)))
    print("".join([str(x) for x in l]))

def dump_board(board):
  global x_size, y_size
  for y in range(y_size):
    row = []
    for x in range(x_size):
      row.append(board[idx_from_x_y(x, y)])
    print("".join([x.rjust(0) for x in row]))

def new_from_old(c, old_value):
  if old_value == 'L' and c == 0:
    return '#'

  if old_value == '#' and c >= 5:
    return 'L'
  
  return old_value

print("Dimensions: %d,%d" % (x_size, y_size))

stable = False
generations = 0
while not stable: # and generations < 5:
  #dump_board(board)
  #print_board_neighbor_count(board)
  new_board = []
  for y in range(y_size):
    for x in range(x_size):
      c = count_neighbors(x, y, board)
      new_board.append(new_from_old(c, board[idx_from_x_y(x,y)]))

  stable = board == new_board
  board = new_board
  generations += 1
  print("%d occupied seats after %d generations" % (board.count('#'), generations))

print("We're stable after %d generations, with %d occupied seats" % (generations, board.count('#')))