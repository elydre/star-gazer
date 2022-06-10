'''    _             _
  ___ | | _   _   __| | _ __   ___
 / _ \| || | | | / _` || '__| / _ |
|  __/| || |_| || (_| || |   |  __/
 \___||_| \__, | \__,_||_|    \___|
          |___/
___________________________________

 - codé en : UTF-8
 - langage : python3
 - GitHub  : github.com/elydre
 - Licence : GNU GPL v3
'''

entette = """
     |
,---.|--- ,---.,---.   ,---.,---.,---,,---.,---.
`---.|    ,---||    ---|   |,---| .-' |---'|
`---'`---'`---^`       `---|`---^'---'`---'`
 hole                  `---'
"""

import socket
import sys
import os
from _thread import start_new_thread
from multiprocessing import Pool
from random import choice, randint
from time import sleep

from cryptography.fernet import Fernet

KEY = ""
stop = False

def code_centre(arg):
    l, code = arg
    exec(code)
    return(eval(f"centre({l})"))

def code_do(arg):
    l, code = arg
    exec(code)
    return(eval(f"do({l})"))

if __name__ == "__main__":

    def read(chemain):
        with open(f'{os.path.dirname(sys.argv[0])}/{chemain}' if sys.platform == "win32" else chemain, "r") as fil:
            code = fil.read()
        return code

    KEY = read("/key.txt") if KEY == "" else KEY
    
    def generer_liste(start, end, step, quantite, n):
        listes = [[] for _ in range(quantite)]

        istep = 0
        ii = 0
        for i in range(start, end):

            listes[istep].append(i)
            ii += 1

            if ii == step:
                istep += 1
                ii = 0
            
            if istep == quantite:
                istep = 0
            
        if n == -1:
            return listes
        return listes[n]

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

    f = Fernet(KEY)
    client = ClientCom()

    global cpu_usable
    cpu_usable = 100
    personal_id = choice(["elise", "ronan", "adele", "clara", "alain", "loris", "akyzo", "haros", "mario"]) + str(randint(1000, 9999))
    start = "!06!"

    print(entette)

    secure_send = lambda code, msg: client.send(start + f.encrypt(f"{code}§{msg}".encode()).decode())

    def analyse(code, msg):
        global cpu_usable
        if code == 100:
            secure_send(101, personal_id)
            print("pong send")

        info = msg.split("§")
        if info[0] == personal_id:

            if code == 102:
                secure_send(103, f"{personal_id}§{personal_id}§{os.cpu_count()}§{cpu_usable}")
                print(f"cpu send, nb cpu : {os.cpu_count()}, {cpu_usable}% usable")

            elif code == 150:
                gn = [int(e) for e in info[1].split(",")]
                liste = generer_liste(*gn)
                print(f"starts work, {len(liste)} elements in todo list")
                secure_send(151, f"{personal_id}")
                s = go(info[2], liste)
                print(f"{personal_id} ends work, {s}")
                secure_send(153, f"{personal_id}§{s}")

            elif code == 154:
                print("§".join(info[1:]).replace("%", "\n").replace("$", personal_id).replace("#", "\n"*100))

            elif code == 156:
                print("STOP")
                global stop
                stop = True
                try: client.close()
                except: pass
                sys.exit(0)

            elif code == 158:
                print(f"cpu usable set to {info[1]}%")
                cpu_usable = int(info[1])


    def go(func, todo):
        print(func)

        code = func.split("§")[0]
        print("ecrire DONE!")

        with Pool(int(os.cpu_count()*(cpu_usable/100))) as p:
            sortie = (p.map(code_do, [[t, code] for t in todo]))
        print("pool DONE!")

        with Pool(1) as p:
            s = (p.map(code_centre, [[sortie, code]])[0])
        print(f"centre DONE! - {s}")

        return s        

    @client.on_message
    def recv_msg(msg):
        if msg.startswith(start):
            try:
                new = f.decrypt(msg[len(start):].encode()).decode()
                start_new_thread(analyse, (int(new.split("§")[0]), "§".join(new.split("§")[1:])))
            except Exception:
                print("decrypt error")

    try:
        print(f"worker DONE - {personal_id}")
        while not stop:
            sleep(1)
    except KeyboardInterrupt:
        client.close()
