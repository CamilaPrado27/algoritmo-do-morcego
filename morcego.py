import numpy as np
import matplotlib.pyplot as plt
import math

longitudes = [-46.633,-46.583,-46.533,-46.483,-46.433,-46.383,-46.333,-46.283,-46.233,-46.183,-46.133,-46.083,-46.033,-45.983,-45.933,-45.883,]
latitudes = [-23.550, -23.488, -23.426, -23.364, -23.302, -23.240, -23.178]

destino = np.array([-45.883, -23.178])
origem = np.array([-46.633, -23.550])

pontos = np.array([(lon, lat) for lon in longitudes for lat in latitudes])

populacao = 10
dimensao = 2
limite_max = np.max(pontos, axis=0)
limite_min = np.min(pontos, axis=0)
velocidade_max = 0.1 * (limite_max - limite_min)
interacoes = 100

# função de custo deveria avaliar a rota e não o ponto 
def calcular_distancia(ponto, destino):
    return np.linalg.norm(ponto - destino)

posicoes = np.tile(origem, (populacao, 1))
velocidades = np.zeros((populacao, dimensao))
pulso_emissao = 0.5
pulso_emissao_fix = 0.5
amplitude = 1
frequencia_min = 0
frequencia_max = 2

melhor_solucao = origem
solucao_final = []

melhor_distancia_global = calcular_distancia(origem, destino)
melhor_solucao_global = origem.copy()

for t in range(interacoes):
    print('interação ', t)
    for i in range(populacao):                 
        frequencia = (frequencia_min + (frequencia_max - frequencia_min) * np.random.rand())
        velocidades[i] += (posicoes[i] - melhor_solucao) * frequencia
        posicoes[i] += velocidades[i]

        if np.random.rand() > pulso_emissao:
            posicoes[i] = melhor_solucao + 0.001 * np.random.rand(dimensao)
        
        nova_posicao = limite_min + (limite_max - limite_min) * np.random.rand(dimensao)

        if np.random.rand() < amplitude and calcular_distancia(nova_posicao, destino) < calcular_distancia(melhor_solucao, destino):
            posicoes[i] = nova_posicao
            pulso_emissao = pulso_emissao_fix * (1 - np.exp(-0.1 * t))
            amplitude *= 0.9

        if calcular_distancia(posicoes[i], destino) < calcular_distancia(melhor_solucao, destino):
            melhor_solucao = posicoes[i]


        distancia_atual = calcular_distancia(melhor_solucao, destino)
        if distancia_atual < melhor_distancia_global:
            melhor_distancia_global = distancia_atual
            melhor_solucao_global = melhor_solucao.copy()
    
    print(calcular_distancia(melhor_solucao, destino))
    solucao_final.append(melhor_solucao.copy())


print(f"Melhor solução geral encontrada: calcular_distancia = {melhor_distancia_global}, x* = {melhor_solucao_global, destino}")

solucao_final = np.array(solucao_final)


plt.scatter(pontos[:, 0], pontos[:, 1], c="blue", label="Pontos")

for i in range(len(solucao_final)):
    plt.scatter(
        solucao_final[i, 0], solucao_final[i, 1], label=f"Iteração {i + 1}", alpha=0.5
    )

# for i in range(len(posicoes)):
#     plt.scatter(
#         posicoes[i, 0], posicoes[i, 1], label=f"Iteração {i + 1}", alpha=0.5
#     )

plt.scatter(melhor_solucao_global[0], melhor_solucao_global[1], c="red", label="Melhor Solução")

plt.scatter(origem[0], origem[1], c="purple", label="Origem", marker="o")
plt.scatter(destino[0], destino[1], c="red", label="Destino", marker="x")

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Algoritmo do Morcego")
plt.show()
