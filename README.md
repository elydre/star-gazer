# star-gazer
pooling multi machine

## commande master

```
CAT         affiche le contenu de pool.py
CLEAR       clear screen
CPU         get cpu count of all workers
EXIT        quitte le programme
GO          lance le travail
HELP        affiche cette aide
INIT        reinitialise le programme
LW          affiche la liste des workers
MF          affiche l'historique des messages
MM          affiche les messages du master
MW          affiche les messages des workers
PING/GET    recupère la liste des workers
PRINT       affiche un message chez les workers
SPEED       la latence master-msg-master
SW          stop tout les workers
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
| 156  | arrete des workers        |

### 150

```
150§destination§start,end,step,quantite,n§fonctions
```

## print

| alias | description |
| ----- | ----------- |
| %     | \n          |
| $     | worker name |