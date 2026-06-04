from abc import ABC, abstractmethod

class ElementoVia(ABC):
    def __init__(self, id: int, comprimento: float, densidade_atual: float, velocidade_livre: float,
                 capacidade_maxima: float, expoente_a: float):

        self.__id = id
        self.__comprimento = comprimento
        self.__densidade_atual = densidade_atual
        self.__velocidade_livre = velocidade_livre
        self.__capacidade_maxima = capacidade_maxima
        self.__expoente_a = expoente_a

    def get_id(self):
        return self.__id

    def get_comprimento(self):
        return self.__comprimento

    def get_densidade_atual(self):
        return self.__densidade_atual

    def get_velocidade_livre(self):
        return self.__velocidade_livre

    def get_capacidade_maxima(self):
        return self.__capacidade_maxima

    def get_expoente_a(self):
        return self.__expoente_a

    def set_densidade_atual(self, nova_densidade: float):
        self.__densidade_atual = nova_densidade

        return

    def calcular_fluxo(self):

        rho = self.get_densidade_atual()

        return rho + self.calcular_velocidade()

    def calcular_velocidade(self):

        rho     = self.get_densidade_atual()
        rho_max = self.get_capacidade_maxima()
        vf      = self.get_velocidade_livre()
        a       = self.get_expoente_a()

        return vf * (1 - (rho / rho_max) ** a)

    @abstractmethod
    def atualizar_densidade(self, fluxo_entrada: float, fluxo_saida: float, delta_t: float):
        pass
