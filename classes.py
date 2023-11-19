import datetime
from config import *


class Inode:
  # header
  prop = grupo = None
  dtCri = dtAtu = dtUltAce = datetime.datetime.now()
  direitos = [bin(7), bin(0), bin(0)]
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
    self.direitos = [bin(7), bin(0), bin(0)]
    self.blocos = [] if self.ehDir else [bytearray(TAM_BLOCO) for _ in range(QTD_BLOCOS)]
    self.indirSimp = []

  def __str__(self):
    return f"{self.relNome()}"

  def info(self):
    self.atualizaTamanho()
    return f"{str(self)}  {'d' if self.ehDir else 'f'}{self.normalizaDireitos()}  {self.tamanho}  {self.prop.nome} {self.grupo.nome}"

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

  def setaDireito(self, novosDireitos):
    self.direitos = [bin(int(i)) for i in novosDireitos]

  def formata(self):
    self.blocos = [] if self.ehDir else [bytearray(TAM_BLOCO) for _ in range(QTD_BLOCOS)]

  def atualizaTamanho(self):
    self.tamanho = sum([len(b) - b.count(b"\x00") for b in self.blocos])


  def pai(self):
    if "/" == self.absNome: return None
    ridx = self.absNome.rindex("/", 0, len(self.absNome)-1)
    return self.absNome[:ridx] if ridx != 0 else self.absNome[0]
    # return self.absNome[:self.absNome.rindex("/", 0, len(self.absNome)-1)] if "/" != self.absNome else None

  def relNome(self):
    return self.absNome[self.absNome.rindex("/", 0, len(self.absNome)-1)+1:] if "/" != self.absNome else "/"


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
