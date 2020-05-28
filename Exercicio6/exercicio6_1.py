# Matemática Computacional I - parte B - Exercício 6
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1o período 2020
# Autores: Denis Eiras
# 18/05/2020 - V1.0
#
#
# Descrição
#
# 6.1. Considere as séries temporais listadas na tabela dataset_signal e obtenha, para cada série, os valores
# respectivos do seguintes atributos: S 2 , K, β (via PSD) e α (via DFA). Confira para todas as series se
# β (via PSD) está bem ajustado a partir da formula WKP: β = 2 α – 1. Construa dois espaços de parâmetros
# EPSB-K-means: S 2 x K x β e EDF-K-means: S 2 x K x α .
#
#
# Entradas:
#
# - is_plot_comparacao_beta: (Boolean) True para plotar na tela o arquivo de comparação alfa_x_beta
# - nome_arquivo_espaco_param_ESPB: (String) Nome do arquivo de espaços de parâmetros ESPB gerado
# - nome_arquivo_espaco_param_EDF: (String) Nome do arquivo de espaços de parâmetros EDF gerado
# Nomes de arquivos que devem ser alterados para cada dataset:
# - nome_arq_tabela_estatística: (String) Nome do arquivo de estatísticas.
# - nome_arquivo_fig_alfa_x_beta: (String) Nome da figura comparativa Beta = 2 x Alfa - 1 contra uma reta interpoladora
#   dos pontos dos sinais.
#
# Saídas:
#
# - Arquivo de espaços de parâmetros ESPB gerado, de nome "nome_arquivo_espaco_param_ESPB"
# - Arquivo de espaços de parâmetros EDF gerado, de nome "nome_arquivo_espaco_param_EDF"
# - Arquivo de estatísticas para cada sinal, de nome "nome_arq_tabela_estatística" para cada dataset
# - Arquivo Figura comparativa Beta = 2 x Alfa - 1, de nome "nome_arquivo_fig_alfa_x_beta" para cada dataset


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from Exercicio1.exercicio1_1 import gerador_de_sinais_aleatorios
from Exercicio2.exercicio2 import gerador_de_sinais_colored_noise
from Exercicio3.exercicio3 import gerador_de_sinais_pmodel
from Exercicio5.exercicio5_1 import gerador_de_sinais_logisticos, gerador_de_sinais_henon
from Exercicio6.specplus import psd, dfa1d


def calcula_df_estatistico_por_familia_e_sinal(df_sinais, nome_arq_tabela_estatística):
    df_stats = None
    for familia in df_sinais.familia.unique():
        for sinal in df_sinais.sinal.unique():
            # elementos pertencentes à família e sinal:
            df_is_elem_da_familia_e_sinal = (df_sinais['familia'] == familia) & (
                    df_sinais['sinal'] == sinal)
            df = df_sinais[df_is_elem_da_familia_e_sinal]
            valores = df.valor

            df = calcula_df_estatistico(valores)
            df_stats = pd.concat([df_stats, df])

    df_stats.to_csv(nome_arq_tabela_estatística, index=False)
    return df_stats


def calcula_df_estatistico(valores):
    df = pd.DataFrame()
    df['variancia_ao_quadrado'] = pd.Series(valores.var() ** 2)
    df['curtose'] = valores.kurtosis()
    freqs, power, xdata, ydata, amp, index, powerlaw, INICIO, FIM = psd(valores)
    beta = index
    df['beta'] = beta
    alfa, vetoutput, x, y, reta, erro = dfa1d(valores, 1)
    df['alfa'] = alfa
    df['beta_calc'] = 2 * df['alfa'] - 1
    return df


def plot_comparacao_beta(df_estatisticas, nome_arquivo_fig_alfa_x_beta, titulo, is_plot_comparacao_beta):
    # plot
    fig, ax = plt.subplots()
    ax.scatter(df_estatisticas['alfa'], df_estatisticas['beta'], color='blue')
    ax.plot(np.unique(df_estatisticas['alfa']),
             np.poly1d(np.polyfit(df_estatisticas['alfa'], df_estatisticas['beta'], 1))(
                 np.unique(df_estatisticas['alfa'])), color='cyan', label='interpolação de {}'.format(titulo))
    ax.scatter(df_estatisticas['alfa'], df_estatisticas['beta_calc'], color='red')
    ax.plot(df_estatisticas['alfa'], df_estatisticas['beta_calc'], color='magenta', label='Beta = 2 x Alfa - 1')
    plt.legend()
    plt.xlabel('Alfa')
    plt.ylabel('Beta')
    plt.title(titulo)
    plt.savefig(nome_arquivo_fig_alfa_x_beta)
    if is_plot_comparacao_beta:
        plt.show()


