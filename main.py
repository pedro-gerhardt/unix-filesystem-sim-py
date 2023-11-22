import os
from classes import *
from config import *

# variaveis
userRoot = User(0, "root")
listUser = {0:userRoot}
user = userRoot

root = Inode("/", userRoot.id, True)
root.direitos = [bin(7), bin(7), bin(7)]
inode = root
inodes = {"/": root}

# funcao de apoio
def _montaPossivelNome(nome):
    return inode.absNome + nome if inode.absNome == "/" else inode.absNome + "/" + nome

def _montaNomePadraoBlocoIndireto(nomeAbs, idxBocInd):
    return nomeAbs + ".blocoInd" + str(idxBocInd)

# comandos
def pwd():
    print(inode.absNome)


def mkdir(cmds):
    if not inode.verificaPermissao(user.id, Acao.ESCRITA):
        print(MSG_PERM_INS); return
    if len(cmds) != 2:
        print(MSG_QTD_INV_PARAM); return
    nome = _montaPossivelNome(cmds[1])
    if nome in inodes and inodes[nome].ehDir:
        print(MSG_DIR_EXIST); return
    else:
        inodes[nome] = Inode(nome, user.id, True)
        inode.blocos.append(nome)
        inode.atualizaDataAtualizacao()



def touch(cmds):
    if not inode.verificaPermissao(user.id, Acao.ESCRITA):
        print(MSG_PERM_INS); return
    if len(cmds) != 2:
        print(MSG_QTD_INV_PARAM); return
    nome = _montaPossivelNome(cmds[1])
    if nome in inodes and not inodes[nome].ehDir:
        print(MSG_ARQ_EXIST); return
    else:
        inodes[nome] = Inode(nome, user.id, False)
        inode.blocos.append(nome)
        inode.atualizaDataAtualizacao()


def ls(cmds):
    if len(cmds) not in [1,2]:
        print(MSG_QTD_INV_PARAM); return
    if len(cmds) == 1:
        if not inode.verificaPermissao(user.id, Acao.LEITURA):
            print(MSG_PERM_INS); return
        for sd in inode.blocos:
            print(inodes[sd].info(listUser, inodes))
        inode.atualizaDataAcesso()
    elif len(cmds) == 2:
        nome = _montaPossivelNome(cmds[1])
        if nome in inode.blocos and inodes[nome].ehDir:
            if inodes[nome].verificaPermissao(user.id, Acao.LEITURA):
                for ssd in inodes[nome].blocos:
                    print(inodes[ssd].info(listUser, inodes))
                inodes[nome].atualizaDataAcesso()
            else:
                print(MSG_PERM_INS); return
        else:
            print(MSG_DIR_NAO_EXIST); return  

def cd(cmds):
    global inode
    if len(cmds) == 2:
        if cmds[1] == ".." and inode.pai() is not None:
            if inode.pai() not in inodes:
                print(MSG_DIR_NAO_EXIST); return
            if not inodes[inode.pai()].verificaPermissao(user.id, Acao.EXECUCAO):
                print(MSG_PERM_INS); return
            inode = inodes[inode.pai()]
            inode.atualizaDataAcesso()
            return
        nome = _montaPossivelNome(cmds[1])
        if nome in inode.blocos and nome in inodes and inodes[nome].ehDir:
            if not inodes[nome].verificaPermissao(user.id, Acao.EXECUCAO):
                print(MSG_PERM_INS); return
            inode = inodes[nome]
            inode.atualizaDataAcesso()
        else:
            print(MSG_DIR_NAO_EXIST); return
    else:
        print(MSG_QTD_INV_PARAM); return


def rm(cmds):
    if len(cmds) == 2:
        nome = _montaPossivelNome(cmds[1])
        if nome in inode.blocos and nome in inodes and not inodes[nome].ehDir:
            if inodes[nome].verificaPermissao(user.id, Acao.ESCRITA):
                inode.blocos.remove(nome)
                del inodes[nome]
                inode.atualizaDataAtualizacao()
            else:
                print(MSG_PERM_INS); return
        else:
            print(MSG_ARQ_NAO_EXIST); return
    else:
        print(MSG_QTD_INV_PARAM); return


