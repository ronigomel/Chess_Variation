import socket
import threading
from typing import List

from tcp_by_size import send_with_size, recv_by_size
import time

TURN = 'white'
TURN_LOCK = threading.Lock()


class ChessGame:
    def __init__(self):
        self._outbox = {}
        self._is_white_connected = False
        self._is_black_connected = False
        self._turn = 0

    def white_connected(self) -> bool:
        self._is_white_connected = True

    def black_connected(self) -> bool:
        self._is_black_connected = True

    def game_started(self) -> bool:
        return self._is_white_connected and self._is_black_connected

    def put_black_msg(self, msg: str):
        """
        black put msg to white's outbox
        :param msg: data to send
        """
        self._outbox['white'] = msg

    def put_white_msg(self, msg: str):
        """
        white put msg to black's outbox
        :param msg: data to send
        """
        self._outbox['black'] = msg

    def get_black_msg(self) -> str:
        msg = self._outbox['black']
        del self._outbox['black']
        return msg

    def get_white_msg(self) -> str:
        msg = self._outbox['white']
        del self._outbox['white']
        return msg

    def is_empty(self, colour: str) -> bool:
        return colour not in self._outbox

    def add_turn(self):
        self._turn += 1

    def get_turns(self) -> int:
        return self._turn


def connect(ip: str, port: int):
    server_socket = socket.socket()
    server_socket.bind((ip, port))
    server_socket.listen(2)

    threads = []
    colour = 'white'
    connection = ChessGame()

    for i in range(2):
        print(colour)
        client_socket, client_address = server_socket.accept()
        print('connected')

        if colour == 'black':
            game_start = True
        t = threading.Thread(target=client_loop, args=(client_socket, colour, connection))

        if colour == 'white':
            colour = 'black'

        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

    server_socket.close()
    print('server died')


def log(direction: str, msg: str, colour: str):
    print(direction + '\n')
    print(colour + ': ' + msg)


def client_loop(client_socket: socket.socket, colour: str, game: ChessGame):
    global TURN

    print('start new client thread ' + colour)
    log('new client!', 'connected', colour)
    sent_white = False

    if colour == 'white':
        send_with_size(client_socket, bytearray('00000001$', 'utf-8'), colour)
        log('server >> client ', '00000001$', colour)
        game.white_connected()
    elif colour == 'black':
        send_with_size(client_socket, bytearray('00000000$', 'utf-8'), colour)
        log('server >> client ', '00000000$', colour)
        game.black_connected()

    while not game.game_started():
        time.sleep(0.2)

    while game.game_started():
        if TURN == colour:
            data = recv_by_size(client_socket, colour).decode('utf-8')
            if colour == 'white':
                game.put_white_msg(data)
            else:
                game.put_black_msg(data)

            if data[:4] == 'STOP':

                """
                if colour == 'white':
                    game.put_white_msg(data)
                else:
                    game.put_black_msg(data)"""
                break
            with TURN_LOCK:
                TURN = 'white' if TURN == 'black' else 'black'
            game.add_turn()
        else:
            while game.is_empty(colour):
                time.sleep(0.1)
            if colour == 'white':
                send_with_size(client_socket, bytearray(game.get_white_msg(), 'utf-8'), colour)
            else:
                send_with_size(client_socket, bytearray(game.get_black_msg(), 'utf-8'), colour)

    print('thread going to die ' + colour)


connect('0.0.0.0', 8820)
