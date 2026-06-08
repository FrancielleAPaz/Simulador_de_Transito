# Simulador de Tráfego

Este projeto consiste em um simulador de tráfego desenvolvido em Python utilizando conceitos de Programação Orientada a Objetos. O sistema permite modelar uma rodovia através de segmentos e rampas, simulando a evolução da densidade, velocidade e fluxo de veículos ao longo do tempo. Também é possível salvar cenários em arquivos JSON e exportar os resultados da simulação para arquivos CSV para análise posterior.

Para utilizar o programa, basta executar o arquivo `main.py` e seguir as opções do menu. Inicialmente devem ser cadastrados os elementos da via (segmentos e/ou rampas). Em seguida, o usuário pode visualizar o estado atual da rede, executar a simulação por um número desejado de passos e, caso queira, salvar os resultados obtidos.

Gostaríamos de agradecer à professora pela disciplina e pelos conhecimentos compartilhados ao longo do semestre. O desenvolvimento deste trabalho permitiu aplicar na prática diversos conceitos estudados em sala, especialmente abstração, herança, polimorfismo, tratamento de exceções, persistência de dados e simulação computacional.

A seguir são apresentados três cenários sugeridos para teste do sistema:

## Cenário 1 – Fluxo Livre

Passo 1: Escolha a opção **1 - Adicionar Segmento**

Preencha com:

* Comprimento: `1000`
* Densidade: `0.02`
* Velocidade livre: `33`
* Capacidade máxima: `0.15`
* Expoente a: `1`
* Número de faixas: `2`

Passo 2: Escolha **4 - Executar Simulação**

* Número de passos: `20`

Resultado esperado: velocidades elevadas (próximas da velocidade livre) e fluxo estável, sem congestionamento.

---

## Cenário 2 – Congestionamento

Passo 1: Adicione o primeiro segmento

* Comprimento: `500`
* Densidade: `0.12`
* Velocidade livre: `33`
* Capacidade máxima: `0.15`
* Expoente a: `1`
* Número de faixas: `2`

Passo 2: Adicione o segundo segmento

* Comprimento: `500`
* Densidade: `0.14`
* Velocidade livre: `33`
* Capacidade máxima: `0.15`
* Expoente a: `1`
* Número de faixas: `2`

Passo 3: Execute a simulação

* Número de passos: `20`

Resultado esperado: redução significativa da velocidade e dificuldade de escoamento do fluxo devido à alta ocupação da via.

---

## Cenário 3 – Rodovia com Rampa de Entrada

Passo 1: Adicione um segmento principal

* Comprimento: `1000`
* Densidade: `0.05`
* Velocidade livre: `33`
* Capacidade máxima: `0.15`
* Expoente a: `1`
* Número de faixas: `2`

Passo 2: Adicione uma rampa

* Comprimento: `100`
* Densidade: `0.01`
* Velocidade livre: `20`
* Capacidade máxima: `0.15`
* Expoente a: `1`
* Tipo: `entrada`
* Fluxo externo: `0.5`

Passo 3: Execute a simulação

* Número de passos: `20`

Resultado esperado: aumento gradual da densidade no sistema devido à entrada contínua de veículos pela rampa, acompanhado de redução progressiva da velocidade ao longo da simulação.

IMPORTANTE:

Observação sobre o fluxo: Para garantir a estabilidade numérica da simulação e evitar comportamentos não físicos decorrentes de variações muito abruptas entre os segmentos,
foi implementado um limitador de fluxo no modelo (NO MÉTODO DA CLASSE ELEMENTOVIA). Dessa forma, o fluxo máximo em cada elemento da via é restringido a uma fração da capacidade máxima definida para o segmento.
Embora essa simplificação reduza parte da variabilidade observada em modelos de tráfego mais complexos,
ela contribui para a robustez da simulação e para a obtenção de resultados consistentes nos cenários propostos.
