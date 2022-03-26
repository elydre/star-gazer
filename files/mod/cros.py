import mod.util as util

def main(l):
    code = util.read("fmaster/pool.py").split("#END#")
    if len(code) == 1:
        print("pas la balise de fin dans code.py - #END#")
        return False
    else:
        exec(f"#{code[1]}")
        return eval("cros(l)")