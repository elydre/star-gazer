# star-gazer
pooling multi machine

```
     |
,---.|--- ,---.,---.   ,---.,---.,---,,---.,---.
`---.|    ,---||    ---|   |,---| .-' |---'|
`---'`---'`---^`       `---|`---^'---'`---'`
• berlin               `---'
```

## disclamer

~~yellow~~-star-gazer est un projet bienveillant, comme il~~s~~ ne doi~~ven~~t pas se rependre~~nt~~

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
SPEED       la latence master-msg-master
SW          stop tout les workers
```

## path

```py
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