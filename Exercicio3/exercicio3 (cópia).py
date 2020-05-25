
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
    num_sinais = 10
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

