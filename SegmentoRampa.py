from ElementoVia import ElementoVia

# Classe que representa um segmento de via com rampa.
# A rampa pode ser de entrada (injeta veículos na via)
# ou de saída (remove veículos da via).
class SegmentoRampa(ElementoVia):
    def __init__(self, id: int, comprimento, densidade_atual, velocidade_livre, capacidade_maxima, expoente_a, tipo, fluxo_externo):

        # Inicializa os atributos herdados da classe base
        super().__init__(id, comprimento, densidade_atual, velocidade_livre, capacidade_maxima, expoente_a)

        # Validação do tipo de rampa
        if not isinstance(tipo, str):
            raise TypeError("O tipo do 'segmento-rampa' deve ser uma string!")

        if not tipo.strip():
            raise ValueError("O tipo não pode ser vazio!")

        if tipo not in ["entrada", "saida"]:
            raise ValueError("O tipo deve ser 'entrada' ou 'saida'!")

        # Validação do fluxo externo
        if not isinstance(fluxo_externo, (int, float)):
            raise TypeError("O fluxo externo dever ser um inteiro ou um float!")

        if fluxo_externo <= 0:
            raise ValueError("O fluxo externo deve ser um número positivo!")

        # Armazena o tipo da rampa
        # ("entrada" ou "saida")
        self.__tipo = tipo

        # Fluxo adicional associado à rampa
        self.__fluxo_externo = fluxo_externo

    # Métodos getters
    def get_tipo(self):
        return self.__tipo

    def get_fluxo_externo(self):
        return self.__fluxo_externo

    # Atualização da densidade
    # Considera o efeito de uma rampa
    # de entrada ou saída conectada ao segmento.
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

        # Tratamento da rampa de entrada
        if self.get_tipo() == "entrada":
            # Se a via está cheia, a rampa de entrada não consegue injetar o fluxo total

            # Espaço disponível antes da saturação da via
            espaco_disponivel = self.get_capacidade_maxima() - rho

            # Limita o fluxo efetivo para evitar
            # que a densidade ultrapasse a capacidade máxima
            fluxo_rampa_efetivo = min(self.get_fluxo_externo(), max(0, espaco_disponivel * self.get_comprimento() / delta_t))

            # Soma o fluxo da rampa ao fluxo de entrada
            fluxo_entrada += fluxo_rampa_efetivo

        # Tratamento da rampa de saída
        elif self.get_tipo() == "saida":
            # A rampa de saída não pode tirar mais carros do que existem no segmento

            # Quantidade máxima de veículos que podem
            # ser removidos do segmento
            carros_disponiveis = rho * self.get_comprimento() / delta_t

            # Impede que a rampa retire mais veículos
            # do que realmente existem na via
            fluxo_rampa_efetivo = min(self.get_fluxo_externo(), max(0, carros_disponiveis))

            # Soma a retirada da rampa ao fluxo de saída
            fluxo_saida += fluxo_rampa_efetivo

        # Equação de conservação
        rho_novo = rho + (delta_t / self.get_comprimento()) * (fluxo_entrada - fluxo_saida)

        # Mantém a densidade dentro dos
        # limites físicos permitidos
        rho_novo = min(self.get_capacidade_maxima(), max(0, rho_novo))

        # Atualiza a densidade armazenada
        self.set_densidade_atual(rho_novo)

        return

    # Conversão para dicionário
    # Acrescenta ao dicionário os dados
    # específicos do segmento com rampa.
    def para_dict(self):

        # Obtém os dados da classe base
        dados = super().para_dict()

        # Identifica o tipo da classe
        dados["classe"] = "SegmentoRampa"

        # Tipo da rampa
        dados["tipo"] = self.get_tipo()

         # Fluxo associado à rampa
        dados["fluxo_externo"] = self.get_fluxo_externo()

        return dados
