import sys
from multiprocessing import Pool
from os import cpu_count, path

from cryptography.fernet import Fernet

import mod.key as key
from mod.POOcom import ClientCom
from temp.code import do, centre

def code_centre(l):
    return centre(l)

def code_do(n):
    return do(n)

if __name__ == "__main__":
    f = Fernet(key.key) 

    client = ClientCom()

    start = "!06!"

    path_v = path.dirname(sys.argv[0])

    secure_send = lambda msg: client.send(start + f.encrypt(msg.encode()).decode())



    def go(func):

        print(f"{func}")

        with open(f'{path_v}/temp/code.py' if sys.platform == "win32" else "temp/code.py", "w") as f:
            f.write(func.split("§")[0])

        print("ecrire DONE!")

        todo = eval(func.split("§")[1])

        print("todo DONE!")

        with Pool(cpu_count()) as p:
            sortie = (p.map(code_do, todo))

        print("pool DONE!")

        with Pool(1) as p:
            s = (p.map(code_centre, [sortie])[0])

        print("centre DONE!")

        print(s)
        secure_send(str(s))

        print("send DONE!")

    @client.on_message
    def recv_msg(msg):
        if msg.startswith(start):
            go(f.decrypt(msg[len(start):].encode()).decode())

    try:
        while True:
            input()
    except KeyboardInterrupt:
        client.close()