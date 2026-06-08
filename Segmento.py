from ElementoVia import ElementoVia

# Classe que representa um segmento comum da via.
# Herda as características básicas de ElementoVia e
# adiciona a informação sobre o número de faixas.
class Segmento(ElementoVia):
    def __init__(self, id: int, comprimento, densidade_atual, velocidade_livre, capacidade_maxima, expoente_a, num_faixas: int):

        # Inicializa os atributos herdados da classe base
        super().__init__(id, comprimento, densidade_atual, velocidade_livre, capacidade_maxima, expoente_a)

        # Validação do número de faixas
        if not isinstance(num_faixas, int):
            raise TypeError("O número de faixas deve ser um número inteiro!")

        if num_faixas <= 0:
            raise ValueError("O número de faixas deve ser um número positivo!")

        # Armazena a quantidade de faixas do segmento
        self.__num_faixas = num_faixas

    # Getter do número de faixas
    def get_num_faixas(self):
        return self.__num_faixas

    # Atualização da densidade
    # Implementa a equação de conservação de veículos:
    #
    # rho_novo = rho +
    #              (delta_t / comprimento)
    #            * (fluxo_entrada - fluxo_saida)
    #
    # Se entra mais fluxo do que sai,
    # a densidade aumenta.
    #
    # Se sai mais fluxo do que entra,
    # a densidade diminui.
    def atualizar_densidade(self, fluxo_entrada, fluxo_saida, delta_t):

        # Validação do fluxo de entrada
        if not isinstance(fluxo_entrada, (int, float)):
            raise TypeError("O fluxo de entrada deve ser um inteiro ou um float!")

        if fluxo_entrada < 0:
            raise ValueError("O fluxo de entrada deve ser um número não negativo!")

        # Validação do fluxo de saída
        if not isinstance(fluxo_saida, (int, float)):
            raise TypeError("O fluxo de saída deve ser um inteiro ou um float!")

        if fluxo_saida < 0:
            raise ValueError("O fluxo de saída deve ser um número não negativo!")

        # Validação do passo de tempo
        if not isinstance(delta_t, (int, float)):
            raise TypeError("A variação do tempo deve ser um inteiro ou um float!")

        if delta_t <= 0:
            raise ValueError("A variação do tempo deve ser positiva!")

        # Densidade atual do segmento
        rho = self.get_densidade_atual()

        # Atualização da densidade utilizando
        # o balanço entre entrada e saída de veículos
        rho_novo = rho + (delta_t / self.get_comprimento()) * (fluxo_entrada - fluxo_saida)

        # Garante que a densidade permaneça
        # dentro dos limites físicos permitidos
        rho_novo = min(self.get_capacidade_maxima(), max(0, rho_novo))

        # Atualiza a densidade armazenada
        self.set_densidade_atual(rho_novo)

        return

    # Conversão para dicionário
    # Acrescenta informações específicas
    # da classe Segmento ao dicionário
    # gerado pela classe base.
    def para_dict(self):

        # Obtém os dados comuns da superclasse
        dados = super().para_dict()

        # Identifica o tipo do objeto
        dados["classe"] = "Segmento"

        # Adiciona o número de faixas
        dados["num_faixas"] = self.get_num_faixas()

        return dados
