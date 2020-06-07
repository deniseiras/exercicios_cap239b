# Matemática Computacional I - parte A - Prova - Branch Esquerda - Fluxograma
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1o período 2020
# Autores: Denis Eiras
# 02/06/2020 - V1.0
#
#
# Descrição
#
# Utilizar os dados de casos diários do país Bolívia, entre 10/03 a 28/05 e executar as tarefas do fluxograma:
# - (plot 1) - Mostrar o histograma
# - (plot 2) - Identificar a classe estatística no espaço de Cullen-Frey
# - (plot 3) - Ajustar um PDF ao histograma
# - (plot 4) - Calcular o índice espectral Alfa via DFA
# - Estimar o Beta teórico via valor de Alfa
# - (plot 5) - Obter o espectro de singularidades  f(Alfa) x Alfa
# - Calcular Delta de Alfa e A de Alfa = (a0 - amin) / (amax - a0)
# - Plote uma tebela com os valores de Alfa, Beta, Delta de Alfa, a0 e A de Alfa
#
#
# Entradas:
#
# - N: (Inteiro) - Número de dias de dados de COVIDA
# - coluna_agrupadora_covid: (String) = nome da coluna para agrupar a série. Ex. 'location'
# - coluna_serie_covid: (String) Nome da coluna da série, ex:  'new_cases'
# - valor_coluna_agrupador: (String) Valor da coluna agrupadora. Ex: 'Bolivia'
# - coluna_data: (String) Nome da coluna que contém a data. Ex: 'date'
# - data_inicial: (String) Data inicial da serie. Ex: '2020-05-09'
# - data_final: (String) Data final de dados Reais. Ex: '2020-06-05'
# - url_owid_covid_data: : (String) Url para baixar arquivo da COVID.
#   Ex:'https://covid.ourworldindata.org/data/owid-covid-data.csv'
# - nome_arq_covid_completo: (String) Nome do arquivo da covid a salvar. Ex: './owid-covid-data.csv'
#
# Saídas
# - Figura contendo as previsões, os dados observados e as médias para cada espectro de probabilidades.
# - Figura contendo o fator de supressão
#

#


import math

import matplotlib.pyplot as plt
import numpy as np

from Codigos.Specplus import dfa1d
from Codigos.mfdfa_ss_m2 import getMSSByUpscaling
from Exercicio4.exercicio4_1 import graph
from Exercicio4.exercicio4_2_1 import plot_histograma_e_gev


def executa_branch_esquerda(d):

    # (plot 1) - Mostrar o histograma
    str_compl_titulo = '{} de COVID-19 de {}'.format(d.coluna_serie_covid.capitalize(), d.valor_coluna_agrupador)
    arr_valores = d.df_covid_pais_real[d.coluna_serie_covid].to_numpy()
    histogram, bins_edge = np.histogram(arr_valores, bins=20)
    width = 0.7 * (bins_edge[1] - bins_edge[0])
    center = (bins_edge[:-1] + bins_edge[1:]) / 2
    plt.bar(center, histogram, align='center', width=width)
    plt.title('Histograma da série {}'.format(str_compl_titulo))
    plt.xlabel("bin")
    plt.ylabel("Quantidade")
    plt.savefig("./plot_1_histograma.png")
    plt.show()

    # (plot 2) - Identificar a classe estatística no espaço de Cullen-Frey
    graph(arr_valores, boot=100)

    # (plot 3) - Ajustar um PDF ao histograma
    num_total = 100
    c = -1
    loc = 0
    scale = 35
    num_inicio = 0
    num_final = 850
    plot_histograma_e_gev(
        str_compl_titulo,
        d.df_covid_pais_real, c, loc, scale, num_inicio, num_final, num_total,
        nome_coluna=d.coluna_serie_covid)

    # (plot 4) - Calcular o índice espectral Alfa via DFA
    alfa, vetoutput, x, y, reta, error = dfa1d(arr_valores, 1)
    fig = plt.figure()
    if not math.isnan(alfa):
        cor_dfa = 'darkmagenta'
        # DFA axes title:
        texto_dfax = '$log_{10}$ (s)'
        texto_dfay = '$log_{10}$ F(s)'
        texto_titulo_dfa = r'Detrended Fluctuation Analysis $\alpha$ = '

        # Plot DFA
        fig_dfa = fig.add_subplot()
        fig_dfa.plot(x, y, 's', color=cor_dfa, alpha=0.8)
        fig_dfa.plot(x, reta, '-', color=cor_dfa, linewidth=1.5)
        fig_dfa.set_title(texto_titulo_dfa + '%.4f' % alfa, loc='center')
        fig_dfa.set_xlabel(texto_dfax)
        fig_dfa.set_ylabel(texto_dfay)
        fig_dfa.grid()

    else:
        fig_dfa = fig.add_subplot()
        fig_dfa.set_title('Detrended Fluctuation Analysis $\alpha$ = ' + 'N.A.', loc='center')
        fig_dfa.grid()

    # Draw and save figure (avoid showing to prevent blocking)
    # plt.suptitle(title_main, fontsize=size_font_main)
    img_filename = './plot_4_alfa_dfa.png'
    fig.set_size_inches(10, 5)
    plt.savefig(img_filename, dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.show()

    # Estimar o Beta teórico via valor de Alfa
    beta_teorico = 2 * alfa - 1
    print('Beta teórico estimado = {}'.format(beta_teorico))

    # (plot 5) - Obter o espectro de singularidades  f(Alfa) x Alfa
    [_, _, _, stats, _] = getMSSByUpscaling(arr_valores.tolist(), isNormalised=1)
    plt.plot(stats['LH'], stats['f'], 'ko-')
    plt.title('Espectro de singularidades')
    plt.xlabel(r'$\alpha$')
    plt.ylabel(r'$f(\alpha)$')
    plt.grid('on', which='major')
    plt.savefig('./plot_5_espectro_de_singularidades.png')
    plt.show()

    # Calcular Delta de Alfa e A de Alfa = (a0 - amin) / (amax - a0)
    delta_alfa = stats['LH_max'] - stats['LH_min']
    alfa_0 = max(stats['f'])[0]
    a_alfa = (alfa_0 - stats['LH_min']) / (stats['LH_max'] - alfa_0)

    # - Plote uma tebela com os valores de Alfa, Beta, Delta de Alfa, Alfa0 e A de Alfa
    print('Alfa\tBeta\tDelta_Alfa\tAlfa_0\tA_alfa')
    print('{}\t{}\t{}\t{}\t{}'.format(alfa, beta_teorico, delta_alfa, alfa_0, a_alfa))
