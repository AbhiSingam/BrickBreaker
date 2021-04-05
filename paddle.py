import config as C
from brick import *

class Paddle:
    def __init__(self, board):
        self.width = int(board.width / 3)
        # self.width = board.width
        self.x = int(board.width / 3)
        # self.x = 0
        self.y = board.height - 1
    
    def move(self, disp, board, ball, ufo):
        balldis = ball.x-self.x
        old_x = self.x
        self.x += disp*3
    
        if self.x + self.width > board.width:
            self.x = board.width - self.width
        elif self.x < 0:
            self.x = 0
        
        if ball.attach:
            ball.x = self.x + balldis

        ufo.move(self.x - old_x, board)

class Laser:
    def __init__(self, board, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 1
        board.lasers[y][x] = '|'
        self.ded = False

    def move(self, board, bricks):
        self.y -= self.vy
        if self.y < 0:
            board.lasers[self.y + 1][self.x] = ''
            self.ded = True
        elif board.bp[self.y][self.x] < 0:
            board.lasers[self.y + 1][self.x] = ''
            board.lasers[self.y][self.x] = '|'
        else:
            bricks[board.bp[self.y][self.x]].hit(board, bricks, self)
            board.lasers[self.y + 1][self.x] = ''
            self.ded = True  

class UFO (Paddle):
    def __init__(self, board):
        self.width = self.width = int(board.width / 3) - 4
        self.x = int(board.width / 3) + 2
        self.y = 0
        self.health = C.boss_health

    def move(self, disp, board):
        self.x += disp

        if self.x + self.width > board.width:
            self.x = board.width - self.width
        elif self.x < 0:
            self.x = 0
    
    def drop_bomb(self, board):
        C.bombs.append(Bomb(board, self.x + (self.width//2), self.y + 1))

    def spawn_bricks(self, board, bricks):
        for i in range(6):
            bricks.append(Brick(1, 5*i, self.health, len(bricks), board))
            bricks.append(Brick(1, board.width - 5 * (i+1), self.health , len(bricks), board))


class Bomb:
    def __init__(self, board, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = -1
        board.bombs[y][x] = 'V'
        self.ded = False

    def move(self, board, paddle):
        self.y -= self.vy
        if self.y >= board.height:
            board.bombs[self.y - 1][self.x] = ''
            self.ded = True
        elif self.y == paddle.y and self.x >= paddle.x and self.x < paddle.x + paddle.width:
            board.bombs[self.y - 1][self.x] = ''
            self.ded = True
            return -1
        else:
            board.bombs[self.y - 1][self.x] = ''
            board.bombs[self.y][self.x] = 'V'
        return 0
