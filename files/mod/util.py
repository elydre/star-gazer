from cryptography.fernet import Fernet
import os, sys

entette = """
     |
,---.|--- ,---.,---.   ,---.,---.,---,,---.,---.
`---.|    ,---||    ---|   |,---| .-' |---'|
`---'`---'`---^`       `---|`---^'---'`---'`
                       `---'
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

def loadkey():
    try:
        return read("mod/key.txt").encode()
    except:
        print("key.txt not found, press enter to generate a new key or paste your own key")
        key = input("KEY > ")
        if key == "":
            print("generating key...")
            key = Fernet.generate_key().decode()
        write("mod/key.txt", key)
        return key