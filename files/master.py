import os, sys
from time import sleep, time

from cryptography.fernet import Fernet

import mod.key as key
import mod.util as util
import mod.cros as cros
from mod.POOcom import ClientCom

start = "!06!"

cmd_help = """
CLEAR       clear screen
EXIT        quitte le programme
GO          lance le travail
HELP        affiche cette aide
LW          affiche la liste des workers
MM          affiche les messages du master
PING/GET    recupère la liste des workers
WM          affiche les messages des workers
"""

worker_messages = []
master_messages = []
worker = []

f = Fernet(key.key) 
client = ClientCom()

secure_send = lambda code, msg: client.send(start + f.encrypt(f"{code}§{msg}".encode()).decode())

@client.on_message
def recv_msg(msg):
    if msg.startswith(start):
        new = f.decrypt(msg[len(start):].encode()).decode()
        code, msg = int(new.split("§")[0]), "§".join(new.split("§")[1:])
        if code % 2 == 1:
            worker_messages.append((code, msg))
        else:
            master_messages.append((code, msg))

def go(inp):
    def push(start, end, step, quantite):
        pool = util.read("fmaster/pool.py").split("#END#")[0]
        for n in range(quantite):
            secure_send(150, f"{worker[n]}§{start},{end},{step},{quantite},{n}§{pool}")
            print(f"send to {worker[n]}")
            sleep(0.1)

    if len(inp) == 1:
        print("go <end>")
        print("go <start> <end>")
        print("go <start> <end> <step>")
        print("go <start> <end> <step> <quantite>")
        return -1
    if len(inp) == 2:
        push(0, inp[1], 10, len(worker))
    elif len(inp) == 3:
        push(inp[1], inp[2], 10, len(worker))
    elif len(inp) == 4:
        push(inp[1], inp[2], inp[3], len(worker))
    elif len(inp) == 5:
        push(inp[1], inp[2], inp[3], inp[4])
    else:
        print("Syntax error")
        return -1
    return inp[4] if len(inp) > 4 else len(worker)

def ping(to_wait):
    secure_send(100, "ping")
    worker.clear()
    d = time()
    while to_wait > (time() - d):
        sleep(0.05)
        for m in worker_messages:
            if m[0] == 101:
                worker_messages.remove(m)
                worker.append(m[1])
                print(f"{m[1]} is online {round((time() - d)*1000)}ms")
    print(f"ping DONE!, {len(worker)} workers online")

def wait_reply(exit_code):
    w = []
    while len(w) < exit_code:
        sleep(0.1)
        for m in worker_messages:
            if m[0] != 151:
                continue
            worker_messages.remove(m)
            info = m[1].split("§")
            print(f"{info[0]} starts work, {info[1]} elements in todo list :)")
            w.append(info[0])
    print("all workers started")

    w, s = [], []
    while len(w) < exit_code:
        sleep(0.1)
        for m in worker_messages:
            if m[0] != 153:
                continue
            worker_messages.remove(m)
            info = m[1].split("§")
            print(f"{info[0]} finished work, s = {info[1]}")
            s.append(info[1])
            w.append(info[0])
    print("all workers finished")

    print(cros.main(s))


def shell():
    while True:
        get_inp = lambda inp, id, default: default if len(inp) <= id else inp[id]

        inp = input("MASTER > ").split(" ")
        cmd = inp[0]
        if cmd in ["exit", "quit", "q"]:
            try: client.close()
            except: pass
            sys.exit(0)


        elif cmd in ["help", "?"]:
            print(cmd_help)

        elif cmd in ["wm"]:
            print(worker_messages)
        
        elif cmd in ["mm"]:
            print(master_messages)

        elif cmd in ["ping", "get"]:
            ping(int(get_inp(inp, 1, 3)))

        elif cmd in ["lw", "w"]:
            print(f"{len(worker)} workers in list")
            print(", ".join(worker))

        elif cmd in ["clear", "cls"]:
            os.system("cls")

        elif cmd in ["print"]:
            secure_send(154, get_inp(inp, 1, "%master print"))

        elif cmd in ["go", "start", "run"]:
            exit_code = go(inp)
            if exit_code > 0:
                wait_reply(exit_code)

        elif cmd != "":
            print("commande inconnue")


while True:
    try: shell()
    except KeyboardInterrupt: print("ctrl+c")