from time import sleep, time
from cryptography.fernet import Fernet
import mod.key as key
from mod.POOcom import ClientCom
import os

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


pool = """
def do(n):
    if n == 2:
        return n
    if n % 2 == 0:
        return False
    return next((False for i in range(3, int(n**0.5)+1, 2) if n % i == 0), n)

def centre(l):
    k = [e for e in l if e != False]
    return len(k)
"""

#secure_send(f'{pool}§list(range(1, 10000000))')

def shell():
    while True:
        get_inp = lambda inp, id, default: default if len(inp) <= id else inp[id]

        inp = input("MASTER > ").split(" ")
        cmd = inp[0]
        if cmd == "exit":
            client.close()
            return
        elif cmd == "msg":
            print(messages)
        elif cmd == "ping":
            secure_send(100, "ping")
            worker.clear()
            d = time()
            while int(get_inp(inp, 1, 5)) > (time() - d):
                sleep(0.05)
                for m in messages:
                    if m[0] == 101:
                        messages.remove(m)
                        worker.append(m[1])
                        print(f"{m[1]} is online {round((time() - d)*1000)}ms")
            print(f"ping DONE!, {len(worker)} workers online")
        elif cmd == "lw":
            print(f"{len(worker)} workers in list")
            print("\n".join(worker))
        elif cmd == "clear":
            os.system("cls")
        else:
            print("commande inconnue")


try:
    while True:
        shell()
except KeyboardInterrupt:
    client.close()