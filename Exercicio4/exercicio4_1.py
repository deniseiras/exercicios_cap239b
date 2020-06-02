# Matemática Computacional I - parte B - Exercício 4
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1o período 2020
# Autores: Denis Eiras
# 28/04/2020 - V1.0
#
# Considere duas das séries das famílias N8 dos exercícios anteriores. Classifique as mesmas no espaço de Cullen-Frey.
#
# Métodos utilizados:
#
# Programa cullen_frey_andre_from_R, versão do programa em R adaptada para Python
#
# Entradas:
#
# - num_valores_por_sinal: (Array de inteiros) Cada elemento representa uma quantidade de valores do sinal de uma
#   família.
# - num_sinais: (Inteiro) Número de sinais gerados por família.
# - nome_arquivo_sinais_endogenos: (String) Nome do arquivo de saída dos sinais endógenos gerados
# - nome_arquivo_sinais_exogenos: (String) Nome do arquivo de saída dos sinais exógenos gerados
#
# Saídas:
#
# - nome_arquivo_sinais_endogenos: Arquivo de saída dos sinais endógenos gerados
# - nome_arquivo_sinais_exogenos: Arquivo de saída dos sinais exógenos gerados
#

from Exercicio2.exercicio2 import gerador_de_sinais_colored_noise
from Exercicio3.exercicio3 import gerador_de_sinais_pmodel
from Exercicio4.cullen_frey_andre_from_R import graph

# início do programa principal
if __name__ == '__main__':
    # ==== Entrada de dados ======================================================
    num_valores_por_sinal = [256]
    num_sinais = 1
    nome_arquivo_sinais_endogenos = './resultados_4_1/sinais_endogenos.csv'
    nome_arquivo_sinais_exogenos = './resultados_4_1/sinais_exogenos.csv'
    # ============================================================================

    # endógenas
    arr_p_endo = [0.32, 0.36, 0.42]
    beta_endo = 0.4

    # exógenas
    arr_p_exo = [0.18, 0.22, 0.28]
    beta_exo = 0.7

    num_sinais_por_familia = len(arr_p_endo) * num_sinais
    df_sinais = gerador_de_sinais_pmodel(num_valores_por_sinal, beta_endo, arr_p_endo, num_sinais)
    graph(df_sinais['valor'], boot=100)
    df_sinais.to_csv(nome_arquivo_sinais_endogenos)

    df_sinais = gerador_de_sinais_pmodel(num_valores_por_sinal, beta_exo, arr_p_exo, num_sinais)
    graph(df_sinais['valor'], boot=100)
    df_sinais.to_csv(nome_arquivo_sinais_exogenos)
