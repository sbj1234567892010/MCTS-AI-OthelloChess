import AI
import sys,random,pygame,math,threading
from pygame.locals import *
from AI import *
from math import *



pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Reversi")
font = pygame.font.Font(None,18)

initimage = pygame.image.load("init.png")
initimage = pygame.transform.smoothscale(initimage,(800,600))
board = pygame.image.load("background.jpg")
board = pygame.transform.smoothscale(board,(600,600))
blackimage = pygame.image.load("black.png")
blackimage = pygame.transform.smoothscale(blackimage,(60,60))
whiteimage = pygame.image.load("white.png")
whiteimage = pygame.transform.smoothscale(whiteimage,(60,60))

laughimage = pygame.image.load("laugh.png")
laughimage = pygame.transform.smoothscale(laughimage,(60,60))
cryimage = pygame.image.load("cry.png")
cryimage = pygame.transform.smoothscale(cryimage,(60,60))

start_x = 33
start_y = 29
distance = 68

gamestate = 0 #init state
start = 0     #who start first

playerturn = 0 #who's turn
UCTstate = OthelloState(8)

#the mouse position
mouse_x = 0
mouse_y = 0

#calculate which square the mouse in,according to the mouse position
area_x = -1
area_y = -1

turn = 1


def mouse_area(x,y):
    global area_x,area_y
    area_y = int((x - start_x)/distance)
    area_x = int((y - start_y)/distance)

def draw_chess():
    global UCTstate
    for i in range(8):
        for j in range(8):
            if UCTstate.board[i][j] == 1:
                screen.blit(blackimage,(start_x + j*distance,start_y + i*distance))
            elif UCTstate.board[i][j] == 2:
                screen.blit(whiteimage, (start_x + j * distance, start_y + i * distance))


def check_turn():
    global UCTstate
    global turn
    if UCTstate.GetMoves()!=[]:
        turn = 3 - turn
    else:
        print("player continue")
        UCTstate.playerJustMoved = 2

def draw_valid():
    global UCTstate
    valid = UCTstate.GetMoves()
    for area in valid:
        screen.blit(laughimage,(start_x + area[1] * distance, start_y + area[0] * distance))

def aifunc():
    global turn
    global playerturn
    global UCTstate
    if turn == 3 - playerturn:
        m = UCT(rootstate=UCTstate, itermax=10000000, verbose=False)
        UCTstate.DoMove((m[0],m[1]))
        if UCTstate.GetMoves != []:
            turn = 3 - turn
        else:
            print("AI continue")
            UCTstate.playerJustMoved = 1

def check_gameover():
    global UCTstate
    global start
    global gamestate
    if UCTstate.GetMoves() == []:
        print("Debug")
        UCTstate.playerJustMoved = 3 - UCTstate.playerJustMoved
        if UCTstate.GetMoves() == []:
            print("gameover")
            start = False
            gamestate = 0
            blackcount = len([(x, y) for x in range(UCTstate.size) for y in range(UCTstate.size) if UCTstate.board[x][y] == 1])
            whitecount = len(
                [(x, y) for x in range(UCTstate.size) for y in range(UCTstate.size) if UCTstate.board[x][y] == 2])
            if blackcount > whitecount:
                print("Black Win!")
            elif whitecount > blackcount:
                print("White Win!")
            else:
                print("Draw!")
            UCTstate = OthelloState(8)
        else:
            UCTstate.playerJustMoved = 3 - UCTstate.playerJustMoved

def game():
    global gamestate
    global UCTstate
    while gamestate == 1:
        screen.blit(board,(0,0))
        draw_chess()
        if turn == playerturn:
            draw_valid()
        for event in pygame.event.get():  # get mouse and key events
            if event.type == MOUSEBUTTONDOWN:
                pressed_array = pygame.mouse.get_pressed()
                if pressed_array[0]:
                    pos = pygame.mouse.get_pos()
                    pos_x = pos[0]
                    pos_y = pos[1]
                    mouse_area(pos_x,pos_y)
                    if turn == playerturn and (area_x,area_y) in UCTstate.GetMoves():
                        UCTstate.DoMove((area_x,area_y))
                        draw_chess()
                        pygame.display.update()
                        #print("draw")
                        check_turn()
        aifunc()
        check_gameover()
        pygame.display.update()
    return

def init():
    global start
    global gamestate
    global playerturn
    while True:
        screen.blit(initimage, (0, 0))
        #screen.blit(BLACKFIRST, (200, 250))
        #screen.blit(WHITEFIRST,(400,250))
        pygame.draw.rect(screen,[0,0,0],[300,175,200,100])
        pygame.draw.rect(screen, [255, 255, 255], [300, 325, 200, 100])
        for event in pygame.event.get():  # get mouse and key events
            if event.type == MOUSEBUTTONDOWN:
                pressed_array = pygame.mouse.get_pressed()
                if pressed_array[0]:
                    pos = pygame.mouse.get_pos()
                    pos_x = pos[0]
                    pos_y = pos[1]
                    if pos_x >= 300 and pos_x <= 500 and pos_y >= 175 and pos_y <= 275:
                        start = True
                        playerturn = 1

                    elif pos_x >= 300 and pos_x <= 500 and pos_y >= 325 and pos_y <= 425:
                        start = True
                        playerturn = 2
        if start :
            gamestate = 1
            break
        pygame.display.update()

def loop():
    while True:
        if gamestate == 0:
            init()
        elif gamestate == 1:
            game()

if __name__ == '__main__':
    loop()