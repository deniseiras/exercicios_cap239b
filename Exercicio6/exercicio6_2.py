# Matemática Computacional I - parte B - Exercício 6.2
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1o período 2020
# Autores: Denis Eiras e Cristiano Reis
# 18/05/2020 - V1.0
#
#
# Entradas
#
# Parâmetros gerais de entrada
# is_plotar_kmeans_cotovelo: (Boolean) True para plotar o kmeans na tela
#
# espacos ESPB e EDF ~~~~~~~
# nome_arquivo_espaco_param_ESPB: (String) Nome do arquivo de espaços de parâmetros ESPB gerados no exercicio6_1.py
# nome_arquivo_espaco_param_EDF: (String) Nome do arquivo de espaços de parâmetros EDF gerados no exercicio6_1.py
#
# # covid 19 ~~~~~~~~~~~~~~~~~
# is_atualizar_arquivo_covid: (Boolean) True para baixar o arquivo da covid com dados atuais
# url_owid_covid_data: (String) Url dos dados de covid (Ex. 'https://covid.ourworldindata.org/data/owid-covid-data.csv')
# nome_arq_covid_completo: (String) Nome arquivo da covid a ser baixado da url do parâmetro url_owid_covid_data
# country_iso_code: (String) Iso_code do país a analisar (Ex. 'USA')
# nome_arquivo_estatisticas_covid_ndc_espb: (String) Nome do arquivo de estatísticas da série no espaco ESPB, a gerar
# nome_arquivo_estatisticas_covid_ndc_edf: (String) Nome do arquivo de estatísticas da série no espaco EDF, a gerar
#
# # sol  ~~~~~~~~~~~~~~~~~~~~~
# nome_arquivo_sol = './sol3ghz.dat'
# nome_arquivo_estatisticas_sol_espb: (String) Nome do arquivo de estatísticas da série no espaco ESPB, a gerar
# nome_arquivo_estatisticas_sol_edf: (String) Nome do arquivo de estatísticas da série no espaco EDF, a gerar
#
# # surf_temp  ~~~~~~~~~~~~~~~
# nome_arquivo_surf_temp = './surftemp504.txt'
# nome_arquivo_estatisticas_surf_temp_espb: (String) Nome do arquivo de estatísticas da série no espaco ESPB, a gerar
# nome_arquivo_estatisticas_surf_temp_edf: (String) Nome do arquivo de estatísticas da série no espaco EDF, a gerar
#
# Saidas
#
# Arquivos de saídas contendo as estatísticas dentro dos espaços de parâmetros, de nomes definidos nas variáveis
# nome_arquivo_estatisticas_<serie>_<espaco>, onde série é o nome da série e <espaco> é o espaço de parâmetros, ESPB ou
# # EDF.
# Arquivo de nome "<serie>_<espaco>_k_2.png", contendo o agrupamento K-means da serie no espaço de parâmetros, ESPB ou
# EDF.

import shutil

import pandas as pd

from Exercicio1.exercicio1_3 import k_means_e_metodo_do_cotovelo
from Exercicio4.exercicio4_2_2 import ler_serie_generica_de_arquivo_ou_url
from Exercicio6.exercicio6_1 import calcula_df_estatistico


def serie_no_espaco_param(label_serie, df_serie, label_espaco_param, df_espaco_param, nome_arquivo_estatisticas_espaco_param):
    # parâmetros fixos
    metodos_do_cotovelo = []  # N/A, apenas k = 2
    k_array = [2]             # Tentativa de separar df_serie de df_espaco_param

    if label_espaco_param == 'espb':
        coluna_espaco_param = 'beta'
    else:
        coluna_espaco_param = 'alfa'
    df_serie_espaco_param = pd.concat([df_serie[['variancia_ao_quadrado', 'curtose', coluna_espaco_param]], df_espaco_param])
    df_serie_espaco_param.to_csv(nome_arquivo_estatisticas_espaco_param, index=False)
    k_means_e_metodo_do_cotovelo(nome_arquivo_estatisticas_espaco_param, k_array, metodos_do_cotovelo, is_plotar=False)
    shutil.move('./k_2.png', './{}_{}_k_2.png'.format(label_serie, label_espaco_param))


