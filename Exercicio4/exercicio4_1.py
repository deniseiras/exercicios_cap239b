# Matemática Computacional I - parte B - Exercício 4
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1o período 2020
# Autores: Denis Eiras e Cristiano Reis
# 28/04/2020 - V1.0
#
# Considere duas das séries das famílias N8 dos exercícios anteriores. Classifique as mesmas no espaço de Cullen-Frey.
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

# início do programa principal
if __name__ == '__main__':

    # ==== Entrada de dados ======================================================
    num_valores_por_sinal = [256]
    num_sinais = 1
    is_plotar_sinal_familia = False
    # ============================================================================

    betas = [0]
    nome_arquivo_colorednoise = './white_noise.csv'
    df_sinais = gerador_de_sinais_colored_noise(num_valores_por_sinal, num_sinais, nome_arquivo_colorednoise, betas)
    graph(df_sinais['valor'], boot=100)

    betas = [1]
    nome_arquivo_colorednoise = './pink_noise.csv'
    df_sinais = gerador_de_sinais_colored_noise(num_valores_por_sinal, num_sinais, nome_arquivo_colorednoise, betas)
    graph(df_sinais['valor'], boot=100)

    betas = [2]
    nome_arquivo_colorednoise = './red_noise.csv'
    df_sinais_red = gerador_de_sinais_colored_noise(num_valores_por_sinal, num_sinais, nome_arquivo_colorednoise, betas)
    graph(df_sinais_red['valor'], boot=100)

    nome_arquivo_pmodel = './sinais_ppmodel.csv'
    # endógenas
    arr_p_endo = [0.32, 0.36, 0.42]
    beta_endo = 0.4

    # exógenas
    arr_p_exo = [0.18, 0.22, 0.28]
    beta_exo = 0.7

    num_sinais_por_familia = len(arr_p_endo) * num_sinais
    df_sinais = gerador_de_sinais_pmodel(num_valores_por_sinal, beta_endo, arr_p_endo, num_sinais)
    graph(df_sinais['valor'], boot=100)

    df_sinais = gerador_de_sinais_pmodel(num_valores_por_sinal, beta_exo, arr_p_exo, num_sinais)
    graph(df_sinais['valor'], boot=100)