# início do programa principal
if __name__ == '__main__':

    # Parâmetros de entrada gerais ===================================
    is_plot_comparacao_beta = False
    nome_arquivo_todos_sinais = './todos_sinais.csv'
    nome_arquivo_espaco_param_ESPB = './espaco_param_ESPB.csv'
    nome_arquivo_espaco_param_EDF = './espaco_param_EDF.csv'

    # ================================================================

    # Gerando sinais noise ===========================================
    nome_arq_tabela_estatística = 'estatisticas_noise.csv'
    nome_arquivo_fig_alfa_x_beta = './alfa_x_beta_noise.png'
    familias = [64, 128, 256, 512, 1024, 2048, 4096, 8192]
    num_sinais = 10
    nome_arquivo_noise = './noise.csv'
    df_sinais_noise = gerador_de_sinais_aleatorios(familias, num_sinais, nome_arquivo_noise)
    df_estatisticas_noise = calcula_df_estatistico_por_familia_e_sinal(df_sinais_noise, nome_arq_tabela_estatística)
    # Verificando graficamente se as séries estão bem ajustadas à fórmula WKP: Beta = 2 x alfa – 1
    plot_comparacao_beta(df_estatisticas_noise, nome_arquivo_fig_alfa_x_beta, "Noise", is_plot_comparacao_beta)

    # Gerando sinais colored noise ===================================
    nome_arq_tabela_estatística = 'estatisticas_colorednoise.csv'
    nome_arquivo_fig_alfa_x_beta = './alfa_x_beta_colorednoise.png'
    num_valores_por_sinal = [8192]
    num_sinais = 20
    # beta 0, 1, 2 = white, pink e red noises
    betas_calculados = [0, 1, 2]
    nome_arquivo_colorednoise = './colored_noise.csv'
    df_sinais_colored_noise = gerador_de_sinais_colored_noise(num_valores_por_sinal, num_sinais, nome_arquivo_colorednoise,
                                                              betas_calculados)
    df_estatisticas_colored_noise = calcula_df_estatistico_por_familia_e_sinal(df_sinais_colored_noise, nome_arq_tabela_estatística)
    # Verificando graficamente se as séries estão bem ajustadas à fórmula WKP: Beta = 2 x alfa – 1
    plot_comparacao_beta(df_estatisticas_colored_noise, nome_arquivo_fig_alfa_x_beta, "Colored Noise", is_plot_comparacao_beta)

    # Gerando sinais pmnoise =========================================
    nome_arq_tabela_estatística = 'estatisticas_pmnoise.csv'
    nome_arquivo_fig_alfa_x_beta = './alfa_x_beta_pmnoise.png'
    num_valores_por_sinal = [8192]
    num_sinais = 10
    # endógenas
    arr_p_endo = [0.32, 0.36, 0.42]
    beta_endo = 0.4
    # exógenas
    arr_p_exo = [0.18, 0.22, 0.28]
    beta_exo = 0.7
    num_sinais_por_familia = len(arr_p_endo) * num_sinais
    df_endo = gerador_de_sinais_pmodel(num_valores_por_sinal, beta_endo, arr_p_endo, num_sinais)
    df_exo = gerador_de_sinais_pmodel(num_valores_por_sinal, beta_exo, arr_p_exo, num_sinais)
    df_sinais_pnoise = pd.concat([df_endo, df_exo])
    df_estatisticas_pnoise = calcula_df_estatistico_por_familia_e_sinal(df_sinais_pnoise, nome_arq_tabela_estatística)
    # Verificando graficamente se as séries estão bem ajustadas à fórmula WKP: Beta = 2 x alfa – 1
    plot_comparacao_beta(df_estatisticas_pnoise, nome_arquivo_fig_alfa_x_beta, "P Noise", is_plot_comparacao_beta)

    # Gerando sinais chaosnoise =======================================
    nome_arq_tabela_estatística = 'estatisticas_chaosnoise.csv'
    nome_arquivo_fig_alfa_x_beta = './alfa_x_beta_chaosnoise.png'
    num_sinais = 30
    valores_por_sinal = 8192
    df_sinais_log = gerador_de_sinais_logisticos(num_sinais, valores_por_sinal)
    df_sinais_henon = gerador_de_sinais_henon(num_sinais, valores_por_sinal)
    df_sinais_chaosnoise = pd.concat([df_sinais_log, df_sinais_henon])
    df_estatisticas_chaosnoise = calcula_df_estatistico_por_familia_e_sinal(df_sinais_chaosnoise, nome_arq_tabela_estatística)
    # Verificando graficamente se as séries estão bem ajustadas à fórmula WKP: Beta = 2 x alfa – 1
    plot_comparacao_beta(df_estatisticas_chaosnoise, nome_arquivo_fig_alfa_x_beta, "Chaos Noise", is_plot_comparacao_beta)

    # Criando os espaços de parâmetros EPSB-K-means: S 2 x K x β e EDF-K-means: S 2 x K x α .
    df_todos_espacos = pd.concat([df_estatisticas_noise, df_estatisticas_colored_noise, df_estatisticas_pnoise, df_estatisticas_chaosnoise])
    df_espaco_param_ESPB = df_todos_espacos[['variancia_ao_quadrado', 'curtose', 'beta']]
    df_espaco_param_ESPB.to_csv(nome_arquivo_espaco_param_ESPB, index=False)
    df_espaco_param_EDF = df_todos_espacos[['variancia_ao_quadrado', 'curtose', 'alfa']]
    df_espaco_param_EDF.to_csv(nome_arquivo_espaco_param_EDF, index=False)

