import os
from time import sleep, time

from cryptography.fernet import Fernet

import mod.key as key
import mod.util as util
from mod.POOcom import ClientCom

start = "!06!"

messages = []
worker = []

f = Fernet(key.key) 
client = ClientCom()

secure_send = lambda code, msg: client.send(start + f.encrypt(f"{code}§{msg}".encode()).decode())

@client.on_message
def recv_msg(msg):
    if msg.startswith(start):
        new = f.decrypt(msg[len(start):].encode()).decode()
        messages.append([int(new.split("§")[0]), "§".join(new.split("§")[1:])])

def go(inp):
    def push(start, end, step, quantite):
        pool = util.read("fmaster/pool.py")
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
        for m in messages:
            if m[0] == 101:
                messages.remove(m)
                worker.append(m[1])
                print(f"{m[1]} is online {round((time() - d)*1000)}ms")
    print(f"ping DONE!, {len(worker)} workers online")

def wait_reply(exit_code):
    started = []
    while len(started) < exit_code:
        sleep(0.1)
        for m in messages:
            if m[0] == 151:
                messages.remove(m)
                info = m[1].split("§")
                print(f"{info[0]} starts work, {info[1]} elements in todo list :)")
                started.append(info[0])

def shell():
    while True:
        get_inp = lambda inp, id, default: default if len(inp) <= id else inp[id]

        inp = input("MASTER > ").split(" ")
        cmd = inp[0]
        if cmd in ["exit", "quit", "q"]:
            client.close()
            return

        elif cmd in ["msg", "print"]:
            print(messages)

        elif cmd in ["ping", "get"]:
            ping(int(get_inp(inp, 1, 3)))

        elif cmd in ["lw", "w"]:
            print(f"{len(worker)} workers in list")
            print(", ".join(worker))

        elif cmd in ["clear", "cls"]:
            os.system("cls")

        elif cmd in ["go", "start", "run"]:
            exit_code = go(inp)
            if exit_code > 0:
                wait_reply(exit_code)

        elif cmd != "":
            print("commande inconnue")

try:
    while True:
        shell()
except KeyboardInterrupt:
    client.close()