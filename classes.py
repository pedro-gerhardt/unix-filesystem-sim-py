import datetime
from enum import Enum
from config import *


def _binToStrDireito(dir):
    return str(dir)[2:].zfill(3)


class Inode:
    # header
    prop = grupo = None
    dtCri = dtAtu = dtUltAce = datetime.datetime.now()
    direitos = [bin(7), bin(5), bin(0)]
    ehDir = False
    tamanho = 0
    absNome = ""

    # conteudo
    blocos = []
    indirSimp = []

    def __init__(self, nome, prop, ehDir=False):
        self.prop = self.grupo = prop
        self.dtCri = self.dtAtu = self.dtUltAce = datetime.datetime.now()
        self.ehDir = ehDir
        self.absNome = nome
        self.direitos = [bin(7), bin(5), bin(0)]
        self.blocos = [] if self.ehDir else [bytearray(TAM_BLOCO) for _ in range(QTD_BLOCOS_INT)]
        self.indirSimp = []

    def __str__(self):
        return f"{self.relNome()}"

    def info(self, listUser, inodes):
        self.atualizaTamanho(inodes)
        return f"{str(self)}  {'d' if self.ehDir else 'f'}{self.normalizaDireitos()}  {self.tamanho}  {listUser[self.prop].nome if self.prop in listUser else self.prop} {listUser[self.grupo].nome if self.grupo in listUser else self.grupo}"

    def data(self):
        return f"{str(self)}  {self.dtCri.isoformat(' ', 'seconds')}    {self.dtAtu.isoformat(' ', 'seconds')}    {self.dtUltAce.isoformat(' ', 'seconds')}"

    def normalizaDireitos(self):
        padrao = "rwx"
        saida = ""
        for dir in self.direitos:
            strDir = _binToStrDireito(dir)
            for i in range(len(strDir)):
                saida += f"{padrao[i] if strDir[i] == str(1) else '-'}"
        return saida

    def setaDireito(self, novosDireitos):
        self.direitos = [bin(int(i)) for i in novosDireitos]

    def formata(self):
        self.blocos = [] if self.ehDir else [bytearray(TAM_BLOCO) for _ in range(QTD_BLOCOS_INT)]

    def atualizaTamanho(self, inodes):
        self.tamanho = (
            len(self.blocos) * 4
            if self.ehDir
            else sum([len(b) - b.count(b"\x00") for b in self.blocos])
        )
        if not self.ehDir:
            for n in self.indirSimp:
                self.tamanho += len(inodes[n]) - inodes[n].count(b"\x00")


    def pai(self):
        if "/" == self.absNome:
            return None
        ridx = self.absNome.rindex("/", 0, len(self.absNome) - 1)
        return self.absNome[:ridx] if ridx != 0 else self.absNome[0]
        # return self.absNome[:self.absNome.rindex("/", 0, len(self.absNome)-1)] if "/" != self.absNome else None

    def relNome(self):
        return (
            self.absNome[self.absNome.rindex("/", 0, len(self.absNome) - 1) + 1 :]
            if "/" != self.absNome
            else "/"
        )

    def verificaPermissao(self, userId, acao):
        return (
            (_binToStrDireito(self.direitos[Agente.GERAL.value])[acao.value] != "0")
            or (
                self.grupo == userId
                and _binToStrDireito(self.direitos[Agente.GRUPO.value])[acao.value]
                != "0"
            )
            or (
                self.prop == userId
                and _binToStrDireito(self.direitos[Agente.PROPRIETARIO.value])[acao.value]
                != "0"
            )
        )

    def atualizaDataAtualizacao(self):
        self.dtUltAce = self.dtAtu = datetime.datetime.now()

    def atualizaDataAcesso(self):
        self.dtUltAce = datetime.datetime.now()


class User:
    id = 0
    nome = ""
    senha = ""

    def __init__(self, id, nome="", senha=""):
        self.id = id
        self.nome = nome
        self.senha = senha

    def __str__(self):
        return f"{self.id} - {self.nome}"


class Acao(Enum):
    LEITURA = 0
    ESCRITA = 1
    EXECUCAO = 2


class Agente(Enum):
    PROPRIETARIO = 0
    GRUPO = 1
    GERAL = 2
