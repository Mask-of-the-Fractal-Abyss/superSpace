from copy import deepcopy

class space:
  def __init__(self, boardsize=10):
    self.boardsize = boardsize
    self.board = [[None for _ in range(boardsize)] for _ in range(boardsize)]

  def prettyPrint(self):
    emptyChar = '.'
    spaceChar = ' '
    for row in self.board:
      for obj in row:
        if obj is None:
          print(emptyChar, end=spaceChar)
        else:
          print(obj.symbol, end=spaceChar)
      print()

  def updateBoard(self):
    copy = deepcopy(self.board)
    newLocs = []
    for y in range(len(copy)):
      for x in range(len(copy[0])):
        newLocs.append([y, x] + copy[y][x].projectedLocation(y, x))
    for loc1 in newLocs:
      for loc2 in newLocs:
        if [loc1[2], loc1[3]] == [loc2[2], loc2[3]]:


class boardObject:
  def __init__(self, weaknesses, xdelta=0, ydelta=0, mass=1):
    self.xdelta = xdelta
    self.ydelta = ydelta
    self.mass = mass
    self.weaknesses = weaknesses

  def weakTo(self, obj):
    return type(obj) in self.weaknesses

  def projectedLocation(self, yloc, xloc):
    return [yloc + self.deltay, xloc + self.deltax]

  @property
  def moving(self):
    return xdelta == 0 and ydelta == 0

class laser(boardObject):
  def __init__(self):
    super().__init__(weaknesses=[laser, planet, ship])

class planet(boardObject):
  def __init__(self):
    super().__init__(weaknesses=[laser])

class ship(boardObject):
  def __init__(self):
    super().__init__(weaknesses=[laser, planet])
    self.direction = 0  # 0, 1, 2, 3 = NESW
    self.thrust = 2

  def accelerate(self):
    d = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    self.xdelta += d[self.direction][0]
    self.ydelta += d[self.direction][1]

  def rotate(self, cw=1):  # cw = 1, ccw = -1
    self.direction = (self.direction + cw) % 4

  @property
  def symbol(self):
    return ['^', '>', 'v', '<'][self.direction]

board = space()
player = ship()
board.board[0][0] = player
board.prettyPrint()
player.rotate()
board.prettyPrint()
from copy import deepcopy

class space:
  def __init__(self, boardsize=10):
    self.boardsize = boardsize
    self.board = [[None for _ in range(boardsize)] for _ in range(boardsize)]

  def prettyPrint(self):
    emptyChar = '.'
    spaceChar = ' '
    for row in self.board:
      for obj in row:
        if obj is None:
          print(emptyChar, end=spaceChar)
        else:
          print(obj.symbol, end=spaceChar)
      print()

  def updateBoard(self):
    copy = deepcopy(self.board)
    newLocs = []
    for y in range(len(copy)):
      for x in range(len(copy[0])):
        newLocs.append([y, x] + copy[y][x].projectedLocation(y, x))
    for loc1 in newLocs:
      for loc2 in newLocs:
        if [loc1[2], loc1[3]] == [loc2[2], loc2[3]] and loc1 is not loc2:
		  if loc1.weakTo(loc2):
		    copy[loc1[0]][loc1[1]] = None
		  if loc2.weakTo(loc1):
		    copy[loc2[0]][loc2[1]] = None
		  elif not loc1.weakTo(loc2) and not loc2.weakTo(loc1):
		    copy[loc2[0]][loc2[1]] = None
		    copy[loc1[0]][loc1[1]] = None
	self.board = copy

class boardObject:
  def __init__(self, weaknesses, xdelta=0, ydelta=0, mass=1):
    self.xdelta = xdelta
    self.ydelta = ydelta
    self.mass = mass
    self.weaknesses = weaknesses

  def weakTo(self, obj):
    return type(obj) in self.weaknesses

  def projectedLocation(self, yloc, xloc):
    return [yloc + self.deltay, xloc + self.deltax]

  @property
  def moving(self):
    return xdelta == 0 and ydelta == 0

class laser(boardObject):
  def __init__(self):
    super().__init__(weaknesses=[laser, planet, ship])

class planet(boardObject):
  def __init__(self):
    super().__init__(weaknesses=[laser])

class ship(boardObject):
  def __init__(self):
    super().__init__(weaknesses=[laser, planet])
    self.direction = 0  # 0, 1, 2, 3 = NESW
    self.thrust = 2

  def accelerate(self):
    d = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    self.xdelta += d[self.direction][0]
    self.ydelta += d[self.direction][1]

  def rotate(self, cw=1):  # cw = 1, ccw = -1
    self.direction = (self.direction + cw) % 4

  @property
  def symbol(self):
    return ['^', '>', 'v', '<'][self.direction]

board = space()
player = ship()
board.board[0][0] = player
board.prettyPrint()
player.rotate()
board.prettyPrint()
