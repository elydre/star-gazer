import sys
from multiprocessing import Pool
from os import cpu_count, path
from time import sleep

from cryptography.fernet import Fernet

import mod.key as key
from mod.POOcom import ClientCom
from worker.code import do, centre
from random import randint, choice


def code_centre(l):
    return centre(l)

def code_do(n):
    return do(n)

if __name__ == "__main__":

    f = Fernet(key.key) 
    client = ClientCom()

    path_v = path.dirname(sys.argv[0])
    personal_id = choice(["elise", "ronan", "adele", "clara", "alain", "loris"]) + str(randint(1000, 9999))
    start = "!06!"


    secure_send = lambda code, msg: client.send(start + f.encrypt(f"{code}§{msg}".encode()).decode())

    def analyse(code, msg):
        if code == 100:
            sleep(randint(1, 500)/1000)
            secure_send(101, personal_id)
            print("pong send")


    def go(func):
        print(f"{func}")

        with open(f'{path_v}/worker/code.py' if sys.platform == "win32" else "worker/code.py", "w") as f:
            f.write(func.split("§")[0])
        print("ecrire DONE!")

        todo = eval(func.split("§")[1])
        print("todo DONE!")

        with Pool(cpu_count()) as p:
            sortie = (p.map(code_do, todo))
        print("pool DONE!")

        with Pool(1) as p:
            s = (p.map(code_centre, [sortie])[0])
        print(f"centre DONE! - {s}")
        
        secure_send(str(s))
        print("send DONE!")

    @client.on_message
    def recv_msg(msg):
        if msg.startswith(start):
            new = f.decrypt(msg[len(start):].encode()).decode()
            analyse(int(new.split("§")[0]), "§".join(new.split("§")[1:]))

    try:
        print(f"worker DONE - {personal_id}")
        while True:
            input()
    except KeyboardInterrupt:
        client.close()