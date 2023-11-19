import os
from classes import User, Inode
from config import *

# variaveis
userRoot = User(0, "root")
listUser = {0:userRoot}
user = userRoot

root = Inode("/", userRoot, True)
inode = root
inodes = {"/": root}

# funcao de apoio
def _montaPossivelNome(nome):
    return inode.absNome + nome if inode.absNome == "/" else inode.absNome + "/" + nome

# comandos
def pwd():
    print(inode.absNome)


def mkdir(cmds):
    if len(cmds) != 2:
        print(MSG_QTD_INV_PARAM); return
    nome = _montaPossivelNome(cmds[1])
    if nome in inodes and inodes[nome].ehDir:
        print(MSG_DIR_EXIST); return
    else:
        inodes[nome] = Inode(nome, user, True)
        inode.blocos.append(nome)


def touch(cmds):
    if len(cmds) != 2:
        print(MSG_QTD_INV_PARAM); return
    nome = _montaPossivelNome(cmds[1])
    if nome in inodes and not inodes[nome].ehDir:
        print(MSG_ARQ_EXIST); return
    else:
        inodes[nome] = Inode(nome, user, False)
        inode.blocos.append(nome)


def ls(cmds):
    if len(cmds) not in [1,2]:
        print(MSG_QTD_INV_PARAM); return
    if len(cmds) == 1:
        for sd in inode.blocos:
            print(inodes[sd].info())
    elif len(cmds) == 2:
        nome = _montaPossivelNome(cmds[1])
        if nome in inode.blocos and inodes[nome].ehDir:
            for ssd in inodes[sd.absNome].blocos:
                print(inodes[ssd].info())
        else:
            print(MSG_DIR_NAO_EXIST); return  


def cd(cmds):
    global inode
    if len(cmds) == 2:
        if cmds[1] == ".." and inode.pai() is not None:
            inode = inodes[inode.pai()]; return
        nome = _montaPossivelNome(cmds[1])
        if nome in inode.blocos and nome in inodes and inodes[nome].ehDir:
            inode = inodes[nome]
        else:
            print(MSG_DIR_NAO_EXIST); return
    else:
        print(MSG_QTD_INV_PARAM); return


def rm(cmds):
  if len(cmds) == 2:
    nome = _montaPossivelNome(cmds[1])
    if nome in inode.blocos and nome in inodes and not inodes[nome].ehDir:
        inode.blocos.remove(nome)
        del inodes[nome]
    else:
      print(MSG_ARQ_NAO_EXIST); return
  else:
    print(MSG_QTD_INV_PARAM); return


def rmdir(cmds):
    if len(cmds) == 2:
        nome = _montaPossivelNome(cmds[1])
        if nome in inode.blocos and nome in inodes and inodes[nome].ehDir:
            inode.blocos.remove(nome)
            del inodes[nome]
        else:
            print(MSG_DIR_NAO_EXIST); return
    else:
        print(MSG_QTD_INV_PARAM); return


def adduser(cmds):
    if len(cmds) == 3:
        if int(cmds[2]) in listUser:
            print("Usuário existente!"); return
        else:
            listUser[int(cmds[2])] = User(int(cmds[2]), cmds[1])
    else: 
        print(MSG_QTD_INV_PARAM); return


# remove por id
def rmuser(cmds):
    if len(cmds) == 2:
        if int(cmds[1]) in listUser:
            # chamar funcao para apagar todos arquivos que usuario é proprietario
            del listUser[int(cmds[1])]
        else:
            print("Usuário inexistente!"); return
    else: 
        print(MSG_QTD_INV_PARAM); return


def lsuser():
    for u in listUser.values():
        print(u)


def chown(cmds):
    if len(cmds) in [3, 4]:
        nome = _montaPossivelNome(cmds[-1])
        if nome in inode.blocos:
            for u in listUser.values():
                if u.nome == cmds[1]:
                    inodes[nome].prop = u
                if len(cmds) == 4 and u.nome == cmds[2]:
                    inodes[nome].grupo = u
        else:
            print(MSG_DIR_ARQ_NAO_EXIST); return
    else:
      print(MSG_QTD_INV_PARAM); return


def chmod(cmds):
    if len(cmds) == 3:
        nome = _montaPossivelNome(cmds[1])
        if nome in inode.blocos:
            inodes[nome].setaDireito(cmds[2])
        else:
            print(MSG_DIR_ARQ_NAO_EXIST); return
    else:
        print(MSG_QTD_INV_PARAM); return


def grava(cmds):
    if len(cmds) != 5:
        print(MSG_QTD_INV_PARAM); return
    _, nome, posicao, nbytes, buffer = cmds
    posicao = int(posicao)
    nbytes = int(nbytes)
    if posicao > (QTD_BLOCOS * TAM_BLOCO):
        print("Erro: posicao maior que o tamanho do disco"); return
    blocos = None
    nomeAbs = _montaPossivelNome(nome)
    if nomeAbs in inodes and not inodes[nomeAbs].ehDir:
        blocos = inodes[nomeAbs].blocos
    if blocos is None:
        print(MSG_ARQ_NAO_EXIST); return

    bufferNumerico = [ord(s) for s in buffer]
    tamParcial = min(len(buffer), nbytes)
    idxBoc = posicao // TAM_BLOCO
    posBocInit = offsetStrInit = posicao - (idxBoc * TAM_BLOCO)
    idxStr = 0
    posStrInit = idxStr * TAM_BLOCO

    if posicao + tamParcial > TAM_TOTAL:
        print("Tamanho do bloco maior que o tamanho do disco"); return

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
        nome = _montaPossivelNome(cmds[1])
        if nome in inodes and not inodes[nome].ehDir:
            print("".join(["".join([chr(b) for b in bloco]) for bloco in inodes[nome].blocos]))
        else:
           print(MSG_ARQ_NAO_EXIST); return
    else:
        print(MSG_QTD_INV_PARAM); return


def formata(cmds):
    if len(cmds) == 2:
        nome = _montaPossivelNome(cmds[1])
        if nome in inodes:
            inodes[nome].formata()
    else:
        print(MSG_QTD_INV_PARAM); return


def main():
  while True:
    comando = input(inode.absNome + "# ")
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
    else:
       print("Comando desconhecido!")


main()
