from SimuladorTrafego import SimuladorTrafego
from Segmento import Segmento
from SegmentoRampa import SegmentoRampa
from BancoDados import BancoDados

# Sistema de Simulação de Tráfego

# Este módulo implementa a interface de interação
# com o usuário através do terminal.
#
# Funcionalidades:
# - Criação de segmentos da via;
# - Criação de rampas de entrada e saída;
# - Visualização do estado atual da rede;
# - Execução da simulação;
# - Salvamento de cenários;
# - Carregamento de cenários;
# - Exportação dos resultados para CSV.
#
# O módulo atua como camada de apresentação,
# enquanto as regras de negócio ficam nas classes
# SimuladorTrafego, Segmento, SegmentoRampa e
# BancoDados.

# Menu principal
# Exibe as opções disponíveis ao usuário e retorna
# a opção digitada.
def menu():

    print("\n" + "-" * 40)
    print(" SIMULADOR DE TRÁFEGO ")
    print("-" * 40)
    print("1 - Adicionar Segmento")
    print("2 - Adicionar Rampa")
    print("3 - Mostrar Estado Atual")
    print("4 - Executar Simulação")
    print("5 - Salvar Cenário")
    print("6 - Carregar Cenário")
    print("7 - Listar Cenários")
    print("0 - Sair")

    return input("\nEscolha: ")

# Entrada segura de números reais
# Solicita um valor float ao usuário e garante:
# - entrada numérica válida;
# - valor acima do mínimo especificado.
def obter_float(msg, min_val = 0):

    while True:

        try:

            v = float(input(msg))

            if v < min_val:

                print(f"Valor deve ser >= {min_val}")

                continue

            return v

        except ValueError:
            print("Digite um número válido.")

# Entrada segura de números inteiros
# Solicita um valor inteiro ao usuário e garante:
# - entrada válida;
# - valor acima do mínimo especificado.
def obter_int(msg, min_val = 1):

    while True:

        try:

            v = int(input(msg))

            if v < min_val:

                print(f"Valor deve ser >= {min_val}")

                continue

            return v

        except ValueError:
            print("Digite um inteiro válido.")

# Criação de um segmento convencional
# Solicita ao usuário todos os parâmetros
# necessários para instanciar um objeto Segmento.
def criar_segmento(id_atual):

    print("\n--- Segmento ---")

    comp = obter_float("Comprimento(metros): ", 0.1)
    dens = obter_float("Densidade(veic/metro): ", 0)
    v = obter_float("Velocidade livre(m/s): ", 1)
    cap = obter_float("Capacidade máxima(veic/metro): ", 0.01)

    # Garante consistência física:
    # densidade não pode ultrapassar a capacidade.
    while dens > cap:

        print("Densidade não pode ser maior que capacidade.")

        dens = obter_float("Densidade(veic/metro): ", 0)

    a = obter_float("Expoente a (padrão 1.0): ", 0.1)

    faixas = obter_int("Número de faixas: ", 1)

    return Segmento(id_atual, comp, dens, v, cap, a, faixas)

# Criação de um segmento com rampa
# Solicita os parâmetros necessários para criar
# uma rampa de entrada ou saída.
def criar_rampa(id_atual):

    print("\n--- Rampa ---")

    comp = obter_float("Comprimento(metros): ", 0.1)
    dens = obter_float("Densidade(veic/metro): ", 0)
    v = obter_float("Velocidade livre(m/s): ", 1)
    cap = obter_float("Capacidade máxima(veic/metro): ", 0.01)

    while dens > cap:

        print("Densidade não pode ser maior que capacidade.")

        dens = obter_float("Densidade(veic/metro): ", 0)

    a = obter_float("Expoente a (padrão 1.0): ", 0.1)

    while True:

        tipo = input("Tipo (entrada/saida): ").strip().lower()

        if tipo in ["entrada", "saida"]:
            break

        print("Digite 'entrada' ou 'saida'.")

    fluxo = obter_float("Fluxo externo da rampa(veic/segundo): ", 0)

    return SegmentoRampa(id_atual, comp, dens, v, cap, a, tipo, fluxo)

