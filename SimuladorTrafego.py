from BancoDados import BancoDados

class SimuladorTrafego:
    def __init__(self, tempo_passo):

        self.__tempo_passo   = tempo_passo
        self.__elementos_via = []

        self.__banco = BancoDados()

    def get_elementos_via(self):
        return self.__elementos_via
    
    def adicionar_elemento(self, elemento):
        self.__elementos_via.append(elemento)

    def simular_passo(self):

        fluxos = []

        for elemento in self.__elementos_via:
            fluxos.append(elemento.calcular_fluxo())

        for i, elemento in enumerate(self.__elementos_via):

            fluxo_entrada = (fluxos[i - 1] if i > 0 else 0)

            fluxo_saida = fluxos[i]

            elemento.atualizar_densidade(fluxo_entrada, fluxo_saida, self.__tempo_passo)

    def obter_estado_atual(self):

        estado = []

        for elemento in self.__elementos_via:

            estado.append({

                "id":
                    elemento.get_id(),

                "densidade":
                    elemento.get_densidade_atual(),

                "velocidade":
                    elemento.calcular_velocidade(),

                "fluxo":
                    elemento.calcular_fluxo()

            })

        return estado
