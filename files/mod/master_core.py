import contextlib
import sys
from _thread import start_new_thread
from math import ceil
from time import sleep, time

from cryptography.fernet import Fernet

import mod.cros as cros
import mod.util as util
from mod.POOcom import ClientCom

f = Fernet(util.loadkey())
client = ClientCom()

find_diff = lambda l1, l2: [e for e in l1 if e not in l2]
get_inp = lambda inp, id, default: default if len(inp) <= id else inp[id]
secure_send = lambda code, msg: client.send(start + f.encrypt(f"{code}§{msg}".encode()).decode())
msg_history = lambda msg: "\n".join([":".join([str(f) for f in e]) for e in msg])

STOP = True
start = "!06!"
fonc_time = 0.05
send_time = 0.1

def set_var(var, val):
    global fonc_time, send_time, start, STOP
    if var == "fonc": fonc_time = val
    elif var == "send": send_time = val
    elif var == "start": start = val
    elif var == "STOP": STOP = val
    else: print("unknown var")

@client.on_message
def recv_msg(msg):
    if msg.startswith(start):
        try:
            new = f.decrypt(msg[len(start):].encode()).decode()
            code, msg = int(new.split("§")[0]), "§".join(new.split("§")[1:])
            full_messages.append((code, msg))
            if code % 2 == 1: worker_messages.append((code, msg))
            else: master_messages.append((code, msg))
        except Exception:
            full_messages.append(("-1", "decrypt error"))
            print("decrypt error")

def init(*args):
    global worker, worker_messages, master_messages, full_messages, STOP
    STOP = True
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

def wait_reply(attendu, code, string1, max_wait=10, special_worker=0):
    w = []
    s = []
    debut = time()
    while len(w) < attendu:
        sleep(fonc_time)
        for m in worker_messages:
            if m[0] != code:
                continue
            info = m[1].split("§")
            if special_worker != 0 and info[0] != special_worker:
                continue
            worker_messages.remove(m)
            if info[0] not in w:
                if string1 != -1:
                    print(f"{info[0]} {string1}")
                w.append(info[0])
                s.append("§".join(info[1:]))
        if time() - debut > max_wait and max_wait != -1:
            return s, w, round((time() - debut) * 1000)
    return s, 0, round((time() - debut) * 1000)

def start_igo(inp):                     # sourcery no-metrics
    def igo(start, end, k, step):
        def w_reply(w):
            s, x, t = wait_reply(1, 151, -1, 5, w)
            wstat[w][0] = 2 if x == 0 else -1
            if x != 0:
                TD[wstat[w][1]][0] = 0
                return
            TD[wstat[w][1]][0] = 2
            s, x, t = wait_reply(1, 153, -1, -1, w)
            wstat[w][0], TD[wstat[w][1]][0] = 0, 3
            sortie.append(s[0])

        def print_stat():
            print(
                " WORKERS:\n",
                sum(wstat[w][0] == 0 for w in worker),
                "workers idle\n",
                sum(wstat[w][0] == 1 for w in worker),
                "workers checking\n",
                sum(wstat[w][0] == 2 for w in worker),
                "workers working\n",
                sum(wstat[w][0] == -1 for w in worker),
                "workers dead\n",
                "\nLISTE:\n",
                sum(TD[x][0] == 0 for x in range(kq)),
                "liste en attente\n",
                sum(TD[x][0] == 1 for x in range(kq)),
                "liste en demarage\n",
                sum(TD[x][0] == 2 for x in range(kq)),
                "liste en cours\n",
                sum(TD[x][0] == 3 for x in range(kq)),
                "liste finis",
            )

        def printer():

            print("\n"*10)
            while sum(TD[x][0] == 3 for x in range(kq)) < kq and not STOP:
                [[util.go_up(), util.clear_line()] for _ in range(11)]
                print_stat()
                sleep(1)

        global STOP
        STOP = False
        debut = time()
        kq = ceil(k * ((end - start) // step) / 1000)
        kq = max(kq, len(worker))
        print(f"{kq} jobs to do")
        wstat = {e: [0, -1] for e in worker}
        sortie = []
        TD = [[0, start, end, step, kq, n] for n in range(kq)]
        iTD = 0

        start_new_thread(printer, ())

        try:
            while sum(TD[x][0] == 3 for x in range(kq)) < kq:
                for e in wstat:
                    while wstat[e][0] == 0 and iTD < kq:
                        if TD[iTD][0] == 0:
                            TD[iTD][0] = 1
                            secure_send(150, f"{e}§{TD[iTD][1]},{TD[iTD][2]},{TD[iTD][3]},{TD[iTD][4]},{TD[iTD][5]}§" + util.read("fmaster/pool.py").split("#END#")[0])
                            wstat[e][0] = 1
                            wstat[e][1] = iTD
                            start_new_thread(w_reply, (e,))
                        iTD += 1
                        sleep(send_time)
                    if iTD == kq:
                        iTD = 0

                sleep(fonc_time)

            [[util.go_up(), util.clear_line()] for _ in range(11)]
            print_stat()

            print(f"FINISHED in {round((time() - debut) * 1000)}ms")
            print(cros.main(sortie))
        except KeyboardInterrupt:
            STOP = True
            print("^C - STOPPED")

    inp = ["igo"] + [int(e) for e in inp[1:]]

    if len(inp) == 1:
        print("go <end>")
        print("go <end> <nb list/10k>")
        print("go <start> <end> <nb list/10k>")
        print("go <start> <end> <nb list/10k> <step>")
        print("go <start> <end> <nb list/10k> <step>")
        return -1
    if len(inp) == 2:
        igo(0, inp[1], 10, 10)
    elif len(inp) == 3:
        igo(0, inp[1], inp[2], 10)
    elif len(inp) == 4:
        igo(inp[1], inp[2], inp[3], 10)
    elif len(inp) in {5, 6}:
        igo(inp[1], inp[2], inp[3], inp[4])
    else:
        print("Syntax error")
        return -1

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
    with contextlib.suppress(Exception):
        client.close()
    sys.exit(0)

def code2w(code, wid, msg):
    try:
        w = [worker[int(wid)]] if wid != "*" else worker
        for e in w:
            sleep(send_time)
            secure_send(int(code), f"{e}§{msg}")
            print(f" {code} send to {e}")
    except Exception:
        print("syntax or index error")
