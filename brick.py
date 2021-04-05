import numpy as np
from powerup import *
import config as C


class Brick:
    def __init__(self, strength, x, y, ind, board):
        self.x = x
        self.y = y
        self.str = strength
        self.width = 5
        self.height = 1

        for i in range(self.width):
            for j in range(self.height):
                board.bp[self.y+j][self.x+i] = ind

    def hit(self, board, bricks, ball):
        self.str -= 1
        if self.str == 0:
            if np.random.random() < C.pprob and C.level_counter != 3:
                # create powerup
                C.powerups.append(Powerup(self.x, self.y, board, np.random.choice(['s','f']), ball.vx, ball.vy))

            for i in range(self.width):
                for j in range(self.height):
                    board.bp[self.y+j][self.x+i] = -1

    def destroy(self, board, bricks, ball):
        self.str = 0
        if np.random.random() < C.pprob and C.level_counter != 3:
            # create powerup
            C.powerups.append(Powerup(self.x, self.y, board,
                                      np.random.choice(['s', 'f']), ball.vx, ball.vy))

        for i in range(self.width):
            for j in range(self.height):
                board.bp[self.y+j][self.x+i] = -1
    
    def boom (self, board, bricks, ball):
        C.fireball = False
        for i in range(self.width):
            for j in range(self.height):
                board.bp[self.y+j][self.x+i] = -1

        # Brick top
        if board.bp[self.y-1][self.x] >= 0:
            bricks[board.bp[self.y-1][self.x]].destroy(board, bricks, ball)

        # Brick bottom
        if board.bp[self.y+self.height][self.x] >= 0:
            bricks[board.bp[self.y+self.height]
                   [self.x]].destroy(board, bricks, ball)

        # Brick left
        if board.bp[self.y][self.x-1] >= 0:
            bricks[board.bp[self.y][self.x-1]].destroy(board, bricks, ball)

        # Brick right
        if board.bp[self.y][self.x+self.width] >= 0:
            bricks[board.bp[self.y][self.x+self.width]
                   ].destroy(board, bricks, ball)

        # Brick top-left
        if board.bp[self.y-1][self.x-1] >= 0:
            bricks[board.bp[self.y-1][self.x-1]].destroy(board, bricks, ball)

        # Brick top-right
        if board.bp[self.y-1][self.x+self.width] >= 0:
            bricks[board.bp[self.y-1][self.x+self.width]
                   ].destroy(board, bricks, ball)

        # Brick bottom-left
        if board.bp[self.y+self.height][self.x-1] >= 0:
            bricks[board.bp[self.y+self.height]
                   [self.x-1]].destroy(board, bricks, ball)

        # Brick bottom-right
        if board.bp[self.y+self.height][self.x+self.width] >= 0:
            bricks[board.bp[self.y+self.height]
                   [self.x+self.width]].destroy(board, bricks, ball)


class ExpBrick(Brick):
    def __init__(self, x, y, ind, board):
        Brick.__init__(self, 4, x, y, ind, board)

    def hit(self, board, bricks, ball):
        self.destroy(board, bricks, ball)

    def destroy(self, board, bricks, ball):
        for i in range(self.width):
            for j in range(self.height):
                board.bp[self.y+j][self.x+i] = -1

        # Brick top
        if board.bp[self.y-1][self.x] >= 0:
            bricks[board.bp[self.y-1][self.x]].destroy(board, bricks, ball)

        # Brick bottom
        if board.bp[self.y+self.height][self.x] >= 0:
            bricks[board.bp[self.y+self.height]
                   [self.x]].destroy(board, bricks, ball)

        # Brick left
        if board.bp[self.y][self.x-1] >= 0:
            bricks[board.bp[self.y][self.x-1]].destroy(board, bricks, ball)

        # Brick right
        if board.bp[self.y][self.x+self.width] >= 0:
            bricks[board.bp[self.y][self.x+self.width]
                   ].destroy(board, bricks, ball)

        # Brick top-left
        if board.bp[self.y-1][self.x-1] >= 0:
            bricks[board.bp[self.y-1][self.x-1]].destroy(board, bricks, ball)

        # Brick top-right
        if board.bp[self.y-1][self.x+self.width] >= 0:
            bricks[board.bp[self.y-1][self.x+self.width]
                   ].destroy(board, bricks, ball)

        # Brick bottom-left
        if board.bp[self.y+self.height][self.x-1] >= 0:
            bricks[board.bp[self.y+self.height]
                   [self.x-1]].destroy(board, bricks, ball)

        # Brick bottom-right
        if board.bp[self.y+self.height][self.x+self.width] >= 0:
            bricks[board.bp[self.y+self.height]
                   [self.x+self.width]].destroy(board, bricks, ball)


class RainbowBrick(Brick):
    def __init__(self, x, y, ind, board):
        Brick.__init__(self, 5, x, y, ind, board)

    def hit(self, board, bricks, ball):
        if self.str == 5:
            self.str = np.random.choice([1, 2, 3])
        else:
            self.str -= 1
            if self.str == 0:
                if np.random.random() < C.pprob and C.level_counter != 3:
                    # create powerup
                    C.powerups.append(
                        Powerup(self.x, self.y, board, np.random.choice(['s', 'f']), ball.vx, ball.vy))

                for i in range(self.width):
                    for j in range(self.height):
                        board.bp[self.y+j][self.x+i] = -1


