from input import *
from paddle import *
from board import Board, print_time
from ball import *
from brick import *
from os import system
from time import sleep, time
import config as C
import sound

system('clear')
print('\033[0;0H')

fps = 20
naptime = 1/fps

board = Board()
paddle = Paddle(board)
ufo = UFO(board)

system("stty -echo")

prtper = True
lives = 3

C.start_time = time()


C.powerups = []

C.level_counter = 1
C.scores = [0,0,0]
# bricks = []

bricks = next_level(C.level_counter, board)
start_score = calc_score(bricks, board, ufo)

C.play_time = '0:00'

C.ticks = 0

if __name__ == '__main__':
    # system('clear')
    for live in range(lives):
        ball = Ball(paddle,False)
        while True:
            st = str(input_to())

            if st!=None:
                sleep(0.08)


            ball.move(paddle, board, bricks, ufo)
            ball.move(paddle, board, bricks, ufo)

            C.ticks += 1
            C.ticks = C.ticks % 10000000
            nuked = False

            if(C.ticks % 2 == 0):
                move_powerups(board, paddle)
                to_kill = []
                for i in C.llist:
                    i.move(board, bricks)
                    if i.ded:
                        to_kill.append(i)
                for i in to_kill:
                    C.llist.remove(i)
                to_kill = []
                for i in C.bombs:
                    if(i.move(board, paddle) == -1):
                        nuked = True
                        break
                    if i.ded:
                        to_kill.append(i)
                for i in to_kill:
                    C.bombs.remove(i)

            if nuked:
                break

            if(C.ticks % 20 == 0 and C.shoot['active']):
                C.llist.append(Laser(board, paddle.x, paddle.y - 1))
                C.llist.append(Laser(board, paddle.x + paddle.width - 1, paddle.y - 1))
                sound.play_shoot()

            if(C.ticks % 35 == 20 and C.level_counter == 3):
                ufo.drop_bomb(board)


            # ball.move(paddle, board, bricks)
            
            # prtper = not prtper
            # if speedspeed:
            #     prtper = True
            
            if st == 'x':
                system("stty echo")
                quit()
            elif st == 'a' or st == 'A':
                paddle.move(-1,board, ball, ufo)
            elif st == 'd' or st == 'D':
                paddle.move(1,board, ball, ufo)
            elif (st == 'w' or st == 'W') and ball.attach:
                ball.release()
            elif (st == 'p' or st == 'P'):
                print(ball.vx)
                print(ball.vy)
                sleep(0.5)
            elif st == 'n' or st == 'N':
                C.scores[C.level_counter-1] = start_score - \
                    calc_score(bricks, board, ufo)
                C.level_counter += 1
                C.start_time = time()
                if(C.level_counter > 3):
                    system('clear')
                    print("GAME OVER")
                    print(C.play_time)
                    print(C.final_score)
                    system("stty echo")
                    quit()
                ball = Ball(paddle, False)
                bricks = next_level(C.level_counter, board)
                start_score = calc_score(bricks, board, ufo)
                start_score += C.scores[C.level_counter-2]
                C.powerups = []
                C.shoot['active'] = False
                C.fireball = False
                system('clear')
                print('\033[0;0H')
            
            if ball.ded:
                board.pp = np.full([board.height, board.width], '')
                board.lasers = np.full([board.height, board.width], '')
                C.powerups = []
                C.shoot['active'] = False
                C.fireball = False
                break

            board.render(paddle,ball,bricks,ufo)
            print("Lives: " + str(lives - live))
            C.play_time = print_time(C.start_time)
            C.final_score = "Score: " + str(start_score - calc_score(bricks, board, ufo))
            # C.final_score = "Score: " + str(calc_score(bricks, board))
            print(C.final_score)
            shoot_time = time() - C.shoot['time']
            if shoot_time > 10 and C.shoot['active']:
                C.shoot['active'] = False
            if C.shoot['active']:
                print("Laser Paddle Duration: " + str(int(10 - shoot_time)))
            # else:
                # print("                                                                                         ")

            print('\033[0;0H')
            if (calc_score(bricks, board, ufo) == 0 and C.level_counter != 3) or (ufo.health == 0 and C.level_counter == 3):
                system('clear')
                print('\033[0;0H')
                print("Congratulation, you won!!!")
                print(C.play_time)
                print(C.final_score)
                # system("stty echo")
                while True:
                    st = str(input_to())
                    if st == 'n' or st == 'N':
                        C.scores[C.level_counter-1] = start_score - \
                            calc_score(bricks, board, ufo)
                        C.level_counter += 1
                        if(C.level_counter > 3):
                            system('clear')
                            print("GAME OVER")
                            print(C.play_time)
                            print(C.final_score)
                            system("stty echo")
                            quit()
                        C.start_time = time()
                        ball = Ball(paddle, False)
                        bricks = next_level(C.level_counter, board)
                        start_score = calc_score(bricks, board, ufo)
                        start_score += C.scores[C.level_counter-2]
                        C.powerups = []
                        C.shoot['active'] = False
                        C.fireball = False
                        system('clear')
                        print('\033[0;0H')
                        break



    system('clear')
    print("GAME OVER")
    print(C.play_time)
    print(C.final_score)

    system("stty echo")
