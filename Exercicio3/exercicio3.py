# Matemática Computacional I - parte B - Exercício 3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1o período 2020
# Autores: Denis Eiras
# 28/04/2020 - V1.0
#
#
# O exercício 3 consiste em 3 etapas:
#
#   1. Executar a função gerador_de_sinais_pmodel, para gerar 2 familias, endógeno e exógeno.
#          
#   2. Cada fámilia terá 30 sinais que seram divididos em 3 grupos de 10 sinais.
#
#   3. Cada grupo será composto por 3 valores de beta dentro de uma faixa p.
#      Faixa endógeno (0.32-0.42)
#      Faixa exógeno (0.18-0.28)
#
# Entradas:
#
# - num_valores_por_sinal: (Array de inteiros) Cada elemento representa uma quantidade de valores do sinal de uma
#   família.
# - num_sinais: (Inteiro) Número de sinais gerados por família.
# - nome_arquivo_pmodel: (String) nome do arquivo csv gerado na saída, contendo os sinais das famílias.
# - nome_arquivo_figura_sinais_endo: (String) nome do arquivo da figura que exibe os sinais endógenos
# - nome_arquivo_figura_sinais_exo: (String) nome do arquivo da figura que exibe os sinais exógenos
# - nome_arq_saida_todos_momentos: (String) Nome do arquivo csv contendo os momentos estatísticos, nas colunas
# - metodos_do_cotovelo: (Array de Strings). Métodos do cotovelo a serem plotados. Opções:
#   - distorcao_km_inertia - Utiliza a soma das distâncias ao quadrado utilizado pelo próprio Kmeans do sklearn
#   - distorcao_yellowbrick - Utiliza a soma das distâncias ao quadrado do pacote yellowbrick. Neste gráfico é possível
#       observar a indicação de melhor k e tempo de cálculo de cada k.
#   - silhueta_yellowbrick - Utiliza o método silhueta do pacote yellowbrick. Neste gráfico é possível observar o tempo
#       de cálculo de cada k.
#   - calinski_harabasz_yellowbrick - Utiliza o método silhueta do pacote yellowbrick.
#   variância, assimetria e curstose, e as informações de família e sinal, nas colunas familia e sinal.
# - k: (Array) Array contendo número de clusters do algoritmo K-means
# - is_normalizar_valores: (Boolean) Indica se os valores armazenados no arquivo de momenteos deverão ser normalizados.
# - is_plotar_histograma_familia: (Boolean) True para plotar um histograma exemplo de um sinal da cada família
# - is_plotar_kmeans_cotovelo: (Boolean) True para plotar os gráficos de agrupamento para cada k e o gráfico do cotovelo
# - is_plotar_momentos_3d: (Boolean) True para plotar os gráficos com os momentos estatísticos em 3 dimensões
# - arr_p_endo: (Array de inteiros) Cada elemento representa um valor dentro da faixa p endógeno.
# - beta_endo: 0.4 itentificando a família endógeno.
# - arr_p_exo: (Array de inteiros) Cada elemento representa um valor dentro da faixa p exógeno.
# - beta_exo: 0.7 itentificando a família exógeno.
#
#
# Saídas:
#
# - arquivo csv de nome definido em "nome_arquivo_pmodel", contendo os sinais das famílias.
# - arquivo csv de nome definido em "nome_arq_saida_todos_momentos", contendo os momentos estatísticos gerados em
#   exercício 1.2
# - figuras em 2 dimensões contendo classes agrupadas nos espaços de parâmetros variância, assimetria e curtose, para
#   cada k, de nomes "k_#.png", onde # é o número k.
# - figuras em 3 dimensões contendo classes agrupadas nos espaços de parâmetros variância, assimetria e curtose, para
#   cada k, de nomes "k_#.png", onde # é o número k.
#
#
# Observações
#
# Utilização do algoritmo P-model from Meneveau & Sreenevasan, 1987 & Malara et al., 2016
# Author: R.R.Rosa & N. Joshi
# Version: 1.6
# Date: 11/04/2018