def level_random(board, prob):
    bricks = []

    for i in range(1, 7):
        for j in range(2, 15):
            if(np.random.randint(1, prob) == 1):
                str = np.random.choice([-1, 1, 1, 1, 2, 2, 3, 3, 5])
                if str != 5:
                    bricks.append(Brick(str, 5*i, j, len(bricks), board))
                    bricks.append(Brick(str, board.width - 5 *
                                        (i+1), j, len(bricks), board))
                else:
                    bricks.append(RainbowBrick(5*i, j, len(bricks), board))
                    bricks.append(RainbowBrick(board.width - 5 *
                                               (i+1), j, len(bricks), board))

    exp_y = np.random.randint(4, 7)
    exp_x = np.random.randint(1, 3)

    for x in range(exp_x, 6):
        if board.bp[exp_y][5*x] >= 0:
            bricks[board.bp[exp_y][5*x]] = ExpBrick(
                5*x, exp_y, board.bp[exp_y][5*x], board)
            bricks[board.bp[exp_y][board.width - 5 * (x+1)]] = ExpBrick(
                board.width - 5 * (x+1), exp_y, board.bp[exp_y][board.width - 5 * (x+1)], board)
        else:
            bricks.append(ExpBrick(
                5*x, exp_y, len(bricks), board))
            bricks.append(ExpBrick(board.width - 5 *
                                   (x+1), exp_y, len(bricks), board))

        if np.random.random() >= 1/4:
            exp_y += 1

    return bricks

def boss_level_random(board):
    bricks = []

    # for i in range(1, 7):
    #     for j in range(7, 20):
    #         if(np.random.randint(1, 11) == 1):
    #             str = np.random.choice([1, 1, 1, 2, 2, 3, 3, 5])
    #             if str != 5:
    #                 bricks.append(Brick(str, 5*i, j, len(bricks), board))
    #                 bricks.append(Brick(str, board.width - 5 *
    #                                     (i+1), j, len(bricks), board))
    #             else:
    #                 bricks.append(RainbowBrick(5*i, j, len(bricks), board))
    #                 bricks.append(RainbowBrick(board.width - 5 *
    #                                            (i+1), j, len(bricks), board))

    bricks.append(Brick(-1, 5*2, 4, len(bricks), board))
    bricks.append(Brick(-1, board.width - 5 * (2+1), 4, len(bricks), board))
    bricks.append(Brick(-1, 5*4, 4, len(bricks), board))
    bricks.append(Brick(-1, board.width - 5 * (4+1), 4, len(bricks), board))

    bricks.append(Brick(-1, 5*3, 8, len(bricks), board))
    bricks.append(Brick(-1, board.width - 5 * (3+1), 8, len(bricks), board))
    bricks.append(Brick(-1, 5*5, 8, len(bricks), board))
    bricks.append(Brick(-1, board.width - 5 * (5+1), 8, len(bricks), board))

    bricks.append(Brick(-1, 5*2, 12, len(bricks), board))
    bricks.append(Brick(-1, board.width - 5 * (2+1), 12, len(bricks), board))
    bricks.append(Brick(-1, 5*4, 12, len(bricks), board))
    bricks.append(Brick(-1, board.width - 5 * (4+1), 12, len(bricks), board))


    # exp_y = np.random.randint(4, 7)
    # exp_x = np.random.randint(1, 3)

    # for x in range(exp_x, 6):
    #     if board.bp[exp_y][5*x] >= 0:
    #         bricks[board.bp[exp_y][5*x]] = ExpBrick(
    #             5*x, exp_y, board.bp[exp_y][5*x], board)
    #         bricks[board.bp[exp_y][board.width - 5 * (x+1)]] = ExpBrick(
    #             board.width - 5 * (x+1), exp_y, board.bp[exp_y][board.width - 5 * (x+1)], board)
    #     else:
    #         bricks.append(ExpBrick(
    #             5*x, exp_y, len(bricks), board))
    #         bricks.append(ExpBrick(board.width - 5 *
    #                                (x+1), exp_y, len(bricks), board))

    #     if np.random.random() >= 1/4:
    #         exp_y += 1

    return bricks


def calc_score(bricks, board, ufo):
    existing_bricks = [False] * len(bricks)

    for i in range(board.height):
        for j in range(board.width):
            if board.bp[i][j] >= 0:
                existing_bricks[board.bp[i][j]] = True

    score = 0
    for i, val in enumerate(existing_bricks):
        if val:
            if 4 > bricks[i].str > 0:
                score += 10*bricks[i].str
            elif bricks[i].str == 4:
                score += 10
            elif bricks[i].str == 5:
                score += 40

    if C.level_counter == 3 and C.boss_health // 5 < ufo.health <= (C.boss_health*3) // 5:
        score -= 120
    elif C.level_counter == 3 and ufo.health == C.boss_health // 5:
        score -= 240
    return score


def next_level(level, board):
    board.bp = np.full([board.height, board.width], -1)
    board.pp = np.full([board.height, board.width], '')
    board.lasers = np.full([board.height, board.width], '')
    if level == 1:
        return level_random(board, 11)
    elif level == 2:
        return level_random(board, 9)
    elif level == 3:
        return boss_level_random(board)
