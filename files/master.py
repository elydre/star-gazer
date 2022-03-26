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

import os, sys
from time import sleep, time

from cryptography.fernet import Fernet

import mod.key as key
import mod.util as util
import mod.cros as cros
from mod.POOcom import ClientCom

start = "!06!"

cmd_help = """
CAT         affiche le contenu de pool.py
CLEAR       clear screen
CPU         get cpu count of all workers
EXIT        quitte le programme
FM          affiche l'historique des messages
GO          lance le travail
HELP        affiche cette aide
LW          affiche la liste des workers
MM          affiche les messages du master
PING/GET    recupère la liste des workers
PRINT       affiche un message chez les workers
SW          stop tout les workers
WM          affiche les messages des workers
"""

worker_messages = []
master_messages = []
full_messages = []
worker = []

f = Fernet(key.key) 
client = ClientCom()

find_diff = lambda l1, l2: [e for e in l1 if e not in l2]
get_inp = lambda inp, id, default: default if len(inp) <= id else inp[id]
secure_send = lambda code, msg: client.send(start + f.encrypt(f"{code}§{msg}".encode()).decode())
msg_history = lambda msg: "\n".join([":".join([str(f) for f in e]) for e in msg])

@client.on_message
def recv_msg(msg):
    if msg.startswith(start):
        new = f.decrypt(msg[len(start):].encode()).decode()
        code, msg = int(new.split("§")[0]), "§".join(new.split("§")[1:])
        full_messages.append((code, msg))
        if code % 2 == 1: worker_messages.append((code, msg))
        else: master_messages.append((code, msg))

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

def wait_reply(attendu, code, string1, max_wait=10):
    w = []
    s = []
    debut = time()
    while len(w) < attendu:
        sleep(0.1)
        for m in worker_messages:
            if m[0] != code:
                continue
            worker_messages.remove(m)
            info = m[1].split("§")
            print(f"{info[0]} {string1}")
            w.append(info[0])
            s.append("§".join(info[1:]))
        if time() - debut > max_wait and max_wait != -1:
            return s, w, round((time() - debut) * 1000)
    return s, 0, round((time() - debut) * 1000)

def go_reply(exit_code):
    
    s, x, t = wait_reply(exit_code, 151, "starts work")
    if x == 0: print(f"all workers started in {t}ms")
    else: return print(f"no reply from {find_diff(worker, x)} in {t}ms")

    s, x, t = wait_reply(exit_code, 153, "ends work", -1)
    print(f"all workers finished in {t}ms")

    print(cros.main(s))

def get_cpu_count():
    for w in worker:
        secure_send(102, w)
    s, x, t = wait_reply(len(worker), 103, "reply")
    if x == 0: print(f"all workers replied in {t}ms")
    else: print(f"no reply from {find_diff(worker, x)} in {t}ms")
    total_cpu = 0
    for e in s:
        temp = e.split("§")
        print(f" {temp[0]} has {temp[1]} cores")
        total_cpu += int(temp[1])
    print(f"total cpu count : {total_cpu}")


def shell():
    while True:
        inp = input("MASTER > ").split(" ")
        cmd = inp[0]
        if cmd in ["exit", "quit", "q"]:
            try: client.close()
            except: pass
            sys.exit(0)


        elif cmd in ["help", "?"]:
            print(cmd_help)

        elif cmd in ["cat"]:
            print(util.read("fmaster/pool.py"))

        elif cmd in ["fm"]:
            print(msg_history(full_messages))

        elif cmd in ["wm"]:
            print(msg_history(worker_messages))
        
        elif cmd in ["mm"]:
            print(msg_history(master_messages))

        elif cmd in ["ping", "get"]:
            ping(int(get_inp(inp, 1, 3)))

        elif cmd in ["lw", "w"]:
            print(f"{len(worker)} workers in list")
            print(", ".join(worker))

        elif cmd in ["cpu", "lscpu"]:
            get_cpu_count()

        elif cmd in ["clear", "cls"]:
            os.system("cls")

        elif cmd in ["print"]:
            secure_send(154, get_inp(inp, 1, "%master print"))

        elif cmd in ["go", "start", "run"]:
            exit_code = go(inp)
            if exit_code > 0:
                go_reply(exit_code)

        elif cmd in ["stopw", "sw"]:
            secure_send(156, "stop")

        elif cmd != "":
            print("commande inconnue")


while True:
    try: shell()
    except KeyboardInterrupt: print("ctrl+c")