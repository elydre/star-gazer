import os, sys

entette = """
  __  ______  ___  ____     ___   ___  ____  ____ ____ 
 (( \\ | || | // \\\\ || \\\\   // \\\\ // \\\\   // ||    || \\\\
  \\\\    ||   ||=|| ||_//  (( ___ ||=||  //  ||==  ||_//
 \\_))   ||   || || || \\\\   \\\\_|| || || //__ ||___ || \\\\
"""

path_v = os.path.dirname(sys.argv[0])

def read(chemain):
    with open(f'{path_v}/{chemain}' if sys.platform == "win32" else chemain, "r") as fil:
        code = fil.read()
    return code

def write(chemain, code):
    with open(f'{path_v}/{chemain}' if sys.platform == "win32" else chemain, "w") as fil:
        fil.write(code)

def generer_liste(start, end, step, quantite, n):
    listes = [[] for _ in range(quantite)]

    istep = 0
    ii = 0
    for i in range(start, end):

        listes[istep].append(i)
        ii += 1

        if ii == step:
            istep += 1
            ii = 0
        
        if istep == quantite:
            istep = 0
        
    if n == -1:
        return listes
    return listes[n]