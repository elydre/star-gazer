from cryptography.fernet import Fernet
import mod.key as key
from mod.POOcom import ClientCom

start = "!06!"

f = Fernet(key.key) 

client = ClientCom()


@client.on_message
def recv_msg(msg):
    if msg.startswith(start):
        new = f.decrypt(msg[len(start):].encode()).decode()
        print(f"{new}")

try:
    while True: input()
except KeyboardInterrupt:
    client.close()