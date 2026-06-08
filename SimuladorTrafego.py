from ElementoVia import ElementoVia
from BancoDados import BancoDados

# Classe principal do simulador de tráfego
# Responsabilidades:
# - Armazenar os elementos da rede viária;
# - Controlar o avanço temporal da simulação;
# - Calcular a transferência de fluxo entre segmentos;
# - Atualizar as densidades dos elementos;
# - Disponibilizar o estado atual do sistema.
#
# A simulação é baseada em um modelo macroscópico
# de conservação de veículos, onde cada elemento
# troca fluxo com seus vizinhos ao longo do tempo.
class SimuladorTrafego:
    def __init__(self, tempo_passo):

        # Validação do passo temporal
        if not isinstance(tempo_passo, (int, float)):
            raise TypeError("O tempo de passo deve ser numérico!")

        if tempo_passo <= 0:
            raise ValueError("O tempo de passo deve ser positivo!")

        # Intervalo de tempo utilizado em cada iteração
        self.__tempo_passo   = float(tempo_passo)

        # Lista contendo todos os elementos da rede viária
        self.__elementos_via = []

        # Instância do módulo responsável por persistência
        # de cenários e resultados
        self.__banco = BancoDados()

    # Métodos de acesso
    def get_elementos_via(self):
        return self.__elementos_via

    def get_tempo_passo(self):
        return self.__tempo_passo

    # Inserção de elementos na rede
    def adicionar_elemento(self, elemento):

        # Garante que apenas objetos derivados
        # de ElementoVia sejam adicionados
        if not isinstance(elemento, ElementoVia):
            raise TypeError("O objeto deve herdar de 'ElementoVia'!")

        self.__elementos_via.append(elemento)

    # Execução de um passo da simulação
    #
    # O procedimento ocorre em duas etapas:
    #
    # 1) Cada elemento calcula o fluxo que deseja
    #    enviar para frente (fluxo potencial).
    #
    # 2) As densidades são atualizadas utilizando
    #    os fluxos de entrada e saída efetivos.
    #
    # Essa abordagem evita que alterações em um
    # elemento influenciem imediatamente os demais
    # durante o mesmo passo temporal.
    def simular_passo(self):

        num_elementos = len(self.get_elementos_via())

        if num_elementos == 0:
            raise RuntimeError("Não existem elementos para simular!")

        # Calcula a intenção de fluxo potencial de cada elemento baseado na sua densidade atual
        #
        # Cada elemento calcula quanto fluxo
        # gostaria de transferir com base na
        # densidade atual do instante t.
        #
        # Nenhuma densidade é modificada aqui.
        fluxos_potenciais = []
        for elemento in self.get_elementos_via():
            fluxos_potenciais.append(elemento.calcular_fluxo())

        # Atualização das densidades
        for i, elemento in enumerate(self.get_elementos_via()):

            # Cálculo do fluxo de entrada
            if i == 0:

                # O primeiro elemento recebe um fluxo externo inicial constante (ex: demanda da rodovia)
                # Definimos um fluxo de entrada padrão estável (ex: 0.4 veículos por segundo)
                fluxo_entrada = 0.4

            else:

                # O fluxo que entra em 'i' vem do que o elemento de trás 'i-1' quer enviar
                fluxo_entrada = fluxos_potenciais[i - 1]

            # Cálculo do fluxo de saída
            if i == num_elementos - 1:

                # O último elemento não possui
                # vizinho à frente.
                #
                # Portanto todo seu fluxo potencial
                # pode sair do sistema.
                fluxo_saida = fluxos_potenciais[i]

            else:

                # O fluxo que sai de 'i' é o fluxo potencial que o elemento da frente 'i+1' vai receber
                fluxo_saida = fluxos_potenciais[i]

                # Controle de capacidade do próximo segmento
                 # Impede que um elemento envie mais
                # veículos do que o próximo consegue
                # armazenar.
                #
                # Esse mecanismo evita:
                # - superlotação artificial;
                # - densidades acima da capacidade;
                # - instabilidades numéricas.
                elemento_frente = self.__elementos_via[i + 1]
                vagas_na_frente = (elemento_frente.get_capacidade_maxima() - elemento_frente.get_densidade_atual()) * elemento_frente.get_comprimento()
                fluxo_max_suportado = max(0, vagas_na_frente / self.get_tempo_passo())

                # Limita o fluxo de saída ao espaço realmente disponível no elemento seguinte.
                fluxo_saida = min(fluxo_saida, fluxo_max_suportado)

            # Atualização da densidade do elemento
            elemento.atualizar_densidade(fluxo_entrada, fluxo_saida, self.get_tempo_passo())


    # Consulta do estado atual da rede
    #
    # Retorna uma estrutura contendo:
    # - identificação do elemento;
    # - densidade atual;
    # - velocidade atual;
    # - fluxo atual.
    #
    # Esse método é utilizado para:
    # - exibição dos resultados;
    # - armazenamento do histórico;
    # - exportação para CSV.
    def obter_estado_atual(self):

        estado = []

        for elemento in self.get_elementos_via():

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
