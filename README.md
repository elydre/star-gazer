# star-gazer
pooling multi machine

```
     |
,---.|--- ,---.,---.   ,---.,---.,---,,---.,---.
`---.|    ,---||    ---|   |,---| .-' |---'|
`---'`---'`---^`       `---|`---^'---'`---'`
 hole                  `---'
```

# MASTER

## commande master

```
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
```

## path

```py
path = [
[["cat"],                   lambda inp: print(util.read("fmaster/pool.py"))],
[["clear", "cls"],          lambda inp: os.system('cls' if os.name == 'nt' else 'clear')],
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
```

## send code

| code | description               |
| ---- | ------------------------- |
| 100  | ping                      |
| 101  | reponse au 100            |
| 102  | get cpu count             |
| 103  | reponse du 102            |
| 104  | speed master-master       |
| 150  | demande de travail        |
| 151  | reponse au 150            |
| 153  | reponse du travail        |
| 154  | demande de print          |
| 156  | arret des workers         |
| 158  | edit % cpu usable         |


### 150

```
150§destination§start,end,step,quantite,n§fonctions
```

## print

| alias | description |
| ----- | ----------- |
| %     | `"\n"`      |
| $     | worker name |
| #     | `"\n"*100`  |

# WORKER-DOCKER

## create image

```
docker build -t star-gazer .
```

## execute

```
docker run --name w1 star-gazer
```