def rmdir(cmds):
    if len(cmds) == 2:
        nome = _montaPossivelNome(cmds[1])
        if nome in inode.blocos and nome in inodes and inodes[nome].ehDir:
            if inodes[nome].verificaPermissao(user.id, Acao.ESCRITA):
                # passar por todos inodes e se no nome há o caminho do diretorio a ser excluido
                inode.blocos.remove(nome)
                del inodes[nome]
                dirApagar = []
                for i in inodes:
                    if i.count(nome) > 0:
                        dirApagar.append(i)
                for i in dirApagar:
                    del inodes[i]

                inode.atualizaDataAtualizacao()
            else:
                print(MSG_PERM_INS); return
        else:
            print(MSG_DIR_NAO_EXIST); return
    else:
        print(MSG_QTD_INV_PARAM); return


def adduser(cmds):
    if user.id != userRoot.id:
        print(MSG_PERM_INS); return
    if len(cmds) == 3:
        if not cmds[2].isdigit(): 
            print(MSG_ARG_INV); return
        if int(cmds[2]) in listUser:
            print("Usuário existente!"); return
        else:
            listUser[int(cmds[2])] = User(int(cmds[2]), cmds[1])
    else: 
        print(MSG_QTD_INV_PARAM); return


# remove por id
def rmuser(cmds):
    if user.id != userRoot.id:
        print(MSG_PERM_INS); return
    if len(cmds) == 2:
        if not cmds[1].isdigit(): 
            print(MSG_ARG_INV); return
        if int(cmds[1]) == 0:
            print("Não é possível remover o root!"); return
        if int(cmds[1]) in listUser:
            # chamar funcao para apagar todos arquivos que usuario é proprietario
            del listUser[int(cmds[1])]
        else:
            print("Usuário inexistente!"); return
    else: 
        print(MSG_QTD_INV_PARAM); return


def lsuser():
    if user.id != userRoot.id:
        print(MSG_PERM_INS); return
    for u in listUser.values():
        print(u)


def chown(cmds):
    if user.id != userRoot.id:
        print(MSG_PERM_INS); return
    if len(cmds) in [3, 4]:
        nome = _montaPossivelNome(cmds[-1])
        if nome in inode.blocos:
            for u in listUser.values():
                if u.nome == cmds[1]:
                    inodes[nome].prop = u.id
                    inodes[nome].atualizaDataAtualizacao()
                if len(cmds) == 4 and u.nome == cmds[2]:
                    inodes[nome].grupo = u.id
                    inodes[nome].atualizaDataAtualizacao()
        else:
            print(MSG_DIR_ARQ_NAO_EXIST); return
    else:
        print(MSG_QTD_INV_PARAM); return


def chmod(cmds):
    if user.id != userRoot.id:
        print(MSG_PERM_INS); return
    if len(cmds) == 3:
        nome = _montaPossivelNome(cmds[1])
        if nome in inode.blocos:
            inodes[nome].setaDireito(cmds[2])
            inodes[nome].atualizaDataAtualizacao()
        else:
            print(MSG_DIR_ARQ_NAO_EXIST); return
    else:
        print(MSG_QTD_INV_PARAM); return


