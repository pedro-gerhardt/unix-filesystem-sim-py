import os
from classes import User, Inode

# variaveis
userRoot = User(0, "root")
listUser = [userRoot]
user = userRoot
userIdInc = 1

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
        for sd in inode.blocos:
            if sd.nome == cmds[1]:
                for ssd in sd.blocos:
                    print(ssd)

def cd(cmds):
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
    if len(cmds) == 2:
        listUser.append(User(userIdInc, cmds[1]))
        userIdInc += 1
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
        
# gravar_conteudo(nome, posição, nbytes, buffer)
def grava(cmds):
    if len(cmds) == 4:
        for d in inode.blocos:
            if d.nome == cmds[0] and not d.ehDir:
                for c in cmds[3]:
                    # a terminar



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


main()



