import sys
import socket
import pygame
import datetime
import time
import threading
from chess_pieces import *
from tcp_by_size import *

IP = '192.168.1.141'
PORT = 8820
SOCKET_PLAYER = socket.socket()
FILE_NAME = ''
STOP = False
WINDOW_WIDTH = 1250
WINDOW_HEIGHT = 750
win = True

possible_spots = []
GAME_ON = False
TURN_COUNT = 0
MY_TURN = True
WHITE_PLAYER = True
BOARD = [[object, object, object, object, object, object, object, object, object],  # row 0
         [object, object, object, object, object, object, object, object, object],  # row 1
         [None, None, None, None, None, None, None, None],  # row 2
         [None, None, None, None, None, None, None, None],  # row 3
         [None, None, None, None, None, None, None, None],  # row 4
         [None, None, None, None, None, None, None, None],  # row 5
         [object, object, object, object, object, object, object, object, object],  # row 6
         [object, object, object, object, object, object, object, object, object]]  # row 7
pygame.init()
img = pygame.image.load('intro3.jpg')
white = (255, 255, 255)
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
kill_zone_x = 95
kill_zone_y = 82
space_white = 57
space_black = 1002
deaths_mine = 0
kills_other = 0
temp = (0, 0)
BOARD_PIXELS = [[temp for i in range(8)] for k in range(8)]


def reset_board():
    global BOARD
    global BOARD_PIXELS
    for i in range(8):
        BOARD[1][i] = Piece(False, 'pawn', 'pawn_b.png', (i, 1))
        BOARD[6][i] = Piece(True, 'pawn', 'pawn_w.png', (i, 6))

    print('board reset')
    BOARD[0][0] = Piece(False, 'rook', 'rook_b.png', (0, 0))
    BOARD[0][1] = Piece(False, 'knight', 'knight_b.png', (1, 0))
    BOARD[0][2] = Piece(False, 'bishop', 'bishop_b.png', (2, 0))
    BOARD[0][3] = Piece(False, 'queen', 'queen_b.png', (3, 0))
    BOARD[0][4] = Piece(False, 'king', 'king_b.png', (4, 0))
    BOARD[0][5] = Piece(False, 'bishop', 'bishop_b.png', (5, 0))
    BOARD[0][6] = Piece(False, 'knight', 'knight_b.png', (6, 0))
    BOARD[0][7] = Piece(False, 'rook', 'rook_b.png', (7, 0))

    BOARD[7][0] = Piece(True, 'rook', 'rook_w.png', (0, 7))
    BOARD[7][1] = Piece(True, 'knight', 'knight_w.png', (1, 7))
    BOARD[7][2] = Piece(True, 'bishop', 'bishop_w.png', (2, 7))
    BOARD[7][3] = Piece(True, 'queen', 'queen_w.png', (3, 7))
    BOARD[7][4] = Piece(True, 'king', 'king_w.png', (4, 7))
    BOARD[7][5] = Piece(True, 'bishop', 'bishop_w.png', (5, 7))
    BOARD[7][6] = Piece(True, 'knight', 'knight_w.png', (6, 7))
    BOARD[7][7] = Piece(True, 'rook', 'rook_w.png', (7, 7))

    y_pixels = 85
    x_pixels = 332
    for i in range(8):  # fills the rest of the tiles with the right pixels (top left corner)
        for k in range(8):
            BOARD_PIXELS[i][k] = (x_pixels, y_pixels)
            x_pixels += 73
        x_pixels = 332
        y_pixels += 73