def grava(cmds):
    if len(cmds) != 5:
        print(MSG_QTD_INV_PARAM); return
    _, nome, posicao, nbytes, buffer = cmds
    if not posicao.isdigit() or not nbytes.isdigit(): 
        print(MSG_ARG_INV); return
    posicao = int(posicao)
    nbytes = int(nbytes)
    blocos = blocosInd = nomesInd = None
    nomeAbs = _montaPossivelNome(nome)
    if nomeAbs in inodes and not inodes[nomeAbs].ehDir:
        if inodes[nomeAbs].verificaPermissao(user.id, Acao.ESCRITA):
            blocos = inodes[nomeAbs].blocos
            nomesInd = inodes[nomeAbs].indirSimp
            blocosInd = [] # talvez não iniciar aqui, mas somente se algum bloco indireto estiver sendo realmente usado
            for n in nomesInd:
                blocosInd.append(inodes[n])
            # for n in QTD_MAX_BLOCOS_IND:
            #     nomeBloco = _montaNomePadraoBlocoIndireto(nomeAbs, n) 
            #     if nomeBloco in inodes:
            #         blocosInd.append(inodes[nomeBloco])

        else:
            print(MSG_PERM_INS); return
    if blocos is None or nomesInd is None:
        print(MSG_ARQ_NAO_EXIST); return
    
    if posicao > TAM_TOTAL:
        print("Posição maior que o tamanho do disco!"); return

    bufferNumerico = [ord(s) for s in buffer]
    tamParcial = min(len(buffer), nbytes)
    idxBoc = posicao // TAM_BLOCO
    posBocInit = offsetStrInit = posicao - (idxBoc * TAM_BLOCO)
    idxStr = posStrInit = 0
    # posStrInit = idxStr * TAM_BLOCO

    if posicao + tamParcial > TAM_TOTAL:
        print("Tamanho do bloco maior que o tamanho do disco"); return
    
    inodes[nomeAbs].atualizaDataAtualizacao()

    while True:
        if idxBoc < QTD_BLOCOS_INT: 
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

        elif idxBoc >= QTD_BLOCOS_INT and idxBoc < QTD_BLOCOS_INT + QTD_MAX_BLOCOS_IND:
            idxBocInd = idxBoc - QTD_BLOCOS_INT 
            nomeInd = _montaNomePadraoBlocoIndireto(nomeAbs, idxBocInd)
            if nomeInd not in nomesInd:
                nomesInd.append(nomeInd)
                blocosInd.append(bytearray(TAM_BLOCO))
                
            if posBocInit + tamParcial <= TAM_BLOCO:
                blocosInd[idxBocInd][posBocInit:posBocInit + tamParcial] = bufferNumerico[posStrInit:posStrInit + tamParcial]
                for n in range(len(nomesInd)):
                    inodes[nomesInd[n]] = blocosInd[n]
                break
            else:
                blocosInd[idxBocInd][posBocInit:TAM_BLOCO] = bufferNumerico[posStrInit:posStrInit + min(tamParcial, TAM_BLOCO) - posBocInit]
                tamParcial -= min(tamParcial, TAM_BLOCO) - posBocInit
                idxBoc += 1
                posBocInit = 0
                idxStr += 1
                posStrInit = idxStr * TAM_BLOCO - offsetStrInit

        # ao final atualizar blocosInd novamente no dicionario principal
        else:
            print("Espaço do arquivo estorou!"); return



def cat(cmds):
    if len(cmds) == 2:
        nome = _montaPossivelNome(cmds[1])
        if nome in inodes and not inodes[nome].ehDir:
            if inodes[nome].verificaPermissao(user.id, Acao.LEITURA):
                strBlocosInt = "".join(["".join([chr(b) for b in bloco]) for bloco in inodes[nome].blocos])
                for n in inodes[nome].indirSimp:
                    strBlocosInt += "".join([chr(c) for c in inodes[n]])
                print(strBlocosInt)
                inodes[nome].atualizaDataAcesso()
            else:
                print(MSG_PERM_INS); return
        else:
           print(MSG_ARQ_NAO_EXIST); return
    else:
        print(MSG_QTD_INV_PARAM); return


def formata(cmds):
    if len(cmds) == 2:
        nome = _montaPossivelNome(cmds[1])
        if nome in inodes:
            if inodes[nome].verificaPermissao(user.id, Acao.ESCRITA):
                inodes[nome].formata()
                inodes[nome].atualizaDataAtualizacao()
            else:
                print(MSG_PERM_INS); return
        else:
            print(MSG_ARQ_NAO_EXIST); return
    else:
        print(MSG_QTD_INV_PARAM); return
    

# login id
def login(cmds):
    global user
    if len(cmds) == 2:
        if not cmds[1].isdigit():
            print(MSG_ARG_INV); return
        if int(cmds[1]) in listUser:
            user = listUser[int(cmds[1])]
        else:
            print("Usuário não encontrado!"); return
    else:
        print(MSG_QTD_INV_PARAM); return


def lsd(cmds):
    if len(cmds) not in [1,2]:
        print(MSG_QTD_INV_PARAM); return
    if len(cmds) == 1:
        if not inode.verificaPermissao(user.id, Acao.LEITURA):
            print(MSG_PERM_INS); return
        for sd in inode.blocos:
            print(inodes[sd].data())
        inode.atualizaDataAcesso()
    elif len(cmds) == 2:
        nome = _montaPossivelNome(cmds[1])
        if nome in inode.blocos and inodes[nome].ehDir:
            if inodes[nome].verificaPermissao(user.id, Acao.LEITURA):
                for ssd in inodes[nome].blocos:
                    print(inodes[ssd].data())
                inodes[ssd].atualizaDataAcesso()
            else:
                print(MSG_PERM_INS); return
        else:
            print(MSG_DIR_NAO_EXIST); return  


def main():
  while True:
    comando = input(user.nome + ":" + inode.absNome + "# ")
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
    elif cmds[0] == "login":
        login(cmds)
    elif cmds[0] == "lsd":
        lsd(cmds)
    elif cmds[0] == "print":
        print(inodes)
    
    else:
       print("Comando desconhecido!")


main()
