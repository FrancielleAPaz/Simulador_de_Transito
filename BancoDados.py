from Segmento import Segmento
from SegmentoRampa import SegmentoRampa
import json
import csv
import os

# Classe responsável pelo gerenciamento de persistência
# dos dados da aplicação.
#
# Suas principais funções são:
# - Salvar cenários em arquivos JSON;
# - Carregar cenários previamente salvos;
# - Listar cenários disponíveis;
# - Exportar resultados de simulação para arquivos CSV.
class BancoDados:

    def __init__(self):

        # Pasta onde os cenários da simulação serão armazenados
        self.__pasta_cenarios = "cenarios"

        # Pasta onde os resultados das execuções serão armazenados
        self.__pasta_resultados = "resultados"

        # Cria automaticamente as pastas caso não existam
        os.makedirs(self.__pasta_cenarios, exist_ok = True)
        os.makedirs(self.__pasta_resultados, exist_ok = True)

    # GERENCIAMENTO DE CENÁRIOS
    def salvar_cenario(self, nome, simulador):

        #Salva o estado atual da rede viária em um arquivo JSON.

        #Parâmetros:
            #nome (str):
                #Nome do cenário.

            #simulador:
                #Objeto simulador contendo os elementos da via.

        # Estrutura que será convertida para JSON
        dados = {

            # Passo de tempo padrão utilizado na simulação
            "tempo_passo": 1.0,

            # Lista contendo todos os elementos da via
            # convertidos para dicionários
            "elementos": [

                elemento.para_dict()

                for elemento

                in simulador.get_elementos_via()

            ]

        }

        # Monta o caminho completo do arquivo
        caminho = os.path.join(self.__pasta_cenarios, f"{nome}.json")

        # Salva os dados em formato JSON
        with open(caminho, "w", encoding = "utf-8") as arquivo:

            json.dump(dados, arquivo, indent = 4, ensure_ascii = False)

    def carregar_cenario(self, nome):

        #Carrega um cenário salvo em arquivo JSON.

        #Parâmetros:
            #nome (str):
                #Nome do cenário.

        #Retorna:
            #list:
                #Lista de objetos Segmento e/ou SegmentoRampa.

        # Caminho do arquivo de cenário
        caminho = os.path.join(self.__pasta_cenarios, f"{nome}.json")

        # Leitura do arquivo JSON
        with open(caminho, "r", encoding = "utf-8") as arquivo:

            dados = json.load(arquivo)

        # Lista que armazenará os elementos reconstruídos
        elementos = []

        # Reconstrução dos objetos a partir dos dados salvos
        for item in dados["elementos"]:

            # Segmento convencional
            if item["classe"] == "Segmento":

                elementos.append(

                    Segmento(

                        item["id"],

                        item["comprimento"],

                        item["densidade"],

                        item["velocidade_livre"],

                        item["capacidade_maxima"],

                        item["expoente_a"],

                        item["num_faixas"]
                    )
                )

            # Segmento com rampa
            elif item["classe"] == "SegmentoRampa":

                elementos.append(

                    SegmentoRampa(

                        item["id"],

                        item["comprimento"],

                        item["densidade"],

                        item["velocidade_livre"],

                        item["capacidade_maxima"],

                        item["expoente_a"],

                        item["tipo"],

                        item["fluxo_externo"]

                    )

                )

        return elementos

    def listar_cenarios(self):

        #Retorna todos os cenários disponíveis
        #na pasta de armazenamento.

        #Retorna:
            #list:
                #Lista contendo os nomes dos cenários.

        return [

            arquivo.replace(".json", "")

            for arquivo in os.listdir(self.__pasta_cenarios)

            if arquivo.endswith(".json")

        ]

    # EXPORTAÇÃO DE RESULTADOS
    def salvar_resultados_csv(self, nome_arquivo, historico):

        #Exporta o histórico da simulação para um arquivo CSV.

        #Parâmetros:
            #nome_arquivo (str):
                #Nome do arquivo de saída.

            #historico (list):
                #Histórico gerado pelo simulador.

        #Retorna:
            #str:
                #Caminho completo do arquivo gerado.

        # Remove caracteres inválidos do nome
        nome = self.__limpar_nome(nome_arquivo)

        # Caminho do arquivo CSV
        caminho = os.path.join(self.__pasta_resultados, f"{nome}.csv")

        with open(caminho, "w", newline = "", encoding = "utf-8") as arquivo:

            writer = csv.writer(arquivo)

            # Cabeçalho do arquivo
            writer.writerow(["passo", "id", "densidade", "velocidade", "fluxo"])

            # Percorre cada passo da simulação
            for passo, estados in enumerate(historico, start = 1):

                # Percorre todos os elementos presentes
                # naquele instante da simulação
                for dado in estados:

                    # Densidade armazenada commaior precisão numérica
                    # Velocidade apresentada com duas casas decimais
                    # Fluxo apresentado com quatro casas decimais
                    writer.writerow([passo, dado["id"], round(dado["densidade"], 6), round(dado["velocidade"], 2), round(dado["fluxo"], 4)])

        return caminho

    # MÉTODOS AUXILIARES
    def __limpar_nome(self, nome):

        #Remove caracteres inválidos de nomes de arquivos.

        #Permite apenas:
            #- letras;
            #- números;
            #- espaço;
            #- underscore (_);
            #- hífen (-).

        #Parâmetros:
            #nome (str):
                #Nome original.

        #Retorna:
            #str:
                #Nome tratado.

        return "".join(

            c

            for c in nome

            if c.isalnum() or c in (
                "_",
                "-",
                " "
            )

        ).strip()