def pawn_moves(pawn):
    global BOARD
    spot_x, spot_y = pawn.get_placement()
    spots = []
    if not WHITE_PLAYER:
        print('black')
        if spot_y != 7:
            if spot_y == 1 and BOARD[spot_y + 2][spot_x] is None:
                spots.append((spot_x, spot_y + 2))
            if BOARD[spot_y + 1][spot_x] is None:
                spots.append((spot_x, spot_y + 1))
            if spot_x != 0:
                if BOARD[spot_y + 1][spot_x - 1] is not None:
                    if BOARD[spot_y + 1][spot_x - 1].get_team() != WHITE_PLAYER:
                        BOARD[spot_y + 1][spot_x - 1].killable()
                        spots.append((spot_x - 1, spot_y + 1))
            if spot_x != 7:
                if BOARD[spot_y + 1][spot_x + 1] is not None:
                    if BOARD[spot_y + 1][spot_x + 1].get_team() != WHITE_PLAYER:
                        BOARD[spot_y + 1][spot_x + 1].killable()
                        spots.append((spot_x + 1, spot_y + 1))
                if BOARD[spot_y + 1][spot_x - 1] is not None:
                    if BOARD[spot_y + 1][spot_x - 1].get_team() != WHITE_PLAYER:
                        BOARD[spot_y + 1][spot_x - 1].killable()
                        spots.append((spot_x - 1, spot_y + 1))
    else:
        if spot_y > 0:
            if spot_y == 6 and BOARD[spot_y - 2][spot_x] is None:
                spots.append((spot_x, spot_y - 2))
            if BOARD[spot_y - 1][spot_x] is None:
                spots.append((spot_x, spot_y - 1))
            if spot_x != 0:
                if BOARD[spot_y - 1][spot_x - 1] is not None:
                    if BOARD[spot_y - 1][spot_x - 1].get_team() != WHITE_PLAYER:
                        BOARD[spot_y - 1][spot_x - 1].killable()
                        spots.append((spot_x - 1, spot_y - 1))
            if spot_x != 7:
                if BOARD[spot_y - 1][spot_x + 1] is not None:
                    if BOARD[spot_y - 1][spot_x + 1].get_team() != WHITE_PLAYER:
                        BOARD[spot_y - 1][spot_x + 1].killable()
                        spots.append((spot_x + 1, spot_y - 1))
                if BOARD[spot_y - 1][spot_x - 1] is not None:
                    if BOARD[spot_y - 1][spot_x - 1].get_team() != WHITE_PLAYER:
                        BOARD[spot_y - 1][spot_x - 1].killable()
                        spots.append((spot_x + 1, spot_y - 1))
    return spots


def log(direction, msg):
    return
    print(
        '------------------------------------------------------------ ' + direction + ' ------------------------------------------------------------\n')
    print(str(datetime.datetime.now()) + ' |  msg:  ' + msg)
    print(print(
        '\n------------------------------------------------------------------------------------------------------------------------------------------------\n'))


def print_possible_moves(spots):
    global BOARD_PIXELS

    for i in range(len(spots)):
        x = BOARD_PIXELS[spots[i][1]][spots[i][0]][0]
        y = BOARD_PIXELS[spots[i][1]][spots[i][0]][1]
        circle = pygame.image.load('green_circle.png').convert()
        red = (255, 0, 0, 0)
        circle.set_colorkey(red)
        screen.blit(circle, [x, y])
        pygame.display.flip()

    return spots


def rook_moves(rook):
    global BOARD
    spot_x, spot_y = rook.get_placement()
    temp_y = spot_y + 1
    spots = []
    while temp_y < 8 and BOARD[temp_y][spot_x] is None:
        spots.append((spot_x, temp_y))
        temp_y += 1
    if temp_y < 8:
        if BOARD[temp_y][spot_x] is not None:
            if BOARD[temp_y][spot_x].get_team() != rook.get_team():
                BOARD[temp_y][spot_x].killable()
                spots.append((spot_x, temp_y))

    temp_x = spot_x + 1
    while temp_x < 8 and BOARD[spot_y][temp_x] is None:
        spots.append((temp_x, spot_y))
        temp_x += 1
    if temp_x < 8:
        if BOARD[spot_y][temp_x].get_team() != rook.get_team():
            BOARD[spot_y][temp_x].killable()
            spots.append((temp_x, spot_y))

    temp_y = spot_y - 1
    while temp_y >= 0 and BOARD[temp_y][spot_x] is None:
        spots.append((spot_x, temp_y))
        temp_y -= 1
    if temp_y > -1:
        if BOARD[temp_y][spot_x] is not None:
            if BOARD[temp_y][spot_x].get_team() != rook.get_team():
                BOARD[temp_y][spot_x].killable()
                spots.append((spot_x, temp_y))

    temp_x = spot_x - 1
    while temp_x >= 0 and BOARD[spot_y][temp_x] is None:
        spots.append((temp_x, spot_y))
        temp_x -= 1

    if temp_x > -1:
        if BOARD[spot_y][temp_x] is not None:
            if BOARD[spot_y][temp_x].get_team() != rook.get_team():
                BOARD[spot_y][temp_x].killable()
                spots.append((temp_x, spot_y))

    return spots


