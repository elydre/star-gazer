# fonction pool
def do(n):
    if n == 2:
        return n
    if n % 2 == 0:
        return False
    return next((False for i in range(3, int(n**0.5)+1, 2) if n % i == 0), n)

# fonction de rasemblement dans worker
def centre(l):
    k = [e for e in l if e != False]
    return len(k)

#END# balise de fin de fichier transmis au worker

# fonction de rasemblement dans master
def cros(l):
    return sum(int(e) for e in l)