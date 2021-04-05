from brick import level_random
import numpy as np
from colorama import Fore, Back, Style
from time import time
import config as C
from os import system

def print_time(start_time):
    cur_time = time()
    mins = int((cur_time - start_time) / 60)
    seconds = int((cur_time - start_time) % 60)
    if seconds < 10:
        seconds = '0'+str(seconds)
    else:
        seconds = str(seconds)

    print("Time Played: " + str(mins) + ':' + seconds)
    return "Time Played: " + str(mins) + ':' + seconds


class Board:
    def __init__(self):
        self.width = 60
        self.height = 30
        self.bp = np.full([self.height,self.width], -1)
        self.pp = np.full([self.height, self.width], '')
        self.lasers = np.full([self.height, self.width], '')
        self.bombs = np.full([self.height, self.width], '')
    
    def render(self, paddle, ball, bricks, ufo):
        # do the printing
        bored = np.full([self.height,self.width], ' ')
        # for i in range(self.height):
        #     for j in range(self.width):
        #         if self.bp[i][j]>=0:
        #             bored[i][j]=self.bp[i][j]

        if C.level_counter == 3:
            # Health bar
            Hbar = [' '] * ((self.width * ufo.health)//C.boss_health)
            Rbar = [' '] * (self.width - (self.width *
                                          ufo.health)//C.boss_health)
            for i in Hbar:
                print(Back.RED + i, end='')
            for i in Rbar:
                print(Back.WHITE + i, end='')
            print()    

        for i in range(self.height):
            for j in range(self.width):
                if self.bombs[i][j] != '':
                    print(Back.WHITE + Fore.RED + self.bombs[i][j], end='')
                elif C.level_counter == 3 and i == ufo.y and j >= ufo.x and j < ufo.x+ufo.width:
                    print(Back.YELLOW + Fore.BLACK + ' ', end='')
                elif self.pp[i][j] != '':
                    print(Back.YELLOW + Fore.BLACK + self.pp[i][j], end='')
                elif self.lasers[i][j] != '':
                    print(Back.WHITE + Fore.RED + self.lasers[i][j], end='')
                elif i == paddle.y and (j == paddle.x or j == paddle.x+paddle.width-1) and C.shoot['active']:
                    print(Back.RED + Fore.BLACK + bored[i][j], end='')
                elif i == paddle.y and j>=paddle.x and j<paddle.x+paddle.width:
                    print(Back.BLUE + Fore.BLACK + bored[i][j], end='')
                elif i == ball.y and j == ball.x:
                    print(Back.WHITE + Fore.BLACK + '●', end='')
                elif self.bp[i][j]>=0:
                    if bricks[self.bp[i][j]].str <= -1:
                        print(Back.BLACK + Fore.WHITE + bored[i][j], end='')
                    elif bricks[self.bp[i][j]].str == 1:
                        print(Back.GREEN + Fore.WHITE + bored[i][j], end='')
                    elif bricks[self.bp[i][j]].str == 2:
                        print(Back.CYAN + Fore.WHITE + bored[i][j], end='')
                    elif bricks[self.bp[i][j]].str == 3:
                        print(Back.MAGENTA + Fore.WHITE + bored[i][j], end='')
                    elif bricks[self.bp[i][j]].str == 4:
                        print(Back.RED + Fore.WHITE + bored[i][j], end='')
                    elif bricks[self.bp[i][j]].str == 5:
                        print(np.random.choice([Back.GREEN, Back.CYAN, Back.MAGENTA]) + Fore.WHITE + bored[i][j], end='')
                else:
                    print(Back.WHITE, end='')
                    print(bored[i][j], end='')
            print()
        print(Style.RESET_ALL, end='')

    def brick_fall(self, bricks):
        if time() - C.start_time > 45:
            # drop everything in board.bp
            # drop everything in bricks
            # check if anything falls out of the board.
            temp_board = np.full([self.height, self.width], -1)
            for i in range(self.height - 1):
                for j in range(self.width):
                    temp_board[i+1][j] = self.bp[i][j]
            self.bp = temp_board

            y_max = 0
            for i in bricks:
                i.y += 1
                if i.y > y_max:
                    y_max = i.y
            
            if y_max >= self.height - 1:
                system('clear')
                print("GAME OVER")
                print(C.play_time)
                print(C.final_score)

                system("stty echo")
                quit()

        return 0
