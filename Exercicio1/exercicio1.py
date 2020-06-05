# Matemática Computacional I - parte B - Exercício 1
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1o período 2020
# Autores: Denis Eiras
# 28/04/2020 - V1.0
#
# O exercício em questão consiste em 3 etapas:
#   1. Executar a função gerador_de_sinais_aleatorios (exercicio1_1.py), para as famílias e sinais parametrizadas neste
#   2. Executar a função gerador_de_momentos (exercicio1_2.py), para gerar um arquivo csv, contendo os momentos
#      estatísticos dos sinais gerados em 1.
#   3. Executar a função metodo_do_cotovelo (exercicio1_3), para realizar agrupamento, utilizando o kmeans, para
#      caracterizar, se houver, classes nos espaço de parâmetros composto por variância, skewness e kurtosis. Em
#      seguida, um gráfico com o método do cotovelo é gerado para a análise do melhor k utilizado no kmeans.
#
# Entradas:
#
# - familias: (Array de inteiros) Cada elemento representa uma quantidade de valores do sinal de uma família
# - num_sinais: (Inteiro) Número de sinais gerados por família
# - k: (Array) Array contendo número de clusters do algoritmo K-means
# - nome_arquivo_saida: (String) Nome do arquivo de saída com os sinais, gerados em 1. , com extensão .csv
# - nome_arq_saida_todos_momentos: (String) Nome do arquivo csv contendo os momentos estatísticos, nas colunas
# - metodos_do_cotovelo: (Array de Strings). Métodos do cotovelo a serem plotados. Opções:
#   - distorcao_km_inertia - Utiliza a soma das distâncias ao quadrado utilizado pelo próprio Kmeans do sklearn
#   - distorcao_yellowbrick - Utiliza a soma das distâncias ao quadrado do pacote yellowbrick. Neste gráfico é possível
#     observar a indicação de melhor k e tempo de cálculo de cada k.
#   - silhueta_yellowbrick - Utiliza o método silhueta do pacote yellowbrick. Neste gráfico é possível observar o tempo
#     de cálculo de cada k.
#   - calinski_harabasz_yellowbrick - Utiliza o método silhueta do pacote yellowbrick.
#   variância, assimetria e curstose, e as informações de família e sinal, nas colunas familia e sinal.
# - is_normalizar_valores: (Boolean) Indica se os valores armazenados no arquivo de momenteos deverão ser normalizados.
# - is_plotar_histograma_familia: (Boolean) True para plotar um histograma exemplo de um sinal da cada família
# - is_plotar_kmeans_cotovelo: (Boolean) True para plotar os gráficos de agrupamento para cada k e o gráfico do cotovelo
# - is_plotar_momentos_3d: (Boolean) True para plotar os gráficos com os momentos estatísticos em 3 dimensões
#
# Saídas:
#
# - arquivo csv de nome definido em "nome_arquivo_saida", contendo os sinais, gerados em 1.
# - arquivo csv de nome definido em "nome_arq_saida_todos_momentos", contendo os momentos estatísticos gerados em 2.
# - arquivos contendo classes agrupadas nos espaços de parâmetros variância, assimetria e curtose, para cada k, de
#   nomes "k_#.png", onde # é o número k, gerados em 3.
# - arquivo com gráficos do cotovelo, silhueta ou outros, de nome definidos pelo nome do método + ".png", gerado em 3.

from Exercicio1.exercicio1_1 import gerador_de_sinais_aleatorios
from Exercicio1.exercicio1_2 import gerador_de_momentos
from Exercicio1.exercicio1_3 import k_means_e_metodo_do_cotovelo

# início do programa principal
if __name__ == '__main__':
    # ==== Entrada de dados ======================================================
    familias = [64, 128, 256, 512, 1024, 2048, 4096, 8192]
    num_sinais = 10
    k_array = range(2, 8)
    nome_arquivo_saida = './elementos.csv'
    nome_arq_saida_todos_momentos = './momentos_das_familias.csv'
    metodos_do_cotovelo = ['distorcao_yellowbrick', 'distorcao_km_inertia', 'silhueta_yellowbrick',
                           'calinski_harabasz_yellowbrick']
    is_normalizar_valores = True
    is_plotar_histograma_familia = False
    is_plotar_kmeans_cotovelo = True
    is_plotar_momentos_3d = False
    # ============================================================================

    gerador_de_sinais_aleatorios(familias, num_sinais, nome_arquivo_saida)

    # utilizacao de função do método do exercício 1.2 - Gerador dos momentos variancia, assimetria e curtose
    gerador_de_momentos(familias, num_sinais, nome_arquivo_saida, nome_arq_saida_todos_momentos,
                        is_normalizar_valores, is_plotar_histograma_familia)

    # utilizacao de função do método do exercício 1.3 - Kmeans e Geração de gráfico de cotovelo
    k_means_e_metodo_do_cotovelo(nome_arq_saida_todos_momentos, k_array, metodos_do_cotovelo, is_plotar_kmeans_cotovelo,
                                 is_plotar_momentos_3d)
