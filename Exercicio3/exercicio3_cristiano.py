#P-model from Meneveau & Sreenevasan, 1987 & Malara et al., 2016
#Author: R.R.Rosa & N. Joshi
#Version: 1.6
#Date: 11/04/2018
# Matemática Computacional I - parte B - Exercício 1
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

# O exercício em questão consiste em 3 etapas:
#   1. Executar a função gerador_de_sinais_pmodel, para gerar 2 familias, endógeno e exógeno.
#          
#   2. Cada fámilia terá 30 sinais que seram divididos em 5 grupos de 10 sinais.
#
#   3. Cada grupo receberá um determinado valor dentro de uma faixa p. 
#      Faixa endógeno (0.32-0.42)
#      Faixa exógeno (0.18-0.28)
#
# Entradas:
#
# - valor: é o valor gerado gerado em relação a p e beta.
# - familias: (Array de inteiros) Cada elemento representa uma quantidade de valores do sinal de uma família.
# - sinal: (Inteiro) Número de sinais gerados por família.
# - arr_p_endo: (Array de inteiros) Cada elemento representa um valor dentro da faixa p endógeno.
# - arr_p_exo: (Array de inteiros) Cada elemento representa um valor dentro da faixa p exógeno.
# - beta_endo: 0.4 itentificando a família endógeno.
# - beta_exo: 0.7 itentificando a família exógeno.
# - num_sinais: número de sinais gerados N vezes.
#
# Saídas:
#
# - arquivo csv de nome definido em "nome_arquivo_saida", contendo os sinais e sua família.
# - arquivo csv de nome definido em "nome_arq_saida_todos_momentos", contendo os momentos estatísticos gerados em 2.
# - arquivos contendo classes agrupadas nos espaços de parâmetros variância, assimetria e curtose, para cada k, de
#   nomes "k_#.png", onde # é o número k, gerados em 3.
# - arquivo com gráfico contendo os sinais gerados.

#P-model from Meneveau & Sreenevasan, 1987 & Malara et al., 2016
#Author: R.R.Rosa & N. Joshi
#Version: 1.6
#Date: 11/04/2018

import numpy as np
from matplotlib import pyplot
import matplotlib.pyplot as plt
import pandas as pd
from numpy import sqrt
from pmodel import pmodel


def gerador_de_sinais_pmodel(beta, arr_p, num_sinais, df_todos_sinais):
    for p in arr_p:
        for sinal in range(num_sinais):
            # (setup: N, p: 0.32-0.42, beta=0.4)
            x, y = pmodel(8192, p, beta)
            df = pd.DataFrame()
            df['valor'] = y
            df['familia'] = beta
            df['sinal'] = sinal + 1
            df_todos_sinais = pd.concat([df_todos_sinais, df])
    return df_todos_sinais


# início do programa principal
if __name__ == '__main__':

    # ==== Entrada de dados ======================================================
    num_sinais = 10756
    nome_arquivo_saida = './pmodel.csv'

    # endógenas
    arr_p_endo = [0.32, 0.34, 0.36, 0.40, 0.42]
    beta_endo = 0.4

    # exógenas
    arr_p_exo = [0.18, 0.20, 0.22, 0.26, 0.28]
    beta_exo = 0.7
    # ==== Entrada de dados ======================================================

    df_todos_sinais = None
    df_todos_sinais = gerador_de_sinais_pmodel(beta_endo, arr_p_endo, num_sinais, df_todos_sinais)
    plt.plot(df_todos_sinais["valor"])
    plt.title("Endogenous Series")
    plt.ylabel("Valores de Amplitude")
    plt.xlabel("N passos no tempo")
    pyplot.show()

    df_todos_sinais = gerador_de_sinais_pmodel(beta_exo, arr_p_exo, num_sinais, df_todos_sinais)
    df_todos_sinais.to_csv(nome_arquivo_saida, index=False)
    plt.plot(df_todos_sinais["valor"])
    plt.title("Exogenous Series")
    plt.ylabel("Valores de Amplitude")
    plt.xlabel("N passos no tempo")
    pyplot.show()


