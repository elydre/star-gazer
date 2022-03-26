# star-gazer
pooling multi machine

## commande master

```
CLEAR       clear screen
EXIT        quitte le programme
GO          lance le travail
HELP        affiche cette aide
LW          affiche la liste des workers
MM          affiche les messages du master
PING/GET    recupère la liste des workers
WM          affiche les messages des workers
```

## send code

| code | description               |
| ---- | ------------------------- |
| 100  | ping                      |
| 101  | reponse du worker au ping |
| 150  | demande de travail        |
| 151  | travail disponible        |
| 153  | reponse du travail        |
| 154  | demande de print          |

### 150

```
150§destination§start,end,step,quantite,n§fonctions
```