import matplotlib.pyplot as plt
import pandas as pd

from Exercicio1.exercicio1_2 import gerador_de_momentos
from Exercicio1.exercicio1_3 import k_means_e_metodo_do_cotovelo
from Exercicio3.pmodel import pmodel


def gerador_de_sinais_pmodel(num_valores_por_sinal, beta, arr_p, num_sinais):
    df_sinais = pd.DataFrame()
    num_sinal = 0
    for p in arr_p:
        for sinal in range(num_sinais):
            num_sinal = num_sinal + 1
            for num_valores in num_valores_por_sinal:
                # (setup: N, p: 0.32-0.42, beta=0.4)
                x, y = pmodel(num_valores, p, beta)
                y = y - 1
                df = pd.DataFrame()
                df['valor'] = y
                df['familia'] = beta
                df['sinal'] = num_sinal
                df_sinais = pd.concat([df_sinais, df])
    return df_sinais


# início do programa principal
if __name__ == '__main__':

    # ==== Entrada de dados ======================================================
    num_valores_por_sinal = [8192]
    num_sinais = 10
    nome_arquivo_pmodel = './sinais_ppmodel.csv'
    nome_arquivo_figura_sinais_endo = 'sinais_endogenos.png'
    nome_arquivo_figura_sinais_exo = 'sinais_exogenos.png'
    nome_arq_saida_todos_momentos = './momentos_pmodel.csv'
    metodos_do_cotovelo = ['distorcao_km_inertia'] #, 'silhueta_yellowbrick'] #, 'distorcao_yellowbrick',
        # 'calinski_harabasz_yellowbrick']
    k_array = range(2, 7)
    is_normalizar_valores = False
    is_plotar_histograma_familia = False
    is_plotar_kmeans_cotovelo = False
    is_plotar_momentos_3d = False

    # endógenas
    arr_p_endo = [0.32, 0.36, 0.42]
    beta_endo = 0.4

    # exógenas
    arr_p_exo = [0.18, 0.22, 0.28]
    beta_exo = 0.7
    # ============================================================================

    df_todos_sinais = None
    if len(arr_p_exo) != len(arr_p_exo):
        print("Programa não adaptado para diferentes números de p por família beta")
        exit(1)
    num_sinais_por_familia = len(arr_p_endo) * num_sinais

    df_endo = gerador_de_sinais_pmodel(num_valores_por_sinal, beta_endo, arr_p_endo, num_sinais)
    plt.plot(df_endo["valor"].to_numpy())
    plt.title("Endogenous Series")
    plt.ylabel("Valores de Amplitude")
    plt.xlabel("N passos no tempo")
    plt.savefig(nome_arquivo_figura_sinais_endo)

    df_exo = gerador_de_sinais_pmodel(num_valores_por_sinal, beta_exo, arr_p_exo, num_sinais)
    plt.plot(df_exo["valor"].to_numpy())
    plt.title("Exogenous Series")
    plt.ylabel("Valores de Amplitude")
    plt.xlabel("N passos no tempo")
    plt.savefig(nome_arquivo_figura_sinais_exo)

    df_todos_sinais = pd.concat([df_todos_sinais, df_endo, df_exo])
    df_todos_sinais.to_csv(nome_arquivo_pmodel, index=False)

    # utilizacao de função do método do exercício 1.2 - Gerador dos momentos variancia, assimetria e curtose
    gerador_de_momentos([beta_endo, beta_exo], num_sinais_por_familia, nome_arquivo_pmodel,
                        nome_arq_saida_todos_momentos,
                        is_normalizar_valores, is_plotar_histograma_familia)

    # utilizacao de função do método do exercício 1.3 - Kmeans e Geração de gráfico de cotovelo
    k_means_e_metodo_do_cotovelo(nome_arq_saida_todos_momentos, k_array, metodos_do_cotovelo, is_plotar_kmeans_cotovelo,
                                 is_plotar_momentos_3d)