def find_tile(x_mouse, y_mouse):
    x_board = 0
    y_board = 0
    stop = False
    for i in range(8):
        for k in range(8):
            if x_mouse >= BOARD_PIXELS[i][k][0] and x_mouse < BOARD_PIXELS[i][k][0] + 73:
                if y_mouse >= BOARD_PIXELS[i][k][1] and y_mouse < BOARD_PIXELS[i][k][1] + 73:
                    x_board = k
                    y_board = i
                    stop = True
                    break
        if stop:
            break
    return x_board, y_board


def knight_moves(knight):
    spot_x, spot_y = knight.get_placement()
    spots = []
    # All possible moves of a knight
    x_moves = [2, 1, -1, -2, -2, -1, 1, 2]
    y_moves = [1, 2, 2, 1, -1, -2, -2, -1]

    # Check if each possible move
    # is valid or not
    for i in range(8):
        # Position of knight after move
        x = spot_x + x_moves[i]
        y = spot_y + y_moves[i]

        # count valid moves
        if x >= 0 and y >= 0 and x < 8 and y < 8:
            if BOARD[y][x] is not None:
                if BOARD[y][x].get_team() != WHITE_PLAYER:
                    BOARD[y][x].killable()
                    spots.append((x, y))
            else:
                spots.append((x, y))

    # Return  possible moves
    return spots


def queen_moves(queen):
    spots = []
    if len(list(rook_moves(queen))) > 0:
        for spot in list(rook_moves(queen)):
            spots.append(spot)
    if len(list(bishop_moves(queen))) > 0:
        for spot in list(bishop_moves(queen)):
            spots.append(spot)
    return spots


def king_moves(king):
    spot_x, spot_y = king.get_placement()
    spots = []

    # all possible king moves
    x_moves = [1, -1, 0, 0, 1, -1, 1, -1]
    y_moves = [0, 0, 1, -1, 1, -1, -1, 1]

    for i in range(8):
        # Position of knight after move
        x = spot_x + x_moves[i]
        y = spot_y + y_moves[i]

        # count valid moves
        if x >= 0 and y >= 0 and x < 8 and y < 8:
            if BOARD[y][x] is not None:
                if BOARD[y][x].get_team() != WHITE_PLAYER:
                    BOARD[y][x].killable()
                    spots.append((x, y))
            else:
                spots.append((x, y))

    # Return  possible moves
    return spots


