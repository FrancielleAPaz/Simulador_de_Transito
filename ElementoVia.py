from abc import ABC, abstractmethod

# Classe abstrata que representa um elemento genérico da via.
# Serve como base para segmentos principais, semáforos, entradas, saídas etc, por exemplo.
class ElementoVia(ABC):
    def __init__(self, id: int, comprimento, densidade_atual, velocidade_livre, capacidade_maxima, expoente_a):

        # Validação do identificador
        if not isinstance(id, int):
            raise TypeError("O identificador deve ser um inteiro!")

        if id < 0:
            raise ValueError("O identificador deve ser um número natural!")

        # Validação do comprimento
        if not isinstance(comprimento, (int, float)):
            raise TypeError("O comprimento deve ser um inteiro ou um float!")

        if comprimento <= 0:
            raise ValueError("O comprimento deve ser um número positivo!")

        # Validação da densidade
        if not isinstance(densidade_atual, (int, float)):
            raise TypeError("A densidade_atual deve ser um inteiro ou um float!")

        if densidade_atual < 0:
            raise ValueError("A densidade atual deve ser um número não negativo!")

        # Validação da velocidade livre
        if not isinstance(velocidade_livre, (int, float)):
            raise TypeError("A velocidade livre deve ser um inteiro ou um float!")

        if velocidade_livre < 0:
            raise ValueError("A velocidade livre deve ser um número não negativo!")

        # Validação da capacidade máxima
        if not isinstance(capacidade_maxima, (int, float)):
            raise TypeError("A capacidade maxima deve ser um inteiro ou um float!")

        if capacidade_maxima <= 0:
            raise ValueError("A capacidade maxima deve ser um número positivo!")

        # Validação do expoente do modelo
        if not isinstance(expoente_a, (int, float)):
            raise TypeError("O expoente 'a' deve ser um inteiro ou um float!")

        if expoente_a <= 0:
            raise ValueError("O expoente 'a' deve ser um número positivo!")

        # Armazenamento dos atributos privados
        self.__id = id
        self.__comprimento = float(comprimento)
        self.__densidade_atual = float(densidade_atual)
        self.__velocidade_livre = float(velocidade_livre)
        self.__capacidade_maxima = float(capacidade_maxima)
        self.__expoente_a = float(expoente_a)

    # Métodos getters
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

    # Atualização da densidade
    def set_densidade_atual(self, nova_densidade):

        # Impede densidades negativas
        if nova_densidade < 0:
            nova_densidade = 0

         # Impede que a densidade ultrapasse a capacidade máxima
        if nova_densidade > self.get_capacidade_maxima():
            nova_densidade = self.get_capacidade_maxima()

        self.__densidade_atual = nova_densidade

        return

    # Cálculo do fluxo de tráfego
    def calcular_fluxo(self):

        # Densidade atual do trecho
        rho = self.get_densidade_atual()

        # Fluxo = densidade × velocidad
        fluxo = rho * self.calcular_velocidade()

        # Limitador físico de fluxo para evitar instabilidade
        fluxo = min(fluxo, self.get_capacidade_maxima() * 0.8)

        return fluxo

    # Modelo velocidade-densidade
    def calcular_velocidade(self):

        rho     = self.get_densidade_atual()
        rho_max = self.get_capacidade_maxima()
        vf      = self.get_velocidade_livre()
        a       = self.get_expoente_a()

        # Evita imprecisão numérica caso rho passe de rho_max de raspão antes do set_densidade_atual agir
        if rho >= rho_max:
            return 0.0

        # Modelo fundamental de tráfego:
        # v = vf * (1 - (rho/rho_max)^a)
        return vf * (1 - (rho / rho_max) ** a)

    # Método abstrato
    # Cada tipo de elemento da via
    # implementa sua própria regra
    # de atualização da densidade.
    @abstractmethod
    def atualizar_densidade(self, fluxo_entrada, fluxo_saida, delta_t):
        pass

    # Conversão para dicionário
    # Facilita exportação para JSON,
    # relatórios ou armazenamento.
    def para_dict(self):

        return {

            "id":
                self.get_id(),

            "comprimento":
                self.get_comprimento(),

            "densidade":
                self.get_densidade_atual(),

            "velocidade_livre":
                self.get_velocidade_livre(),

            "capacidade_maxima":
                self.get_capacidade_maxima(),

            "expoente_a":
                self.get_expoente_a()
        }