# início do programa principal
if __name__ == '__main__':

    # Parâmetros de entrada ==========================================
    # Parâmetros gerais de entrada
    is_plotar_kmeans_cotovelo = True

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
    nome_arquivo_estatisticas_covid_ndc_espb = './estatisticas_covid_ndc_espb.csv'
    nome_arquivo_estatisticas_covid_ndc_edf = './estatisticas_covid_ndc_edf.csv'

    # sol  ~~~~~~~~~~~~~~~~~~~~~
    nome_arquivo_sol = './sol3ghz.dat'
    nome_arquivo_estatisticas_sol_espb = './estatisticas_sol_espb.csv'
    nome_arquivo_estatisticas_sol_edf = './estatisticas_sol_edf.csv'

    # surf_temp  ~~~~~~~~~~~~~~~
    nome_arquivo_surf_temp = './surftemp504.txt'
    nome_arquivo_estatisticas_surf_temp_espb = './estatisticas_surf_temp_espb.csv'
    nome_arquivo_estatisticas_surf_temp_edf = './estatisticas_surf_temp_edf.csv'
    # ================================================================

    # lendo serie espaco espb e edf, gerados no exercício 6.1
    df_espaco_param_ESPB = ler_serie_generica_de_arquivo_ou_url(nome_arquivo_espaco_param_ESPB,
                                                                is_obter_csv_como_dataframe=True)
    df_espaco_param_EDF = ler_serie_generica_de_arquivo_ou_url(nome_arquivo_espaco_param_EDF,
                                                               is_obter_csv_como_dataframe=True)

    # serie covid_ndc =================================================================================================
    label_serie = 'covid_ndc'
    if is_atualizar_arquivo_covid:
        df_covid_completo = ler_serie_generica_de_arquivo_ou_url(url_owid_covid_data, is_obter_csv_como_dataframe=True,
                                                                 is_url=True)
    else:
        df_covid_completo = ler_serie_generica_de_arquivo_ou_url(nome_arq_covid_completo,
                                                                 is_obter_csv_como_dataframe=True)

    df_covid_ndc_eua = df_covid_completo[['iso_code', 'date', 'total_cases']]

    is_df_covid_eua = (df_covid_ndc_eua['iso_code'] == country_iso_code)
    df_covid_eua = df_covid_ndc_eua[is_df_covid_eua]
    arr_covid_ndc_eua = df_covid_eua['total_cases'].values
    df_covid_ndc_eua = calcula_df_estatistico(pd.Series(arr_covid_ndc_eua))
    print("Estatísticas da serie {}: ".format(label_serie), df_covid_ndc_eua)
    serie_no_espaco_param(label_serie, df_covid_ndc_eua, 'espb', df_espaco_param_ESPB, nome_arquivo_estatisticas_covid_ndc_espb)
    serie_no_espaco_param(label_serie, df_covid_ndc_eua, 'edf', df_espaco_param_EDF, nome_arquivo_estatisticas_covid_ndc_edf)

    # serie sol  ======================================================================================================
    label_serie = 'sol'
    arr_sol = ler_serie_generica_de_arquivo_ou_url(nome_arquivo_sol)
    df_sol = calcula_df_estatistico(pd.Series(arr_sol))
    print("Estatísticas da serie {}: ".format(label_serie), df_sol)
    serie_no_espaco_param(label_serie, df_sol, 'espb', df_espaco_param_ESPB, nome_arquivo_estatisticas_sol_espb)
    serie_no_espaco_param(label_serie, df_sol, 'edf', df_espaco_param_EDF, nome_arquivo_estatisticas_sol_edf)

    # serie surf_temp  ================================================================================================
    label_serie = 'surf_temp'
    arr_surf_temp = ler_serie_generica_de_arquivo_ou_url(nome_arquivo_surf_temp)
    df_surf_temp = calcula_df_estatistico(pd.Series(arr_surf_temp))
    print("Estatísticas da serie {}: ".format(label_serie), df_surf_temp)
    serie_no_espaco_param(label_serie, df_surf_temp, 'espb', df_espaco_param_ESPB, nome_arquivo_estatisticas_surf_temp_espb)
    serie_no_espaco_param(label_serie, df_surf_temp, 'edf', df_espaco_param_EDF, nome_arquivo_estatisticas_surf_temp_edf)
