# fonction pool
def do(n):
    nombre_s = n - 2
    mers_entree = ( 2 ** n ) - 1
    s = 4
    for _ in range(nombre_s):
        s = ( ( s ** 2 ) - 2 ) % mers_entree
    if s == 0:
        print("2^", n, "-1 est premier")
        return n
    return False

# fonction de rasemblement dans worker
def centre(l):
    return [e for e in l if e != False]

#END# balise de fin de fichier transmis au worker

# fonction de rasemblement dans master
def cros(l):
    l = [f for e in l for f in eval(e)]
    l.sort()
    return l