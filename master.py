from time import sleep
from cryptography.fernet import Fernet
import mod.key as key
from mod.POOcom import ClientCom

send_start = "!06!"
recv_start = "!07!"

done = False

f = Fernet(key.key) 

client = ClientCom()

secure_send = lambda msg: client.send(send_start + f.encrypt(msg.encode()).decode())

@client.on_message
def recv_msg(msg):
    if msg.startswith(recv_start):
        print(f.decrypt(msg[len(recv_start):].encode()).decode())
        global done
        done = True


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


secure_send(f'{pool}§list(range(1, 10000000))')

try:
    while not done:
        sleep(0.1)
except KeyboardInterrupt:
    client.close()