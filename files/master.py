'''    _             _
  ___ | | _   _   __| | _ __   ___
 / _ \| || | | | / _` || '__| / _ |
|  __/| || |_| || (_| || |   |  __/
 \___||_| \__, | \__,_||_|    \___|
          |___/
___________________________________

 - codé en : UTF-8
 - langage : python3
 - GitHub  : github.com/elydre
 - Licence : GNU GPL v3
'''

import mod.master_core as mc
import mod.util as util

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
SPEED       test la latence master-POOcom-master
SW          stop tout les workers
"""

mc.set_var("fonc", 0.05)
mc.set_var("send", 0.1)

path = [
[["cat"],                   lambda inp: print(util.read("fmaster/pool.py"))],
[["clear", "cls"],          lambda inp: util.clear()],
[["cpu", "lscpu"],          lambda inp: mc.get_cpu_count()],
[["exit", "quit", "q"],     lambda inp: quit()],
[["go", "igo"],             lambda inp: mc.start_igo(inp)],
[["help", "?"],             lambda inp: print(cmd_help)],
[["init", "r"],             lambda inp: mc.init(print("init done"))],
[["key"],                   lambda inp: print(util.loadkey().decode())],
[["lw", "w"],               lambda inp: print(f"{len(mc.worker)} workers:\n", "\n ".join([f"{mc.worker.index(w)}. {w}" for w in mc.worker]))],
[["mf"],                    lambda inp: print(mc.msg_history(mc.full_messages))],
[["mm"],                    lambda inp: print(mc.msg_history(mc.master_messages))],
[["mw"],                    lambda inp: print(mc.msg_history(mc.worker_messages))],
[["perf", "%"],             lambda inp: mc.code2w(158, mc.get_inp(inp, 1, "*"), mc.get_inp(inp, 2, 100))],
[["ping", "get"],           lambda inp: mc.ping(int(mc.get_inp(inp, 1, 3)))],
[["print"],                 lambda inp: mc.code2w(154, mc.get_inp(inp, 1, "*"), mc.get_inp(inp, 2, "%master print"))],
[["speed"],                 lambda inp: mc.speed()],
[["stopw", "sw"],           lambda inp: mc.code2w(156, mc.get_inp(inp, 1, "*"), "stop")],
]

def shell():
    inp = input("\nMASTER > ").split(" ")
    for p in path:
        if inp[0] in p[0]: return p[1](inp)
    if inp[0] != "":
        print("command not found")

print(util.entette)
mc.init()
while True:
    try: shell()
    except KeyboardInterrupt:
        mc.set_var("stop", True)
        print("ctrl+c")
