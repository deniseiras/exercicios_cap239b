# Matemática Computacional I - parte B - Exercício 1.3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1o período 2020
# Autores: Denis Eiras
# 28/04/2020 - V1.0
#
# O exercício deve executar o algoritmo K-means para tentar agrupar classes nos espaços de parâmetros variância,
# assimetria e curtose.
# Exibir os agrupamentos graficamente.
# Utilizar técnicas para descobrir o melhor k.
#
# Observações:
#
# O método do "cotovelo" ajuda a selecionar o número ideal de clusters. Se o gráfico de linhas se assemelhar a um braço,
# o “cotovelo” (o ponto de inflexão na curva) é uma boa indicação de que o modelo subjacente se encaixa melhor nesse
# ponto.
#
# Outras 2 técnicas também foram utilizadas, do pacote yellowbrick, classe KElbowVisualizer: A técnica da silhueta e a
# técnica calinski_harabasz. A técnica da silhueta utiliza uma pontuação do coeficiente médio da silhueta de todas as
# amostras, enquanto a pontuação calinski_harabasz calcula a taxa de dispersão entre e dentro dos clusters.
#
# Entradas:
#
# df_momentos_familias: nome do arquivo com momentos das familias, gerados pelo programa exercicio1_2.py
# k: (Array) Array contendo número de clusters do algoritmo K-means
# - metodos_do_cotovelo: (Array de Strings). Métodos do cotovelo a serem plotados. Opções:
#   - distorcao_km_inertia - Utiliza a soma das distâncias ao quadrado utilizado pelo próprio Kmeans do sklearn
#   - distorcao_yellowbrick - Utiliza a soma das distâncias ao quadrado do pacote yellowbrick. Neste gráfico é possível
#       observar a indicação de melhor k e tempo de cálculo de cada k.
#   - silhueta_yellowbrick - Utiliza o método silhueta do pacote yellowbrick. Neste gráfico é possível observar o tempo
#       de cálculo de cada k.
#   - calinski_harabasz_yellowbrick - Utiliza o método silhueta do pacote yellowbrick.
# is_plotar_kmeans_cotovelo: (Boolean) True para plotar os gráficos de agrupamento para cada k e o gráfico do cotovelo
#
# Saídas:
# - arquivos contendo classes agrupadas nos espaços de parâmetros variância, assimetria e curtose, para cada k, de
#   nomes "k_#.png", onde # é o número k
# - arquivo com gráficos do cotovelo, silhueta ou outros, de nome definidos pelo nome do método + ".png".


import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
from mpl_toolkits.mplot3d.axes3d import Axes3D
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
from yellowbrick.cluster import SilhouetteVisualizer


# função auxiliar para gerar e plotar o k-meeans
def analisador_k_means(df_momentos_familias, np_elem_norm, k, is_plotar, is_plotar_momentos_3d=True):
    kmeans = KMeans(n_clusters=int(k), random_state=0)
    kmeans.fit(np_elem_norm)
    print(
        ' CLUSTERS KMEANS K={} ==============================================================================='.format(
            k))
    print(kmeans.cluster_centers_)
    df_momentos_familias['classes'] = kmeans.labels_
    try:
        grid = sb.pairplot(df_momentos_familias, hue='classes')
        grid.savefig("./k_{}.png".format(k))
        if is_plotar:
            plt.show()
        plt.close('all')
    except Exception as re:
        if str(re).startswith('Selected KDE bandwidth is 0. Cannot estiamte density'):
            grid = sb.pairplot(df_momentos_familias, hue='classes', kde_kws={'bw': 0.1})
            grid.savefig("./k_{}.png".format(k))
            if is_plotar:
                plt.show()
            plt.close('all')
        else:
            raise re

    if is_plotar_momentos_3d:
        fig1 = plt.figure()
        fig1.add_subplot(111, projection='3d')
        ax = Axes3D(fig1, rect=[0, 0, 1, 1], elev=20, azim=-35)
        ax.scatter(df_momentos_familias['variancia'],
                   df_momentos_familias['assimetria'],
                   df_momentos_familias['curtose'],
                   c=df_momentos_familias['classes'],
                   edgecolor='black', s=25)
        ax.set_xlabel('Variância')
        ax.set_ylabel('Assimetrua')
        ax.set_zlabel('Curtose')
        plt.savefig("./3d_k_{}.png".format(k))
        if is_plotar:
            plt.show()
        fig1.clf()
        plt.close('all')

    return kmeans


# Método para descobrir o melhor k
def k_means_e_metodo_do_cotovelo(nome_arq_saida_todos_momentos, k_array, metodos_do_cotovelo,
                                 is_plotar=True, is_plotar_momentos_3d=False):
    df_momentos_familias = pd.read_csv(nome_arq_saida_todos_momentos, sep=",")
    df_momentos_familias = df_momentos_familias.apply(pd.to_numeric, errors='coerce')
    df_momentos_familias = df_momentos_familias.dropna()
    df_momentos_familias = df_momentos_familias.reset_index(drop=True)
    np_elem_norm = df_momentos_familias.to_numpy()

    # método distorcao_km_inertia - soma das distâncias ao quadrado
    soma_das_dist_ao_quadrado = []
    arr_kmeans = []
    for cada_k in k_array:
        k_means_model = analisador_k_means(df_momentos_familias, np_elem_norm, cada_k, is_plotar, is_plotar_momentos_3d)
        arr_kmeans.append(k_means_model)
        soma_das_dist_ao_quadrado.append(k_means_model.inertia_)
        if "silhueta_yellowbrick" in metodos_do_cotovelo:
            visualizer = SilhouetteVisualizer(k_means_model, colors='yellowbrick')
            visualizer.fit(np_elem_norm)  # Fit the data to the visualizer
            visualizer.fig.savefig("./silhueta_yellowbrick__k_{}.png".format(cada_k))
            if is_plotar:
                visualizer.show()
            plt.close('all')

    for metodo_do_cotovelo in metodos_do_cotovelo:
        if metodo_do_cotovelo == "distorcao_km_inertia":
            plt.plot(k_array, soma_das_dist_ao_quadrado, 'bx-')
            plt.xlabel('k')
            plt.ylabel('Distorção')
            plt.title('Método do cotovelo para encontrar o melhor k')
            plt.savefig("./{}.png".format(metodo_do_cotovelo))
            if is_plotar:
                plt.show()
        elif metodo_do_cotovelo == "distorcao_yellowbrick":
            kmeans = KMeans(random_state=0)
            visualizer = KElbowVisualizer(kmeans, k=k_array, metric='distortion')
            visualizer.fit(np_elem_norm)  # Fit the data to the visualizer
            plt.savefig("./{}.png".format(metodo_do_cotovelo))
            melhor_k = visualizer.elbow_value_
            if is_plotar:
                visualizer.show()
        elif metodo_do_cotovelo == "calinski_harabasz_yellowbrick":
            kmeans = KMeans(random_state=0)
            visualizer = KElbowVisualizer(kmeans, k=k_array, metric='calinski_harabasz')
            visualizer.fit(np_elem_norm)  # Fit the data to the visualizer
            plt.savefig("./{}.png".format(metodo_do_cotovelo))
            if is_plotar:
                visualizer.show()
        plt.close('all')

    return arr_kmeans, melhor_k
