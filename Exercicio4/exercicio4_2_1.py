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
# scipy.stats.genextreme
#
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.genextreme.html
#
# Entradas:
#
# - nome_arquivo: (String) nome do arquivo com os sinais a serem plotados
# Parâmetros para geração da PDF e ajuste do histograma:
# - c: (Float) Parâmetro da forma da distribuição
# - loc: (Float) Parâmetro de Localização
# - scale: (Float) Parâmetro de Escala
# - num_inicio: (Float) Início da PDF
# - num_final:(Float) Fim da PDF
#
# Saídas:
#
# Figura com plot do histograma e curva GEV ajustada
#

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import genextreme


def plot_histograma_e_gev(str_fam_sinal, df_sinais, c, loc, scale, num_inicio, num_final, num_total,
                          nome_coluna='valor'):
    arr_valores_atuais = df_sinais[nome_coluna].to_numpy()
    histogram, bins_edge = np.histogram(arr_valores_atuais, bins=20)

    width = 0.7 * (bins_edge[1] - bins_edge[0])
    center = (bins_edge[:-1] + bins_edge[1:]) / 2

    # plot histograma
    # fig, ax = plt.subplots(1, 1)
    fig, ax1 = plt.subplots()
    color = 'tab:blue'
    plt.bar(center, histogram, align='center', width=width)
    plt.title('Histograma da Série {}'.format(str_fam_sinal))
    plt.xlabel("bin")
    plt.ylabel("Quantidade")
    ax1.tick_params(axis='y', labelcolor=color)

    # plot PDF
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
    num_total = 100

    # Para descobrir os parâmetros da curva PDF, execute o somente o trecho abaixo para encontrar melhores parametros c,
    # loc e scale, num_inicio, num_final, num_total. O prompt solicitará esses parâmtetros. Vá executando até conseguir
    # ajustar ao histograma.

    # ========INICIO=================================================================================================
    # nome_arquivo = './sinais_teste.csv'
    # while True:
    #     c = float(input("c:"))
    #     loc = float(input("loc:"))
    #     scale = float(input("scale:"))
    #     num_inicio = float(input('num inicial:'))
    #     num_final = float(input('num final:'))
    #     plot_histograma_e_gev('TIPO_SERIE', df_sinais, c, loc, scale, num_inicio, num_final, num_total)
    # ========FIM=================================================================================================

    # pmodel - série endógena
    nome_arquivo = './resultados_4_1/sinais_endogenos.csv'
    df_sinais = pd.read_csv(nome_arquivo)
    c = 0.3
    loc = -1.0
    scale = 1.0
    num_inicio = -1.0
    num_final = 10.0
    plot_histograma_e_gev('P-Model Endógeno', df_sinais, c, loc, scale, num_inicio, num_final, num_total)

    # pmodel - série exógena
    nome_arquivo = './resultados_4_1/sinais_exogenos.csv'
    df_sinais = pd.read_csv(nome_arquivo)
    c = 0.2
    loc = 0
    scale = 1.0
    num_inicio = 1.0
    num_final = 50.0
    df_sinais = pd.read_csv(nome_arquivo)
    plot_histograma_e_gev('P-Model exógeno', df_sinais, c, loc, scale, num_inicio, num_final, num_total)
