# Matemática Computacional I - parte B - Exercício 2
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1o período 2020
# Autores: Denis Eiras e Cristiano Reis
# 28/04/2020 - V1.0
#
# O exercício em questão consiste em 3 etapas:
#   1. Executar a função gerador_de_sinais_colorednoise, para gerar ruídos gaussianos para cada par de família e sinal,
#      parametrizados neste script.
#   2. Executar a função gerador_de_momentos (exercicio1_2.py), para gerar um arquivo csv, contendo os momentos
#      estatísticos dos sinais gerados em 1.
#   3. Executar a função metodo_do_cotovelo (exercicio1_3), para realizar agrupamento, utilizando o kmeans, para
#      caracterizar, se houver, classes nos espaço de parâmetros composto por variância, skewness e kurtosis. Em
#      seguida, um gráfico com o método do cotovelo é gerado para a análise do melhor k utilizado no kmeans.
#
# Métodos utilizados:
#
# Neste exercício é implementado um gerador de ruído gaussiano com um espectro de leis de potência com expoentes
# arbitrários. Um expoente de dois corresponde ao ruído browniano (red noise). Os expoentes menores produzem correlações
# de longo alcance, ou seja, pink noise para um expoente de 1 (também chamado de ruído 1/f ou ruído de cintilação) e
# white noise, para um expoente de 0.
#
# Baseado no algoritmo em: Timmer, J. e Koenig, M .: Na geração de ruído da lei de energia.
# Astron. Astrophys. 300, 707-710 (1995)
#
# Entradas:
#
# - familias: (Array de inteiros) Cada elemento representa uma quantidade de valores do sinal de uma família
# - num_sinais: (Inteiro) Número de sinais gerados por família
# - betas: (Array de inteiros) array com cada elemento sendo um expoente do ruído. 0 = white noise, 1 = pink noise,
#   2 = red noise.
# - k: (Array) Array contendo número de clusters do algoritmo K-means
# - nome_arquivo_colored_noise: (String) Nome do arquivo de saída com ruídos gaussianos, com extensão .csv
# - metodos_do_cotovelo: (Array de Strings). Métodos do cotovelo a serem plotados. Opções:
#   - distorcao_km_inertia - Utiliza a soma das distâncias ao quadrado utilizado pelo próprio Kmeans do sklearn
#   - distorcao_yellowbrick - Utiliza a soma das distâncias ao quadrado do pacote yellowbrick. Neste gráfico é possível
#       observar a indicação de melhor k e tempo de cálculo de cada k.
#   - silhueta_yellowbrick - Utiliza o método silhueta do pacote yellowbrick. Neste gráfico é possível observar o tempo
#       de cálculo de cada k.
#   - calinski_harabasz_yellowbrick - Utiliza o método silhueta do pacote yellowbrick.
# - is_plotar_sinal_familia: (Boolean) True para plotar o gráfico log log de densidade do Power Sptectrum
# - is_plotar_histograma_familia: (Boolean) True para plotar um histograma exemplo de um sinal da cada família
# - is_plotar_kmeans_cotovelo: (Boolean) True para plotar os gráficos de agrupamento para cada k e o gráfico do cotovelo
#
# Saídas:
#
# - arquivo csv de com ruídos gaussianos, de nome definido na entrada: nome_arquivo_colored_noise
# - arquivo csv de nome definido em "nome_arq_saida_todos_momentos", contendo os momentos estatísticos gerados em 2.
# - arquivos contendo classes agrupadas nos espaços de parâmetros variância, assimetria e curtose, para cada k, de
#   nomes "k_#.png", onde # é o número k, gerados em 3.
# - arquivo com gráfico do cotovelo ("cotovelo.png"), gerado em 3.


import pandas as pd
import colorednoise as cn
from exercicio1_2 import gerador_de_momentos
from exercicio1_3 import k_means_e_metodo_do_cotovelo


def gerador_de_sinais_colored_noise(num_valores_por_sinal, num_sinais, nome_arquivo_colorednoise, betas, is_plotar_exemplo_familia=False):
    df_todos_sinais = None
    for beta in betas:
        for sinal in range(num_sinais):
            for num_valores in num_valores_por_sinal:

                sinais = cn.powerlaw_psd_gaussian(beta, num_valores)
                df = pd.DataFrame()
                df['valor'] = sinais
                # a famílias são as cores
                df['familia'] = beta
                df['sinal'] = sinal + 1
                df_todos_sinais = pd.concat([df_todos_sinais, df])

            if is_plotar_exemplo_familia:
                # plot da densidade do Power Spectral
                from matplotlib import mlab
                from matplotlib import pylab as plt
                s, f = mlab.psd(sinais, NFFT=2 ** 13)
                plt.loglog(f, s)
                plt.grid(True)
                plt.xlabel("log da frequência")
                plt.ylabel("log do valor do Power Spectrum")
                plt.title("Densidade do Power Spectrum para beta = {}".format(beta))
                plt.savefig("./power_spec_beta_{}.png".format(beta))
                plt.show()

    df_todos_sinais.to_csv(nome_arquivo_colorednoise, index=False)
    return df_todos_sinais


# início do programa principal
if __name__ == '__main__':

    # ==== Entrada de dados ======================================================
    num_valores_por_sinal = [8192]
    num_sinais = 20
    # beta 0, 1, 2 = white, pink e red noises
    betas = [0, 1, 2]
    k_array = range(2, 8)
    nome_arquivo_colorednoise = './colored_noise.csv'
    metodos_do_cotovelo = ['distorcao_yellowbrick', 'distorcao_km_inertia', 'silhueta_yellowbrick',
                           'calinski_harabasz_yellowbrick']
    nome_arq_saida_todos_momentos = './momentos_das_familias.csv'
    is_normalizar_valores = False
    is_plotar_histograma_familia = False
    is_plotar_kmeans_cotovelo = True
    is_plotar_sinal_familia = True
    # ============================================================================

    gerador_de_sinais_colored_noise(num_valores_por_sinal, num_sinais, nome_arquivo_colorednoise, betas, is_plotar_sinal_familia)

    # utilizacao de função do método do exercício 1.2 - Gerador dos momentos variancia, assimetria e curtose
    gerador_de_momentos(betas, num_sinais, nome_arquivo_colorednoise, nome_arq_saida_todos_momentos,
                        is_normalizar_valores, is_plotar_histograma_familia)

    # utilizacao de função do método do exercício 1.3 - Kmeans e Geração de gráfico de cotovelo
    k_means_e_metodo_do_cotovelo(nome_arq_saida_todos_momentos, k_array, metodos_do_cotovelo, is_plotar_kmeans_cotovelo)


