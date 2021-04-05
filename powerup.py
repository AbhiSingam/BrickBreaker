import numpy as np
from time import time
import config as C

class Powerup:
    def __init__ (self, x, y, board, type, vx, vy):
        self.x = int(x)
        self.y = int(y)
        self.ded = False
        self.type = type
        self.vx = int(vx)
        self.vy = int(vy)
        board.pp[self.y][self.x] = self.type
    
    def fall(self, board, paddle):
        if not self.ded:
            
            board.pp[self.y][self.x] = ''

            self.x = self.x + self.vx
            self.y = self.y + self.vy


            # check wall collisions

            if (self.x < 0):
                self.x = 0
                self.vx = -1*self.vx
            elif (self.x >= board.width):
                self.x = board.width - 1
                self.vx = -1*self.vx
            
            if (self.y < 0):
                self.y = 0
                self.vy = -1*self.vy

            if 0 <= self.x < board.width and 0 <= self.y < board.height-1:
                board.pp[self.y][self.x] = self.type
            elif self.y >= board.height-1:
                self.ded = True

            if C.ticks % 4 == 0:
                self.vy += 1

            if self.x >= paddle.x and self.x < paddle.x + paddle.width and self.y >= paddle.y:
                if self.type == 's':
                    C.shoot['active'] = True
                    C.shoot['time'] = time()
                elif self.type == 'f':
                    C.fireball = True
                self.ded = True

            elif self.y >= board.height:
                # Failed to catch powerup
                self.ded = True

def move_powerups(board, paddle):
    for pup in C.powerups:
        if not pup.ded:
            pup.fall(board, paddle)
