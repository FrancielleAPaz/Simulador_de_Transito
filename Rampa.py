from ElementoVia import ElementoVia

class Rampa(ElementoVia):
    def __init__(self, id: int, comprimento: float, densidade_atual: float,
                 velocidade_livre: float, capacidade_maxima: float, expoente_a: float, tipo: str, fluxo_externo: float):


        super().__init__(id, comprimento, densidade_atual, velocidade_livre, capacidade_maxima, expoente_a)

        self.__tipo = tipo
        self.__fluxo_externo = fluxo_externo

    def atualizar_densidade(self, fluxo_entrada: float, fluxo_saida: float, delta_t: float):

        rho = self.get_densidade_atual()

        if self.__tipo == "entrada":
            fluxo_entrada += self.__fluxo_externo

        elif self.__tipo == "saida":
            fluxo_saida += self.__fluxo_externo

        rho_novo = rho + (delta_t / self.get_comprimento()) * (fluxo_entrada - fluxo_saida)

        self.set_densidade_atual(max(0, rho_novo))

        return
