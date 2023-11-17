import os
from classes import User, Inode
from config import *

# variaveis
userRoot = User(0, "root")
listUser = [userRoot]
user = userRoot

root = Inode("", userRoot, True)
inode = root

# comandos
def pwd():
    print(inode.returnAbsolutePath())

def mkdir(cmds):
    if len(cmds) > 1:
        inode.blocos.append(Inode(cmds[1], user, True, inode))

def touch(cmds):
    if len(cmds) > 1:
        inode.blocos.append(Inode(cmds[1], user, False, inode))

def ls(cmds):
    if len(cmds) == 1:
        for sd in inode.blocos:
            print(sd.info())
    elif len(cmds) == 2:
        if cmds[1] == "-d":
            for sd in inode.blocos:
                print(sd.data())
        else:
            for sd in inode.blocos:
                if sd.nome == cmds[1]:
                    for ssd in sd.blocos:
                        print(ssd)
    elif len(cmds) == 3:
        if cmds[2] == "-d":
            for sd in inode.blocos:                
                if sd.nome == cmds[1]:
                    for ssd in sd.blocos:
                        print(ssd.data())

def cd(cmds):
    global inode
    if len(cmds) > 1:
        if cmds[1] == ".." and inode.pai is not None:
            inode = inode.pai
        else:
            for d in inode.blocos:
                if d.nome == cmds[1]:
                    inode = d

def rm(cmds):
    if len(cmds) > 1:
        for d in inode.blocos:
            if d.nome == cmds[1] and not d.ehDir:
                inode.blocos.remove(d)

def rmdir(cmds):
    if len(cmds) > 1:
        for d in inode.blocos:
            if d.nome == cmds[1] and d.ehDir:
                inode.blocos.remove(d)

def adduser(cmds): 
    global USER_ID_INC
    if len(cmds) == 2:
        listUser.append(User(USER_ID_INC, cmds[1]))
        USER_ID_INC += 1
    if len(cmds) == 3:
        listUser.append(User(int(cmds[2]), cmds[1]))

def rmuser(cmds): 
    if len(cmds) > 1:
        for u in listUser:
            if u.nome == cmds[1]:
                listUser.remove(u)

def lsuser():
    for u in listUser:
        print(u)

def chown(cmds):
    if len(cmds) in [3, 4]:
        for d in inode.blocos:
            if d.nome == cmds[-1]:
                for u in listUser:
                    if u.nome == cmds[1]:
                        d.prop = u
                    if len(cmds) == 4 and u.nome == cmds[2]:
                        d.grupo = u

def chmod(cmds):
    if len(cmds) == 3:
        for d in inode.blocos:
            if d.nome == cmds[1]:
                d.setaDireito(cmds[2])
                continue
        print("Erro: Diretório/Arquivo não encontrado")
    else:
        print("Erro: Número de argumentos inválido")
        
def grava(cmds):
    if len(cmds) != 5:
        print("Quantidade de parâmetros incorreta!"); return
    _, nome, posicao, nbytes, buffer = cmds        
    posicao = int(posicao)
    nbytes = int(nbytes)
    if posicao > (QTD_BLOCOS * TAM_BLOCO):
        print("Erro: posicao maior que o tamanho do disco"); return
    blocos = None    
    for d in inode.blocos:
        if d.nome == nome and not d.ehDir:
            blocos = d.blocos
    if blocos is None:
        print("Arquivo não encontrado!"); return
    
    bufferNumerico = [ord(s) for s in buffer]
    tamParcial = min(len(buffer), nbytes)
    idxBoc = posicao // TAM_BLOCO
    posBocInit = offsetStrInit = posicao - (idxBoc * TAM_BLOCO)
    idxStr = 0
    posStrInit = idxStr * TAM_BLOCO

    if posicao + tamParcial > TAM_TOTAL:
        print("Tamanho do bloco maior que o tamanho do disco")
        return

    while True:
        if posBocInit + tamParcial <= TAM_BLOCO:
            blocos[idxBoc][posBocInit:posBocInit + tamParcial] = bufferNumerico[posStrInit:posStrInit + tamParcial]
            break
        else:
            blocos[idxBoc][posBocInit:TAM_BLOCO] = bufferNumerico[posStrInit:posStrInit + min(tamParcial, TAM_BLOCO) - posBocInit]
            tamParcial -= min(tamParcial, TAM_BLOCO) - posBocInit
            idxBoc += 1
            posBocInit = 0
            idxStr += 1
            posStrInit = idxStr * TAM_BLOCO - offsetStrInit

def cat(cmds): 
    if len(cmds) == 2:
        for d in inode.blocos:
            if d.nome == cmds[1] and not d.ehDir:
                print("".join(["".join([chr(b) for b in bloco]) for bloco in d.blocos]))

def formata(cmds): 
    if len(cmds) == 2:
        for d in inode.blocos:
            if d.nome == cmds[1]:
                d.formata()



def main():
    global inode, user, listUser

    while True:
        comando = input(inode.returnAbsolutePath() + "# ")
        cmds = comando.split()
        
        if cmds[0] == "pwd":
            pwd()
        elif cmds[0] == "mkdir":
            mkdir(cmds)
        elif cmds[0] == "touch":
            touch(cmds)
        elif cmds[0] == "ls":
            ls(cmds)
        elif cmds[0] == "cd":
            cd(cmds)
        elif cmds[0] == "rm":
            rm(cmds)
        elif cmds[0] == "rmdir":
            rmdir(cmds)
        elif cmds[0] == "adduser":
            adduser(cmds)
        elif cmds[0] == "rmuser":
            rmuser(cmds)
        elif cmds[0] == "lsuser":
            lsuser()
        elif cmds[0] == "c":
            os.system('clear')
        elif cmds[0] == "chown":
            chown(cmds)
        elif cmds[0] == "chmod":
            chmod(cmds)
        elif cmds[0] == "grava":
            grava(cmds)
        elif cmds[0] == "cat":
            cat(cmds)
        elif cmds[0] == "formata":
            formata(cmds)


main()



