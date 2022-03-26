import os, sys

path_v = os.path.dirname(sys.argv[0])

def read(chemain):
    with open(f'{path_v}/{chemain}' if sys.platform == "win32" else chemain, "r") as fil:
        code = fil.read()
    return code

def write(chemain, code):
    with open(f'{path_v}/{chemain}' if sys.platform == "win32" else chemain, "w") as fil:
        fil.write(code)