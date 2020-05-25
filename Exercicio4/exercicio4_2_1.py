# Matemática Computacional I - parte B - Exercício 4.2.1
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1o período 2020
# Autores: Denis Eiras e Cristiano Reis
# 28/04/2020 - V1.0
#
# Escreva (ou utilize) um algoritmo em Python que permita ajustar uma PDF (Gaussiana ou GEV) # aos respectivos
# histogramas selecionadas em 4.1
#
# Métodos utilizados:
#
# Entradas:
#
#
# Saídas:
#

from exercicio2 import gerador_de_sinais_colored_noise
from exercicio3 import gerador_de_sinais_pmodel
from cullen_frey_andre_from_R import graph
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import genextreme
import pandas as pd


def plot_histograma_e_gev(str_fam_sinal, df_sinais, c, loc, scale, num_inicio, num_final, num_total):
    arr_valores_atuais = df_sinais['valor'].to_numpy()
    histogram, bins_edge = np.histogram(arr_valores_atuais, bins=20)

    width = 0.7 * (bins_edge[1] - bins_edge[0])
    center = (bins_edge[:-1] + bins_edge[1:]) / 2

    #plot histograma
    # fig, ax = plt.subplots(1, 1)
    fig, ax1 = plt.subplots()
    color = 'tab:blue'
    plt.bar(center, histogram, align='center', width=width)
    plt.title('Histograma da {}'.format(str_fam_sinal))
    plt.xlabel("bin")
    plt.ylabel("Quantidade")
    ax1.tick_params(axis='y', labelcolor=color)

    # plot GEV
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:ref'
    x = np.linspace(genextreme.ppf(0.01, c), genextreme.ppf(0.99, c), 100)
    x = np.linspace(num_inicio, num_final, num_total)
    ax2.get_yaxis().set_ticks([])
    ax2.plot(x, genextreme.pdf(x, c, loc, scale), 'r-', lw=5, alpha=0.6, label='genextreme pdf')

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig("./histograma_familia_{}.png".format(str_fam_sinal))
    plt.show()
    plt.close()


# início do programa principal
if __name__ == '__main__':

    # white noise
    betas = [0]
    nome_arquivo_colorednoise = './white_noise.csv'
    df_sinais = pd.read_csv(nome_arquivo_colorednoise)

    # execute o programa, que irá executar o trecho abaixo para encontrar melhores parametros c, loc e scale,
    # num_inicio, num_final, num_total. O prompt solicitará esses parâmtetros. Vá executando até conseguir ajustar ao
    # histograma. Faça para white noise e pmodel
    # ========INICIO=================================================================================================
    while True:
        # c = 0.2
        # loc = 1.0
        # scale = 1.0
        c = float(input("c"))
        loc = float(input("loc"))
        scale = float(input("scale"))
        num_inicio = float(input('num inicial'))
        num_final = float(input('num_final'))
        num_total = int(input('num_total'))

        plot_histograma_e_gev('White_Noise', df_sinais, c, loc, scale, num_inicio, num_final, num_total)
    # ========FIM=================================================================================================





    # white noise
    # c = 0.2
    # loc = 1.0
    # scale = 1.0
    # num_inicio = 0.01
    # num_final = 0.99
    # num_total = 100
    nome_arquivo_colorednoise = './white_noise.csv'
    df_sinais = pd.read_csv(nome_arquivo_colorednoise)
    plot_histograma_e_gev('White_Noise', df_sinais, c, loc, scale, num_inicio, num_final, num_total)

    # pmodel - série exógena
    # c = 0.2
    # loc = 1.0
    # scale = 1.0
    # num_inicio = 0.01
    # num_final = 0.99
    # num_total = 100
    nome_arquivo_pmodel = './sinais_ppmodel.csv'
    df_sinais = pd.read_csv(nome_arquivo_pmodel)
    plot_histograma_e_gev('P-Model exógeno', df_sinais, c, loc, scale, num_inicio, num_final, num_total)
