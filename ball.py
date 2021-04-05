import numpy as np
from time import sleep
import config as C
from sound import play_bump

class Ball:
    def __init__ (self, paddle, pup, ball = None):
        if pup:
            self.x = ball.x
            self.y = ball.y
            self.vy = ball.vy
            self.vx = -1*ball.vx
            self.rx = 0
            self.ry = 0
            self.attach = False
            self.throughball = False
            self.ded = False
        
        else:
            self.x = int(paddle.x + np.random.randint(paddle.width))
            self.y = paddle.y - 1
            self.vy = 0
            self.vx = 0
            self.rx = 0
            self.ry = 0
            self.attach = True
            self.throughball = False
            self.ded = False

    def move (self, paddle, board, bricks, ufo):
        if self.vy != 0 and (not self.ded):
            if self.rx==0 and self.ry==0:
                self.x += self.vx
                self.y -= self.vy
                self.rx = self.vx
                self.ry = self.vy
            # print(str(self.ry) + " " + str(self.vy)


            if self.y - self.vy + self.ry >= board.height - 1:
                self.ded = True
            elif self.rx > self.vx/2 or self.ry==0:
                if not self.collCheckX(paddle, board, np.sign(self.vx), bricks, ufo):
                    self.rx -= np.sign(self.vx)            
            else:
                if not self.collCheckY(paddle, board, np.sign(self.vy), bricks, ufo):
                    self.ry -= np.sign(self.vy)



    def release (self):
        self.vx = 0
        self.vy = 1
        self.rx = self.vx 
        self.ry = self.vy
        self.attach = False

    def collCheckX (self, paddle, board, vel, bricks, ufo):
        endpoint = self.x + self.vx - self.rx + vel
        if endpoint < 0:
            self.x = 0
            self.y = self.y - self.vy + self.ry
            self.vx = -1*self.vx
            self.rx = self.vx
            self.ry = self.vy
            play_bump()
            # self.rx += np.sign(self.vx)
            return True
        elif endpoint >= board.width:
            self.x = board.width - 1
            self.y = self.y - self.vy + self.ry
            self.vx = -1*self.vx
            self.rx = self.vx
            self.ry = self.vy
            play_bump()
            # self.rx += np.sign(self.vx)
            return True

        elif (not self.throughball) and board.bp[int(self.y - self.vy + self.ry)][int(endpoint)] >= 0:
            # print("block_ind: " + str(board.bp[int(self.y)][int(endpoint)]))
            # print("endpoint: " + str(endpoint))
            # print("self.y: " + str(self.y))
            # print("xpos: " + str(self.x + self.vx - self.rx + np.sign(self.vx)))
            # print("ypos: " + str(self.y - self.vy + self.ry - np.sign(self.vy)))
            # sleep(10)
            if C.fireball:
                bricks[board.bp[int(self.y - self.vy + self.ry)]
                       [int(endpoint)]].boom(board, bricks, self)
            else:
                bricks[board.bp[int(self.y - self.vy + self.ry)][int(endpoint)]].hit(board, bricks, self)
            self.y = self.y - self.vy + self.ry
            self.x = self.x + self.vx - self.rx
            self.vx = -1*self.vx
            self.rx = self.vx
            self.ry = self.vy
            play_bump()
            # self.rx += np.sign(self.vx)
            return True

        return False

    def collCheckY (self, paddle, board, vel, bricks, ufo):
        endpoint = self.y - self.vy + self.ry - vel
        if endpoint < 0:
            self.y = 0
            self.x = self.x + self.vx - self.rx
            self.vy = -1*self.vy

            self.rx = self.vx
            self.ry = self.vy
            play_bump()
            # self.ry += np.sign(self.vy)


            return True

        elif (self.x + self.vx - self.rx >= paddle.x and self.x + self.vx - self.rx < paddle.x + paddle.width) and endpoint == paddle.y:
            self.y = paddle.y - 1
            # print('henlo')
            # print(self.x)
            self.x = self.x + self.vx - self.rx
            # print(self.x)
            # sleep(0.5)
            self.vy = -1*self.vy
            self.ry = self.vy
            # self.ry += np.sign(self.vy)
            if paddle.width % 2 == 0:
                self.vx = (self.x - paddle.x - paddle.width/2) // 3
                if self.vx>=0:
                    self.vx+=1
            else:
                self.vx = (self.x - paddle.x - (paddle.width-1)/2) // 3

            if self.vx > 3:
                self.vx = 3
            elif self.vx <-3:
                self.vx = -3
            
            # self.vx = 10
            play_bump()

            self.rx = self.vx

            board.brick_fall(bricks)

            return True

        elif C.level_counter == 3 and (self.x + self.vx - self.rx >= ufo.x and self.x + self.vx - self.rx < ufo.x + ufo.width) and endpoint == ufo.y:
            self.y = ufo.y + 1
            # print('henlo')
            # print(self.x)
            self.x = self.x + self.vx - self.rx
            # print(self.x)
            # sleep(0.5)
            self.vy = -1*self.vy
            self.ry = self.vy
            # self.ry += np.sign(self.vy)
            # if paddle.width % 2 == 0:
            #     self.vx = self.x - paddle.x - paddle.width/2
            #     if self.vx >= 0:
            #         self.vx += 1
            # else:
            #     self.vx = (self.x - paddle.x - (paddle.width-1)/2) // 3

            # if self.vx > 3:
            #     self.vx = 3
            # elif self.vx < -3:
            #     self.vx = -3

            # self.vx = 10

            self.rx = self.vx
            play_bump

            ufo.health -= 1

            if ufo.health == (C.boss_health * 3) // 5 or ufo.health == C.boss_health // 5:
                ufo.spawn_bricks(board, bricks)

            # board.brick_fall(bricks)

            return True

        elif board.bp[int(endpoint)][int(self.x + self.vx - self.rx)] >= 0:
            # print("block_ind: " + str(board.bp[int(endpoint)][int(self.x)]))
            # print("self.x: " + str(self.x))
            # print("endpoint: " + str(endpoint))
            # print("xpos: " + str(self.x + self.vx - self.rx + np.sign(self.vx)))
            # print("ypos: " + str(self.y - self.vy + self.ry - np.sign(self.vy)))
            # sleep(10)
            if C.fireball:
                bricks[board.bp[int(endpoint)][int(
                    self.x + self.vx - self.rx)]].boom(board, bricks, self)
            else:
                bricks[board.bp[int(endpoint)][int(self.x + self.vx - self.rx)]].hit(board, bricks, self)
            self.y = self.y - self.vy + self.ry
            self.x = self.x + self.vx - self.rx
            self.vy = -1*self.vy

            self.rx = self.vx
            self.ry = self.vy
            play_bump()
            # self.ry += np.sign(self.vy)
            return True

        return False
