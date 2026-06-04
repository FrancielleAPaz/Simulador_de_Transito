from ElementoVia import ElementoVia

class TrechoNormal(ElementoVia):
    def __init__(self, id: int, comprimento: float, densidade_atual: float,
                 velocidade_livre: float, capacidade_maxima: float, expoente_a: float, num_faixas: int):

        super().__init__(id, comprimento, densidade_atual, velocidade_livre, capacidade_maxima, expoente_a)

        self.__num_faixas = num_faixas

    def get_num_faixas(self):
        return self.__num_faixas

    def atualizar_densidade(self, fluxo_entrada: float, fluxo_saida: float, delta_t: float):

        rho = self.get_densidade_atual()

        rho_novo = rho + (delta_t / self.get_comprimento()) * (fluxo_entrada - fluxo_saida)

        self.set_densidade_atual(max(0, rho_novo))

        return
