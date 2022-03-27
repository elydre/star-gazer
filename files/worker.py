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
 - Licence : GNU GPL v3
--|~|--|~|--|~|--|~|--|~|--|~|--
'''

from multiprocessing import Pool
from os import cpu_count
from random import choice, randint
from time import sleep
import sys

from cryptography.fernet import Fernet

import mod.util as util
from mod.POOcom import ClientCom
from fworker.code import centre, do

stop = False

def code_centre(l):
    return centre(l)

def code_do(n):
    return do(n)

if __name__ == "__main__":

    f = Fernet(util.loadkey()) 
    client = ClientCom()

    global cpu_usable
    cpu_usable = 100
    personal_id = choice(["elise", "ronan", "adele", "clara", "alain", "loris", "akyzo", "haros"]) + str(randint(1000, 9999))
    start = "!06!"

    print(util.entette)

    secure_send = lambda code, msg: client.send(start + f.encrypt(f"{code}§{msg}".encode()).decode())

    def analyse(code, msg):
        global cpu_usable
        if code == 100:
            sleep(randint(1, 500)/1000)
            secure_send(101, personal_id)
            print("pong send")

        info = msg.split("§")
        if info[0] == personal_id:

            if code == 102:
                sleep(randint(1, 500)/1000)
                secure_send(103, f"{personal_id}§{personal_id}§{cpu_count()}§{cpu_usable}")
                print(f"cpu send, nb cpu : {cpu_count()}, {cpu_usable}% usable")

            elif code == 150:
                gn = [int(e) for e in info[1].split(",")]
                liste = util.generer_liste(*gn)
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

        util.write("fworker/code.py", func.split("§")[0])
        print("ecrire DONE!")

        with Pool(int(cpu_count()*(cpu_usable/100))) as p:
            sortie = (p.map(code_do, todo))
        print("pool DONE!")

        with Pool(1) as p:
            s = (p.map(code_centre, [sortie])[0])
        print(f"centre DONE! - {s}")

        return s        

    @client.on_message
    def recv_msg(msg):
        if msg.startswith(start):
            try:
                new = f.decrypt(msg[len(start):].encode()).decode()
                analyse(int(new.split("§")[0]), "§".join(new.split("§")[1:]))
            except:
                print("decrypt error")

    try:
        print(f"worker DONE - {personal_id}")
        while not stop:
            sleep(1)
    except KeyboardInterrupt:
        client.close()