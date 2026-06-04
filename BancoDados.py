import json
import os

class BancoDados:
    def __init__(self):

        self.__pasta = "cenarios"

        if not os.path.exists(self.__pasta):
            os.makedirs(self.__pasta)

    def salvar_cenario(self, nome_cenario, dados):

        caminho = f"{self.__pasta}/{nome_cenario}.json"

        with open(caminho, "w", encoding = "utf-8") as arquivo:

            json.dump(dados, arquivo, indent = 4)

    def carregar_cenarios(self, nome_cenario):

        caminho = f"{self.__pasta}/{nome_cenario}.json"

        with open(caminho, "r", encoding = "utf-8") as arquivo:

            return json.load(arquivo)
