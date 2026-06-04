from SimuladorTrafego import SimuladorTrafego
from TrechoNormal import TrechoNormal
from Rampa import Rampa
from BancoDados import BancoDados

def exibir_ajuda():
    print("\n" + "="*40)
    print(" GLOSSÁRIO DA SIMULAÇÃO")
    print("="*40)
    print("\nCONCEITOS:")
    print("\n Trecho Normal: Um segmento comum da rodovia principal.")
    print(" Rampa: Uma alça de acesso (entrada) ou de escape (saída) que injeta ou remove fluxo da via principal.")
    print("\nPARÂMETROS FÍSICOS:")
    print("\n Densidade: Quantidade atual de veículos por km (Ex: 20).")
    print(" Velocidade Livre: A velocidade máxima atingida quando a via está completamente vazia (Ex: 100 km/h).")
    print(" Capacidade Máxima: O limite máximo de veículos que a via comporta antes do trânsito parar totalmente (Ex: 150).")
    print(" Expoente 'a': Fator matemático da equação que dita como a velocidade cai à medida que a via enche (Geralmente entre 1.5 e 3.0).")
    print(" Fluxo Externo: Quantidade de veículos por unidade de tempo entrando ou saindo pela rampa.")
    print("="*40 + "\n")

def exibir_menu():
    print("\n" + "="*30)
    print(" SIMULADOR DE TRÁFEGO ")
    print("="*30)
    print("1. Adicionar Trecho Normal")
    print("2. Adicionar Rampa")
    print("3. Executar Simulação")
    print("4. Salvar Cenário Atual")
    print("5. Carregar Cenário")
    print("6. Ajuda: Entenda os conceitos da simulação")
    print("0. Sair")
    return input("Escolha uma opção: ")

def obter_float(mensagem):
    """Função auxiliar para garantir que o usuário digite um número decimal válido."""
    while True:
        try:
            valor = float(input(mensagem))
            if valor < 0:
                print("Erro: O valor não pode ser negativo. Tente novamente.")
                continue
            return valor
        except ValueError:
            print("Erro: Entrada inválida. Por favor, digite um número.")

def obter_int(mensagem):
    """Função auxiliar para garantir que o usuário digite um número inteiro válido."""
    while True:
        try:
            valor = int(input(mensagem))
            if valor <= 0:
                print("Erro: O valor deve ser maior que zero. Tente novamente.")
                continue
            return valor
        except ValueError:
            print("Erro: Entrada inválida. Por favor, digite um número inteiro.")

def main():
    simulador = SimuladorTrafego(tempo_passo=1)
    banco = BancoDados()
    contador_id = 1
    print("\nBem-vindo ao Simulador de Tráfego!")
    print("Dica: Se não souber o que preencher, digite '6' no menu para abrir o Glossário.")

    while True:
        opcao = exibir_menu()

        if opcao == "1":
            print("\n--- Adicionando Trecho Normal ---")
            comp = obter_float("Comprimento da via (ex: 1.0): ")
            dens = obter_float("Densidade atual de veículos (ex: 20): ")
            v_livre = obter_float("Velocidade livre da via (ex: 100): ")
            cap_max = obter_float("Capacidade máxima (ex: 150): ")
            while cap_max < comp * dens:
                cap_max = obter_float("\nA capacidade máxima precisa ser maior ou igual à multiplicação entre o comprimento e a densidade, digite novamente.\n\nCapacidade máxima (ex: 150): ")
            exp_a = obter_float("Expoente 'a' da equação de velocidade (ex: 2): ")
            faixas = obter_int("Número de faixas (ex: 3): ")

            trecho = TrechoNormal(contador_id, comp, dens, v_livre, cap_max, exp_a, faixas)
            simulador.adicionar_elemento(trecho)
            print(f"Trecho Normal (ID: {contador_id}) adicionado com sucesso!")
            contador_id += 1

        elif opcao == "2":

            if not simulador.obter_estado_atual():
                print("\n Erro de Física: Uma rampa não pode ser o primeiro elemento do sistema.")
                print("Por favor, adicione pelo menos um 'Trecho Normal' (Opção 1) antes de inserir uma rampa.")
                continue 

            print("\n--- Adicionando Rampa ---")
            comp = obter_float("Comprimento da rampa (ex: 1.0): ")
            dens = obter_float("Densidade atual de veículos: ")
            v_livre = obter_float("Velocidade livre da rampa: ")
            cap_max = obter_float("Capacidade máxima: ")
            while cap_max < comp * dens:
                cap_max = obter_float("\nA capacidade máxima precisa ser maior ou igual à multiplicação entre o comprimento e a densidade, digite novamente.\n\nCapacidade máxima: ")
            exp_a = obter_float("Expoente 'a' da equação: ")
            
            # Tratamento de erro específico para texto
            while True:
                tipo = input("Tipo da rampa ('entrada' ou 'saida'): ").strip().lower()
                if tipo in ["entrada", "saida"]:
                    break
                print("Erro: Digite exatamente 'entrada' ou 'saida'.")
                
            fluxo_ext = obter_float("Fluxo externo de veículos: ")

            rampa = Rampa(contador_id, comp, dens, v_livre, cap_max, exp_a, tipo, fluxo_ext)
            simulador.adicionar_elemento(rampa)
            print(f"Rampa de {tipo} (ID: {contador_id}) adicionada com sucesso!")
            contador_id += 1

        elif opcao == "3":
            if not simulador.obter_estado_atual():
                print("\nNenhuma via adicionada! Adicione elementos antes de simular.")
                continue
                
            passos = obter_int("\nQuantos passos de tempo deseja simular? ")
            for passo in range(passos):
                simulador.simular_passo()
                print(f"\nPASSO {passo + 1}")
                for dado in simulador.obter_estado_atual():
                    print(f"ID: {dado['id']} | Densidade: {dado['densidade']:.2f} | Velocidade: {dado['velocidade']:.2f} | Fluxo: {dado['fluxo']:.2f}")

        elif opcao == "4":
            nome_cenario = input("\nDigite um nome para salvar este cenário: ")
            estado = simulador.obter_estado_atual()

            if not estado:
                print("\nERRO: A via está completamente vazia. Adicione trechos com ou sem rampas antes de salvar o cenário.")
                continue

            try:
                banco.salvar_cenario(nome_cenario, estado)
                print(f"Cenário '{nome_cenario}' salvo com sucesso na base de dados!")
            except Exception as e:
                print(f"Erro ao salvar: {e}")

        elif opcao == "5":
            nome_cenario = input("\nDigite o nome do cenário que deseja carregar: ")
            try:
                dados = banco.carregar_cenarios(nome_cenario)
                print(f"Cenário '{nome_cenario}' carregado! Dados brutos: {dados}")
            except FileNotFoundError:
                print("Erro: Arquivo de cenário não encontrado.")
            except Exception as e:
                print(f"Erro ao carregar: {e}")

        elif opcao == "6":
            exibir_ajuda()

        elif opcao == "0":
            print("\nEncerrando o simulador... Até logo!")
            break
            
        else:
            print("\nOpção inválida. Digite um número de 0 a 5.")

if __name__ == "__main__":
    main()
