from copy import deepcopy
import random


class space:
    def __init__(self, boardsize=20):
        self.boardsize = boardsize
        self.board = [[None for _ in range(boardsize)] for _ in range(boardsize)]
        for _ in range(3):
            ry = random.randint(0, boardsize // 2)
            rx = random.randint(0, boardsize // 2)
            self.board[ry][rx] = planet()
            self.board[boardsize - ry - 1][boardsize - rx - 1] = planet()

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
        for y in range(self.boardsize):
            for x in range(self.boardsize):
                if copy[y][x] is not None:
                    newLocs.append([y, x] + copy[y][x].projectedLocation(y, x))
        for loc1 in newLocs:
            collision = False
            for loc2 in newLocs:
                if loc1[2:] == loc2[2:] and loc1 != loc2:
                    print('aowidnoaiw')
                    obj1 = self.board[loc1[0]][loc1[1]]
                    obj2 = self.board[loc2[0]][loc2[1]]
                    self.board[loc2[0]][loc2[1]] = None
                    if obj1.weakTo(obj2):
                        self.board[loc1[2]][loc1[3]] = obj2
                    collision = True
            if not collision:
                obj = self.board[loc1[0]][loc1[1]]
                self.board[loc1[0]][loc1[1]] = None
                if 0 <= loc1[2] < self.boardsize and 0 <= loc1[3] < self.boardsize:
                    self.board[loc1[2]][loc1[3]] = obj

    def printAndUpdate(self):
        self.prettyPrint()
        self.updateBoard()


class boardObject:
    def __init__(self, weaknesses, ydelta=0, xdelta=0, mass=1):
        self.xdelta = xdelta
        self.ydelta = ydelta
        self.mass = mass
        self.weaknesses = weaknesses

    def weakTo(self, obj):
        return type(obj) in self.weaknesses

    def projectedLocation(self, yloc, xloc):
        return [yloc + self.ydelta, xloc + self.xdelta]

    @property
    def isMoving(self):
        return not (self.xdelta == 0 and self.ydelta == 0)


class laser(boardObject):
    def __init__(self, ydelta, xdelta):
        super().__init__(weaknesses=[laser, planet, ship], ydelta=ydelta, xdelta=xdelta)
        self.symbol = '+'


class planet(boardObject):
    def __init__(self):
        super().__init__(weaknesses=[laser])
        self.symbol = 'O'


class ship(boardObject):
    def __init__(self):
        super().__init__(weaknesses=[laser, planet])
        self.direction = 0  # 0, 1, 2, 3 = NESW
        self.thrust = 2

    def accelerate(self):
        d = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        self.ydelta += d[self.direction][0]
        self.xdelta += d[self.direction][1]

    def fireLaser(self, b):
        y, x = self.findSelf(b)
        up = self.direction % 2
        right = (self.direction + 1) % 2
        if y + up < b.boardsize and x + right < b.boardsize:
            b.board[y + up][x + right] = laser(self.ydelta + up, self.xdelta + right)
        if x - right >= 0 and y - up >= 0:
            b.board[y - up][x - right] = laser(self.ydelta - up, self.xdelta - right)

    def findSelf(self, b):
        for y in range(b.boardsize):
            for x in range(b.boardsize):
                if b.board[y][x] == self:
                    return y, x
        return None

    def rotate(self, cw=1):  # cw = 1, ccw = -1
        self.direction = (self.direction + cw) % 4

    def printStats(self):
        print(self.ydelta, self.xdelta, self.direction)

    @property
    def symbol(self):
        return ['^', '>', 'v', '<'][self.direction]


board = space()

p = ship()
board.board[0][0] = p

while True:
    p.printStats()
    board.printAndUpdate()
    action = input()
    if action == 'a':
        p.accelerate()
    elif action == 'r':
        direction = len(input('dir')) % 2 * -2 + 1  # Response of even length = 1, otherwise equal to -1
        p.rotate(direction)
    elif action == 'f':
        p.fireLaser(board)
