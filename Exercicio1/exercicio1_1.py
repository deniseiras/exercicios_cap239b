# Matemática Computacional I - parte B - Exercício 1.1
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1o período 2020
# Aluno: Denis Eiras
#
# Programa adaptado de:
# Gerador de Série Temporal Estocástica - V.1.2.0
# Autor: R.R.Rosa - V 1.2.0
#
# Modificações: Denis Eiras 28/04/2020 - V1.3.0
#
# Trata-se de um gerador randômico não-gaussiano sem classe de universalidade via PDF.
#
# Objetivo:
#
# Gerar sinais para cada família de números aleatórios.
# O resultado é armazenado no arquivo de nome definido na variável de entrada: nome_arquivo_saida
#
# Entradas:
#
# - familias: (Array de inteiros) Cada elemento representa uma quantidade de valores do sinal de uma família
# - num_sinais: (Inteiro) Número de sinais gerados por família
# - nome_arquivo_saida: (String) Nome do arquivo de saída com extensão .csv
#
# Saídas:
# - data set contendo os valores dos sinais gerados, agrupados em 3 colunas: familia, num_sinal, valor.
# - arquivo csv contendo os valores dos sinais gerados, agrupados em 3 colunas: familia, num_sinal, valor.
#

import numpy as np
import pandas as pd
from numpy import sqrt


def gerador_de_sinais_aleatorios(familias, num_sinais, nome_arquivo_saida):
    df_todos_sinais = None
    for familia in familias:
        for sinal in range(num_sinais):
            res = familia / 12
            # usa-se a família de menor amplitude no cálculo de todos os sinais (famílias[0])
            df_tmp = pd.DataFrame(np.random.randn(familia) * sqrt(res) * sqrt(1 / familias[0])).cumsum()
            df = pd.DataFrame()
            df['valor'] = df_tmp[0]
            df['familia'] = familia
            df['sinal'] = sinal + 1
            df_todos_sinais = pd.concat([df_todos_sinais, df])
    df_todos_sinais.to_csv(nome_arquivo_saida, index=False)
    return df_todos_sinais
