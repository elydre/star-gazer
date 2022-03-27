'''
--|~|--|~|--|~|--|~|--|~|--|~|--
██  ████        ██████        ██
████    ██     ██           ████
██      ██   ████████     ██  ██
████████       ██       ██    ██
██             ██       █████████
██             ██             ██
██
 - codé en : UTF-8
 - langage : python 3
 - GitHub  : github.com/pf4-DEV
--|~|--|~|--|~|--|~|--|~|--|~|--
'''

import socket
from _thread import start_new_thread

version = "1.1.2"

def recv_msg(s, maped):
    while True:
        for e in s.recv(1024).decode().split("<end>")[:-1]:
            maped(e)

class ClientCom:
    def __init__(self, host = "pf4.ddns.net", port = 63535):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

    def on_message(self, func):
        start_new_thread(recv_msg, (self.s, func))

    def send(self, msg):
        self.s.send(f"{msg}<end>".encode())

    def close(self):
        self.s.close()