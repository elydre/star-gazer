# star-gazer
pooling multi machine


## send code

| code | description               |
| ---- | ------------------------- |
| 100  | ping                      |
| 101  | reponse du worker au ping |
| 150  | demande de travail        |
| 151  | travail disponible        |
| 152  | reponse du travail        |

### 150

```
150§destination§start,end,step,quantite,n§fonctions
```