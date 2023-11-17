import datetime
from config import * 

class Inode:
    # header 
    prop = grupo = pai = None
    dtCri = dtAtu = dtUltAce = datetime.datetime.now()
    direitos = [bin(7), bin(0), bin(0)]
    ehDir = False
    tamanho = 0
    nome = ""

    # conteudo
    blocos = []
    indirSimp = []

    def __init__(self, nome, prop, ehDir=False, pai=None):
        self.prop = self.grupo = prop
        self.dtCri = self.dtAtu = self.dtUltAce = datetime.datetime.now()
        self.ehDir = ehDir
        self.nome = nome
        self.pai = pai
        self.direitos = [bin(7), bin(0), bin(0)]
        self.blocos = [] if self.ehDir else [bytearray(TAM_BLOCO) for _ in range(QTD_BLOCOS)]
        self.indirSimp = []

    def __str__(self):
        return f"{self.nome + '/' if self.ehDir else self.nome}"

    def info(self):
        return f"{str(self)}  {'d' if self.ehDir else 'f'}{self.normalizaDireitos()}  {self.prop.nome} {self.grupo.nome}"

    def data(self):
        return f"{str(self)}  {self.dtCri.isoformat(' ', 'seconds')} {self.dtAtu.isoformat(' ', 'seconds')} {self.dtUltAce.isoformat(' ', 'seconds')}"

    def normalizaDireitos(self):
        padrao = "rwx"
        saida = ""
        for dir in self.direitos:
            strDir = str(dir)[2:].zfill(3)
            for i in range(len(strDir)):
                saida += f"{padrao[i] if strDir[i] == str(1) else '-'}"
        return saida

    def returnAbsolutePath(self):
        if self.pai is not None:
            return self.pai.returnAbsolutePath() + str(self)
        else:
            return str(self)

    def setaDireito(self, novosDireitos):
        self.direitos = [bin(int(i)) for i in novosDireitos]

    def formata(self):
        self.blocos = [] if self.ehDir else [bytearray(TAM_BLOCO) for _ in range(QTD_BLOCOS)]

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
    
