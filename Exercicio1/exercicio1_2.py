# Matemática Computacional I - parte B - Exercício 1.2
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1o período 2020
# Autores: Denis Eiras e Cristiano Reis
# 28/04/2020 - V1.0
#
# O exercício consiste em ler os elementos gerados pelo exercício 1.1, normalizar os valores entre 0 e 1 e gerar:
#
# 1. O histograma
# 2. Os três momentos estatísticos, para cada sinal de cada família, em um arquivo contendo csv contendo as colunas:
#   2.1 variância
#   2.2 assimetria
#   2.3 curtose
#
# Entradas:
#
# - familias: (Array de inteiros) Cada elemento representa uma família de sinais
# - num_sinais: (Inteiro) Número de sinais gerados por família
# - nome_arquivo_entrada: (String) Nome do arquivo de entrada, gerado no exercicio1_1.py, com extensão .csv
# - nome_arq_saida_todos_momentos: (String) Nome do arquivo csv contendo os momentos estatísticos, nas colunas
#   variância, assimetria e curstose, e as informações de família e sinal, nas colunas familia e sinal.
# - is_plotar_histograma_familia: (Boolean) True para plotar um histograma exemplo de um sinal da cada família
#
# Saídas:
#
# - arquivo csv contendo os momentos estatísticos, nas colunas variância, assimetria e curstose, e as informações de
#   família e sinal, nas colunas familia e sinal.
#   Cabeçaho: familia, sinal, variancia, assimetria e curtose
#

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def gerador_de_momentos(familias, num_sinais, nome_arquivo_entrada, nome_arq_saida_todos_momentos,
                        is_normalizar_valores, is_plotar_histograma_familia):
    # leitura dos elementos gerados: 10 séries de cada família:
    df = pd.read_csv(nome_arquivo_entrada, sep=',')
    # normalização dos valores entre 0 e 1
    df_elem_normalizados = df.copy()
    if is_normalizar_valores:
        valores = df_elem_normalizados['valor']
        df_elem_normalizados['valor'] = (valores - valores.min()) / (valores.max() - valores.min())
    # DataFrame contendo todos os momentos, por familia e sinal
    df_todos_momentos = pd.DataFrame(columns=['variancia', 'assimetria', 'curtose'])
    for familia in familias:
        for sinal in range(1, num_sinais + 1):
            str_fam_sinal = 'Familia = {} , Sinal = {}'.format(familia, sinal)
            print('\n\n{}\n===============\n'.format(str_fam_sinal))

            # elementos pertencentes à família e sinal:
            df_is_elem_da_familia_e_sinal = (df_elem_normalizados['familia'] == familia) & (
                    df_elem_normalizados['sinal'] == sinal)
            df_elem_norm_familia_e_sinal = df_elem_normalizados[df_is_elem_da_familia_e_sinal]

            # 1.0 histograma
            arr_valores_atuais = df_elem_norm_familia_e_sinal['valor'].to_numpy()
            histogram, bins_edge = np.histogram(arr_valores_atuais, bins=20)

            # 2.1 variância
            variancia = df_elem_norm_familia_e_sinal['valor'].var()
            print('Variância = {}'.format(variancia))

            # 2.2 assimetria
            assimetria = df_elem_norm_familia_e_sinal['valor'].skew()
            print('Assimetria = {}'.format(assimetria))

            # 2.3 curtose
            # The pandas library function kurtosis() computes the Fisher's Kurtosis
            # which is obtained by subtracting the Pearson's Kurtosis by three.
            curtose = df_elem_norm_familia_e_sinal['valor'].kurtosis()
            print('Curtose = {}'.format(curtose))

            # Concatenando os momentos da familia e sinal atual no df geral
            df_todos_momentos = df_todos_momentos.append({'variancia': variancia, 'assimetria': assimetria,
                                                          'curtose': curtose}, ignore_index=True)

            # Plot Histograma
            plt.clf()
            width = 0.7 * (bins_edge[1] - bins_edge[0])
            center = (bins_edge[:-1] + bins_edge[1:]) / 2
            plt.bar(center, histogram, align='center', width=width)
            plt.title('Histograma da {}'.format(str_fam_sinal))
            plt.xlabel("bin")
            plt.ylabel("Quantidade")
            plt.savefig("./histograma_fam_{}_sinal_{}.png".format(familia, sinal))
            if is_plotar_histograma_familia:
                plt.show()
            plt.close('all')

    df_todos_momentos.to_csv(nome_arq_saida_todos_momentos, index=False)