def bishop_moves(bishop):
    x_spot, y_spot = bishop.get_placement()
    temp_x = x_spot + 1
    temp_y = y_spot + 1

    spots = []

    # checks right downward diagonal
    while temp_x < 8 and temp_y < 8:
        if BOARD[temp_y][temp_x] is not None:
            break
        spots.append((temp_x, temp_y))

        temp_x += 1
        temp_y += 1

    if temp_x < 8 and temp_y < 8:
        if BOARD[temp_y][temp_x] is not None:
            if BOARD[temp_y][temp_x].get_team() != WHITE_PLAYER:
                BOARD[temp_y][temp_x].killable()
                spots.append((temp_x, temp_y))

    temp_x = x_spot + 1
    temp_y = y_spot - 1

    # checks right upward diagonal
    while temp_x < 8 and temp_y >= 0:
        if BOARD[temp_y][temp_x] is not None:
            break
        spots.append((temp_x, temp_y))
        temp_x += 1
        temp_y -= 1

    if temp_x < 8 and temp_y >= 0:
        if BOARD[temp_y][temp_x] is not None:
            if BOARD[temp_y][temp_x].get_team() != WHITE_PLAYER:
                BOARD[temp_y][temp_x].killable()
                spots.append((temp_x, temp_y))

    temp_x = x_spot - 1
    temp_y = y_spot - 1

    # checks for left upward diagonal
    while temp_x >= 0 and temp_y >= 0:
        if BOARD[temp_y][temp_x] is not None:
            break
        spots.append((temp_x, temp_y))

        temp_x -= 1
        temp_y -= 1

    if temp_x >= 0 and temp_y >= 0:
        if BOARD[temp_y][temp_x] is not None:
            if BOARD[temp_y][temp_x].get_team() != WHITE_PLAYER:
                BOARD[temp_y][temp_x].killable()
                spots.append((temp_x, temp_y))

    temp_x = x_spot - 1
    temp_y = y_spot + 1

    # checks downward left diagonal
    while temp_x >= 0 and temp_y < 8:
        if BOARD[temp_y][temp_x] is not None:
            break
        spots.append((temp_x, temp_y))

        temp_x -= 1
        temp_y += 1

    if temp_x >= 0 and temp_y < 8:
        if BOARD[temp_y][temp_x] is not None:
            if BOARD[temp_y][temp_x].get_team() != WHITE_PLAYER:
                BOARD[temp_y][temp_x].killable()
                spots.append((temp_x, temp_y))

    return spots


def send_move(old_spot, new_spot, colour):
    write_move(new_spot)
    msg = str(old_spot[0]) + '-' + str(old_spot[1]) + '-' + str(new_spot[0]) + '-' + str(new_spot[1]) + '$'
    send_with_size(SOCKET_PLAYER, bytearray(msg, 'utf-8'), colour)
    log('client >> server', msg)


def write_move(new_spot):
    row = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    with open(FILE_NAME, 'a+') as f1:
        txt = str(TURN_COUNT - 1) + ': ' + BOARD[new_spot[1]][new_spot[0]].get_type() + ' to ' + str(new_spot[0] + 1) + \
              row[
                  new_spot[1]] + '\r\n'
        f1.write(txt)


def recv_move():
    try:
        msg = recv_by_size(SOCKET_PLAYER, '').decode('utf-8')
        log('server >> client', msg)
        msg = msg[:11]
        msg = msg.strip('$').split('-')
        msg[0] = int(msg[0])
        msg[1] = int(msg[1])
        msg[2] = int(msg[2])
        msg[3] = int(msg[3])
    except socket.error:
        return ""

    return msg