# Exibição do estado atual da rede
# Mostra:
# - densidade;
# - velocidade;
# - fluxo.
#
# A velocidade é convertida de m/s para km/h
# para facilitar a interpretação.
def mostrar_estado(sim):

    estado = sim.obter_estado_atual()

    if not estado:
        print("\nSem elementos na simulação.")

        return

    print("\n--- ESTADO ATUAL ---")

    for e in estado:

        print(

            f"ID {e['id']} | "
            f"Densidade {e['densidade']:.4f} v/m | "
            f"Velocidade {e['velocidade']*3.6:.1f} km/h | "
            f"Fluxo {e['fluxo']:.2f} v/s"

        )

# Execução da simulação
#
# Executa vários passos consecutivos da simulação.
#
# Durante a execução:
# - atualiza a rede;
# - armazena o histórico;
# - apresenta os resultados;
# - permite exportação para CSV.
def executar_simulacao(sim, banco):

    passos = obter_int("\nNúmero de passos da simulação: ", 1)

    historico = []

    try:

        for p in range(passos):

            # Avança um passo temporal
            sim.simular_passo()

            # Obtém o novo estado da rede
            estado = sim.obter_estado_atual()

            # Salva para posterior exportação
            historico.append(estado)

            print(f"\nPASSO {p + 1}")

            for e in estado:

                print (

                    f"ID {e['id']} | "
                    f"Densidade {e['densidade']:.4f} v/m | "
                    f"Velocidade {e['velocidade']*3.6:.1f} km/h | "
                    f"Fluxo {e['fluxo']:.5f} v/s"

                )

        # Exportação opcional dos resultados
        if input("\nSalvar CSV? (s/n): ").lower() == "s":

            nome = input("Nome do arquivo: ")

            caminho = banco.salvar_resultados_csv(nome, historico)

            print(f"\nSalvo em: {caminho}")

    except Exception as e:
        print(f"\nErro na simulação: {e}")

# Função principal do programa
# Responsável por:
# - criar os objetos principais;
# - controlar o menu;
# - coordenar as operações do usuário.
def main():

    banco = BancoDados()
    simulador = SimuladorTrafego(tempo_passo = 1.0)

    # Gerador simples de identificadores únicos
    id_atual = 1

    while True:

        op = menu()

        try:

            # Adicionar segmento convencional
            if op == "1":

                seg = criar_segmento(id_atual)
                simulador.adicionar_elemento(seg)
                id_atual += 1
                print("Segmento adicionado.")

            # Adicionar segmento com rampa
            elif op == "2":

                # Exige pelo menos um segmento principal
                if not simulador.obter_estado_atual():
                    print("Adicione um segmento principal antes de um 'segmento-rampa'.")

                    continue

                ramp = criar_rampa(id_atual)
                simulador.adicionar_elemento(ramp)
                id_atual += 1
                print("Rampa adicionada.")

            elif op == "3":

                mostrar_estado(simulador)

            elif op == "4":

                executar_simulacao(simulador, banco)

            elif op == "5":

                nome = input("Nome do cenário: ")
                banco.salvar_cenario(nome, simulador)
                print("Cenário salvo.")

            elif op == "6":

                nome = input("Nome do cenário: ")

                elementos = banco.carregar_cenario(nome)

                # Reconstrói o simulador
                simulador = SimuladorTrafego(tempo_passo = 1.0)

                for e in elementos:
                    simulador.adicionar_elemento(e)

                id_atual = len(elementos) + 1

                print("Cenário carregado.")

            elif op == "7":

                cenarios = banco.listar_cenarios()

                if not cenarios:
                    print("Nenhum cenário salvo.")

                else:
                    print("\nCenários:")

                    for c in cenarios:
                        print("-", c)

            elif op == "0":
                print("Encerrando...")
                break

            else:
                print("Opção inválida.")

        except Exception as e:
            print(f"\nErro: {e}")


# Ponto de entrada da aplicação
# Garante que o programa seja executado apenas
# quando este arquivo for iniciado diretamente.
if __name__ == "__main__":
    main()
