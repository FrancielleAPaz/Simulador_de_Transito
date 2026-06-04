from SimuladorTrafego import SimuladorTrafego
from TrechoNormal import TrechoNormal
from Rampa import Rampa

sim = SimuladorTrafego(tempo_passo = 1)

t1 = TrechoNormal(

    1,
    1.0,
    20,
    100,
    150,
    2,
    3

)

t2 = TrechoNormal(

    2,
    1.0,
    30,
    100,
    150,
    2,
    3

)

r1 = Rampa(

    3,
    1.0,
    25,
    100,
    150,
    2,
    "entrada",
    10

)

sim.adicionar_elemento(t1)
sim.adicionar_elemento(t2)
sim.adicionar_elemento(r1)

for passo in range(10):

    sim.simular_passo()

    print(f"\nPASSO {passo + 1}")

    for dado in sim.obter_estado_atual():
        print(

            f"ID: {dado['id']} | "
            f"Densidade: {dado['densidade']:.2f} | "
            f"Velocidade: {dado['velocidade']:.2f} | "
            f"Fluxo: {dado['fluxo']:.2f}"
            
        )
