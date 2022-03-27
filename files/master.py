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

import mod.util as util
import mod.cros as cros
from mod.POOcom import ClientCom


f = Fernet(util.loadkey())
client = ClientCom()

find_diff = lambda l1, l2: [e for e in l1 if e not in l2]
get_inp = lambda inp, id, default: default if len(inp) <= id else inp[id]
secure_send = lambda code, msg: client.send(start + f.encrypt(f"{code}§{msg}".encode()).decode())
msg_history = lambda msg: "\n".join([":".join([str(f) for f in e]) for e in msg])

start = "!06!"
fonc_time = 0.05
send_time = 0.05

cmd_help = """
CAT         affiche le contenu de pool.py
CLEAR       clear screen
CPU         get cpu count of all workers
EXIT        quitte le programme
GO          lance le travail
HELP        affiche cette aide
INIT        reinitialise le programme
KEY         affiche la clef de cryptage
LW          affiche la liste des workers
MF          affiche l'historique des messages
MM          affiche les messages du master
MW          affiche les messages des workers
PERF        modifie les ressources utilisable des workers
PING/GET    recupère la liste des workers
PRINT       affiche un message chez les workers
SPEED       la latence master-msg-master
SW          stop tout les workers
"""

path = [
[["cat"],                   lambda inp: print(util.read("fmaster/pool.py"))],
[["clear", "cls"],          lambda inp: os.system('cls' if os.name == 'nt' else 'clear')],
[["cpu", "lscpu"],          lambda inp: get_cpu_count()],
[["exit", "quit", "q"],     lambda inp: quit()],
[["go", "start", "run"],    lambda inp: start_go(inp)],
[["help", "?"],             lambda inp: print(cmd_help)],
[["init", "r"],             lambda inp: init(print("init done"))],
[["key"],                   lambda inp: print(util.loadkey().decode())],
[["lw", "w"],               lambda inp: print(f"{len(worker)} workers in list\n", "\n ".join([f"{worker.index(w)}. {w}" for w in worker]))],
[["mf"],                    lambda inp: print(msg_history(full_messages))],
[["mm"],                    lambda inp: print(msg_history(master_messages))],
[["mw"],                    lambda inp: print(msg_history(worker_messages))],
[["perf", "%"],             lambda inp: code2w(158, get_inp(inp, 1, "*"), get_inp(inp, 2, 100))],
[["ping", "get"],           lambda inp: ping(int(get_inp(inp, 1, 3)))],
[["print"],                 lambda inp: code2w(154, get_inp(inp, 1, "*"), get_inp(inp, 2, "%master print"))],
[["speed"],                 lambda inp: speed()],
[["stopw", "sw"],           lambda inp: code2w(156, get_inp(inp, 1, "*"), "stop")],
]

@client.on_message
def recv_msg(msg):
    if msg.startswith(start):
        try:
            new = f.decrypt(msg[len(start):].encode()).decode()
            code, msg = int(new.split("§")[0]), "§".join(new.split("§")[1:])
            full_messages.append((code, msg))
            if code % 2 == 1: worker_messages.append((code, msg))
            else: master_messages.append((code, msg))
        except:
            full_messages.append(("-1", "decrypt error"))
            print("decrypt error")

def init(*args):
    global worker, worker_messages, master_messages, full_messages
    worker_messages = []
    master_messages = []
    full_messages = []
    worker = []

def ping(to_wait):
    secure_send(100, "ping")
    worker.clear()
    d = time()
    while to_wait > (time() - d):
        sleep(fonc_time)
        for m in worker_messages:
            if m[0] == 101:
                worker_messages.remove(m)
                if m[1] not in worker:
                    worker.append(m[1])
                    print(f" {m[1]} is online {round((time() - d)*1000)}ms")
    print(f"ping DONE!, {len(worker)} workers online")

def wait_reply(attendu, code, string1, max_wait=10):
    w = []
    s = []
    debut = time()
    while len(w) < attendu:
        sleep(fonc_time)
        for m in worker_messages:
            if m[0] != code:
                continue
            worker_messages.remove(m)
            info = m[1].split("§")
            if info[0] not in w:
                print(f"{info[0]} {string1}")
                w.append(info[0])
                s.append("§".join(info[1:]))
        if time() - debut > max_wait and max_wait != -1:
            return s, w, round((time() - debut) * 1000)
    return s, 0, round((time() - debut) * 1000)

def start_go(inp):
    def go(inp):
        def push(start, end, step, quantite):
            pool = util.read("fmaster/pool.py").split("#END#")[0]
            for n in range(quantite):
                secure_send(150, f"{worker[n]}§{start},{end},{step},{quantite},{n}§{pool}")
                print(f"send to {worker[n]}")
                sleep(send_time)

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

    def go_reply(exit_code):
        
        s, x, t = wait_reply(exit_code, 151, "starts work")
        if x == 0: print(f"all workers started in {t}ms")
        else:
            worker_messages.clear()
            return print(f"no reply from {find_diff(worker, x)} in {t}ms")

        s, x, t = wait_reply(exit_code, 153, "ends work", -1)
        print(f"all workers finished in {t}ms")
        worker_messages.clear()

        print(cros.main(s))

    exit_code = go(inp)
    if exit_code > 0:
        go_reply(exit_code)

def get_cpu_count():
    for w in worker:
        sleep(send_time)
        secure_send(102, w)
    s, x, t = wait_reply(len(worker), 103, "reply")
    if x == 0: print(f"all workers replied in {t}ms")
    else: print(f"no reply from {find_diff(worker, x)} in {t}ms")
    worker_messages.clear()
    total_cpu = 0
    for e in s:
        temp = e.split("§")
        print(f" {temp[0]} has {temp[1]} cores, {temp[2]}% usable")
        total_cpu += int(int(temp[1])*(int(temp[2])/100))
    print(f"total cpu count : {total_cpu}")

def speed():
    secure_send(104, "speed test")
    d = time()
    master_messages.clear()
    while True:
        sleep(0.001)
        for m in master_messages:
            if m[0] == 104:
                return print(f"DONE!, {round((time() - d)*1000)}ms")

def quit():
    try: client.close()
    except: pass
    sys.exit(0)

def code2w(code, wid, msg):
    try:
        w = [worker[int(wid)]] if wid != "*" else worker
        for e in w:
            sleep(send_time)
            secure_send(int(code), f"{e}§{msg}")
            print(f" {code} send to {e}")
    except:
        print("syntax or index error")

def shell():
    inp = input("\nMASTER > ").split(" ")
    for p in path:
        if inp[0] in p[0]:
            p[1](inp)
            inp = "in path"
            break
    if inp != "in path" and inp[0] != "":
        print("command not found")

print(util.entette)
init()
while True:
    try: shell()
    except KeyboardInterrupt: print("ctrl+c")