def intro():
    global win
    global possible_spots
    global STOP
    global MY_TURN
    global TURN_COUNT
    global screen
    global white
    global size
    global img
    global deaths_mine
    global GAME_ON

    first_press = True
    former_y = 0
    former_x = 0

    reset_board()
    pygame.display.set_caption("Game")
    screen.fill(white)
    screen.blit(img, (0, 0))
    pygame.display.flip()

    if not WHITE_PLAYER:
        MY_TURN = False
    t = threading.Thread(target=not_my_turn, )
    t.start()
    while not STOP:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                STOP = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if TURN_COUNT == 0:
                        img = pygame.image.load('board.jpg')
                        # printing images
                        screen.fill(white)
                        screen.blit(img, (0, 0))
                        pygame.display.flip()
                        for row in range(8):
                            for cube in range(8):
                                if BOARD[row][cube] is not None:
                                    x = BOARD_PIXELS[row][cube][0]
                                    y = BOARD_PIXELS[row][cube][1]
                                    BOARD[row][cube].print(x, y, screen)
                        TURN_COUNT += 1
                        print('game on')
                        GAME_ON = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if GAME_ON:
                    if pygame.mouse.get_pressed()[0]:
                        x, y = pygame.mouse.get_pos()
                        if limits(x, y):
                            if MY_TURN:
                                if first_press:
                                    x_board, y_board = find_tile(x, y)
                                    if BOARD[y_board][x_board] is not None:
                                        if BOARD[y_board][x_board].get_team() == WHITE_PLAYER:
                                            former_y = y_board
                                            former_x = x_board
                                            type_p = BOARD[y_board][x_board].get_type()
                                            if type_p == 'rook':
                                                possible_spots = list(
                                                    print_possible_moves(list(rook_moves(BOARD[y_board][x_board]))))
                                            elif type_p == 'king':
                                                possible_spots = list(print_possible_moves(
                                                    (list(king_moves(BOARD[y_board][x_board])))))
                                            elif type_p == 'bishop':
                                                possible_spots = list(print_possible_moves(
                                                    list(bishop_moves(BOARD[y_board][x_board]))))
                                            elif type_p == 'pawn':
                                                possible_spots = list(
                                                    print_possible_moves(list(pawn_moves(BOARD[y_board][x_board]))))
                                            elif type_p == 'queen':
                                                possible_spots = list(print_possible_moves(
                                                    list(queen_moves(BOARD[y_board][x_board]))))
                                            else:  # 'knight'
                                                possible_spots = list(print_possible_moves(
                                                    list(knight_moves(BOARD[y_board][x_board]))))

                                        if len(possible_spots) > 0:
                                            first_press = False
                                else:
                                    if len(possible_spots) > 0:
                                        x_spot, y_spot = find_tile(x, y)
                                        if (x_spot, y_spot) in possible_spots:
                                            # checks if spot selected is filled with the opposite team's piece
                                            if BOARD[y_spot][x_spot] is not None and BOARD[y_spot][
                                                x_spot].get_team() != WHITE_PLAYER:
                                                BOARD[y_spot][x_spot].killed()
                                                if WHITE_PLAYER:  # checks for white player if checkmate for the black king
                                                    if BOARD[y_spot][x_spot].get_type() == 'king':
                                                        STOP = True
                                                        GAME_ON = False
                                                        send_move((former_x, former_y), (x_spot, y_spot), '')
                                                        break
                                                    else:
                                                        BOARD[y_spot][x_spot].print(
                                                            (deaths_mine % 2) * kill_zone_x + space_white,
                                                            ((deaths_mine // 2) % 5) * kill_zone_y + 169, screen)

                                                        print_square(x_spot, y_spot)

                                                        BOARD[y_spot][x_spot].killed()
                                                        BOARD[y_spot][x_spot] = None

                                                        deaths_mine += 1
                                                else:  # checks for black player if checkmate
                                                    if BOARD[y_spot][x_spot].get_type() == 'king':
                                                        GAME_ON = False
                                                        STOP = True
                                                        send_move((former_x, former_y), (x_spot, y_spot), '')
                                                        break
                                                    else:
                                                        BOARD[y_spot][x_spot].print(
                                                            (deaths_mine % 2) * kill_zone_x + space_black,
                                                            ((deaths_mine // 2) % 5) * kill_zone_y + 169, screen)

                                                        print_square(x_spot, y_spot)

                                                        BOARD[y_spot][x_spot].killed()
                                                        BOARD[y_spot][x_spot] = None
                                                        deaths_mine += 1

                                            BOARD[y_spot][x_spot] = BOARD[former_y][former_x]
                                            BOARD[former_y][former_x] = None

                                            BOARD[y_spot][x_spot].set_placement((x_spot, y_spot))

                                            for spot in possible_spots:
                                                if spot != (x_spot, y_spot):
                                                    if BOARD[spot[1]][spot[0]] is not None:
                                                        if BOARD[spot[1]][spot[0]].get_killable():
                                                            BOARD[spot[1]][spot[0]].risk_free()

                                            TURN_COUNT += 1
                                            MY_TURN = False

                                            print_square(former_x, former_y)
                                            for spot in possible_spots:
                                                print_square(spot[0], spot[1])

                                            send_move((former_x, former_y), (x_spot, y_spot), '')
                                            for row in range(8):
                                                for cube in range(8):
                                                    if BOARD[row][cube] is not None:
                                                        x = BOARD_PIXELS[row][cube][0]
                                                        y = BOARD_PIXELS[row][cube][1]
                                                        BOARD[row][cube].print(x, y, screen)
                                            first_press = True
                                        else:
                                            print('wrong limit')
    end()



def end():
    img_end = pygame.image.load('end_lose.jpg')
    if win:
        img_end = pygame.image.load('end_win.jpg')
    screen.blit(img_end, [0, 0])
    pygame.display.flip()
    time.sleep(2)

    pygame.quit()
    print("Main thread dies")

def print_square(x, y):
    img_file = ''
    if (x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1):
        img_file = 'white_sqr.jpg'
    else:
        img_file = 'black_sqr.jpg'

    x_spot = BOARD_PIXELS[y][x][0]
    y_spot = BOARD_PIXELS[y][x][1]

    img = pygame.image.load(img_file)
    screen.blit(img, [x_spot, y_spot])
    pygame.display.flip()


def not_my_turn():
    global STOP
    global win
    global MY_TURN
    global GAME_ON
    global kills_other

    while not STOP:
        if GAME_ON:
            player2_move = recv_move()
            if not player2_move:
                break
            if BOARD[player2_move[3]][player2_move[2]] is not None:
                if WHITE_PLAYER:
                    if BOARD[player2_move[3]][player2_move[2]].get_type() == 'king':
                        print('king')
                        STOP = True
                        win = False
                        GAME_ON = False
                        end()
                        SOCKET_PLAYER.close()
                        break
                    else:
                        BOARD[player2_move[3]][player2_move[2]].killed()

                        BOARD[player2_move[3]][player2_move[2]].print(
                            (kills_other % 2) * kill_zone_x + space_black,
                            ((kills_other // 2) % 5) * kill_zone_y + 169, screen)
                        BOARD[player2_move[3]][player2_move[2]] = None
                        kills_other += 1
                else:
                    if BOARD[player2_move[3]][player2_move[2]].get_type() == 'king':
                        print('king')
                        STOP = True
                        win = False
                        end()
                        SOCKET_PLAYER.close()
                    else:
                        BOARD[player2_move[3]][player2_move[2]].killed()

                        BOARD[player2_move[3]][player2_move[2]].print(
                            (kills_other % 2) * kill_zone_x + space_white,
                            ((kills_other // 2) % 5) * kill_zone_y + 169, screen)
                        BOARD[player2_move[3]][player2_move[2]] = None
                        kills_other += 1

            print_square(player2_move[2], player2_move[3])
            BOARD[player2_move[3]][player2_move[2]] = BOARD[player2_move[1]][player2_move[0]]
            BOARD[player2_move[1]][player2_move[0]].set_placement(
                (player2_move[2], player2_move[3]))
            BOARD[player2_move[1]][player2_move[0]] = None

            print_square(player2_move[0], player2_move[1])
            for row in range(8):
                for cube in range(8):
                    if BOARD[row][cube] is not None:
                        x = BOARD_PIXELS[row][cube][0]
                        y = BOARD_PIXELS[row][cube][1]
                        BOARD[row][cube].print(x, y, screen)

            MY_TURN = True

    SOCKET_PLAYER.close()
    print("thread client Died")
def limits(x, y):
    if x >= 335 and x <= 915:
        if y >= 84 and y <= 665:
            return True
    return False


def connect():
    global STOP
    global IP
    global PORT
    global SOCKET_PLAYER
    global FILE_NAME
    global MY_TURN
    global WHITE_PLAYER

    #    if len(sys.argv) != 4:
    #       return
    #    IP = sys.argv[1]
    #    PORT = sys.argv[2]
    FILE_NAME = 'sys.argv[3]' + '_moves.txt'

    with open(FILE_NAME, 'w') as f1:
        f1.write(FILE_NAME[:4] + "'s moves\r\n")

    SOCKET_PLAYER = socket.socket()
    SOCKET_PLAYER.connect((IP, PORT))
    print('connected')
    data = recv_by_size(SOCKET_PLAYER, '').decode('utf-8')
    data = data[:-1]
    if data == '00000001':
        WHITE_PLAYER = True
    else:
        WHITE_PLAYER = False
        MY_TURN = False

    intro()
    SOCKET_PLAYER.close()


connect()
