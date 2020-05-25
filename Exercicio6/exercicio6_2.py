# Matemática Computacional I - parte B - Exercício 6.2
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1o período 2020
# Autores: Denis Eiras e Cristiano Reis
# 18/05/2020 - V1.0
#
# ... TODO rever toda descrição, parâmetros ....
#

from exercicio4_2_2 import ler_serie_generica_de_arquivo_ou_url
from exercicio1_3 import k_means_e_metodo_do_cotovelo
from exercicio6_1 import calcula_df_estatistico
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt



# def plot_histograma(df_serie_1, df_serie_2, str_titulo_histograma, str_label_serie_1, str_label_serie_2):
#     histogram_1, bins_edge_1 = np.histogram(df_serie_1, bins=20)
#     histogram_2, bins_edge_2 = np.histogram(df_serie_2, bins=20)
#
#     width = 0.7 * (bins_edge_1[1] - bins_edge_1[0])
#     center = (bins_edge_1[:-1] + bins_edge_2[1:]) / 2
#
#     # plot histograma serie 1
#     fig, ax1 = plt.subplots()
#     color = 'tab:blue'
#     plt.bar(center, histogram_1, align='center', width=width, color=color, lw=5, alpha=0.6, label=str_label_serie_1)
#     ax1.tick_params(axis='y', labelcolor=color)
#
#     # plot histograma serie 2
#     ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
#     color = 'tab:red'
#     plt.bar(center, histogram_2, align='center', width=width, color=color, lw=5, alpha=0.6, label=str_label_serie_2)
#     ax2.get_yaxis().set_ticks([])
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.title('Histograma de {}'.format(str_titulo_histograma))
#     plt.xlabel("bin")
#     plt.ylabel("Quantidade")
#     plt.show()



# início do programa principal
if __name__ == '__main__':

    # Parâmetros de entrada ==========================================
    # Parâmetros gerais de entrada
    metodos_do_cotovelo = ['distorcao_yellowbrick', 'silhueta_yellowbrick']
    is_plotar_kmeans_cotovelo = True
    k_array = range(2)

    # espacos ESPB e EDF ~~~~~~~
    nome_arquivo_espaco_param_ESPB = './exec1/espaco_param_ESPB.csv'
    nome_arquivo_espaco_param_EDF = './exec1/espaco_param_EDF.csv'

    # covid 19 ~~~~~~~~~~~~~~~~~
    is_atualizar_arquivo_covid = True
    url_owid_covid_data = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
    # nome arquivo covid a salvar
    nome_arq_covid_completo = './owid-covid-data.csv'
    # país a analisar
    country_iso_code = 'USA'

    # sol  ~~~~~~~~~~~~~~~~~~~~~
    nome_arquivo_sol = './sol3ghz.dat'
    nome_arquivo_estatisticas_sol_espb = './estatisticas_sol_espb.csv'
    nome_arquivo_estatisticas_sol_edf = './estatisticas_sol_edf.csv'

    # surf_temp  ~~~~~~~~~~~~~~~
    nome_arquivo_surf_temp = './surftemp504.txt'
    # ================================================================

    # lendo serie espaco espb e edf, gerados no exercício 6.1
    df_espaco_param_ESPB = ler_serie_generica_de_arquivo_ou_url(nome_arquivo_espaco_param_ESPB, is_obter_csv_como_dataframe=True)
    df_espaco_param_EDF = ler_serie_generica_de_arquivo_ou_url(nome_arquivo_espaco_param_EDF, is_obter_csv_como_dataframe=True)

    # lendo serie sol e gerando espacos estatísticos
    arr_sol = ler_serie_generica_de_arquivo_ou_url(nome_arquivo_sol)
    df_sol = calcula_df_estatistico(pd.Series(arr_sol))
    print("Estatísticas da serie Sol: ", df_sol)

    # serie sol no espaço de parâmetros ESB
    df_sol_espb = pd.concat([df_sol[['variancia_ao_quadrado', 'curtose', 'beta']], df_espaco_param_ESPB])
    df_sol_espb.to_csv(nome_arquivo_estatisticas_sol_espb, index=False  )
    k_means_e_metodo_do_cotovelo(nome_arquivo_estatisticas_sol_espb, k_array, metodos_do_cotovelo, is_plotar_kmeans_cotovelo, is_plotar_momentos_3d=False)

    # serie sol no espaço de parâmetros EDF
    df_sol_edf = pd.concat([df_sol[['variancia_ao_quadrado', 'curtose', 'alfa']], df_espaco_param_EDF])
    df_sol_edf.to_csv(nome_arquivo_estatisticas_sol_edf, index=False)
    k_means_e_metodo_do_cotovelo(nome_arquivo_estatisticas_sol_edf, k_array, metodos_do_cotovelo,
                                 is_plotar_kmeans_cotovelo, is_plotar_momentos_3d=False)

    # df_estatisticas_sol = calcula_df_estatistico(df_sinais_noise, nome_arq_tabela_estatística)

    # serie surf_temp
    arr_surf_temp = ler_serie_generica_de_arquivo_ou_url(nome_arquivo_surf_temp)

    # serie covid NDC
    if is_atualizar_arquivo_covid:
        df_covid_completo = ler_serie_generica_de_arquivo_ou_url(url_owid_covid_data, is_obter_csv_como_dataframe=True, is_url=True)
    else:
        df_covid_completo = ler_serie_generica_de_arquivo_ou_url(nome_arq_covid_completo, is_obter_csv_como_dataframe=True)

    df_covid_ndc = df_covid_completo[['iso_code', 'date', 'total_cases']]

    is_df_covid_eua = (df_covid_ndc['iso_code'] == country_iso_code)
    df_covid_ndc_eua = df_covid_ndc[is_df_covid_eua]
    arr_covid_ndc_eua = df_covid_ndc_eua['total_cases'].values
    exit(0)


