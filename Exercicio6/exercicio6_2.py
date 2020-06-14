# Matemática Computacional I - parte B - Exercício 6.2
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1o período 2020
# Autores: Denis Eiras
# 18/05/2020 - V1.0
#
#
# Descrição
#
# 6.2. Classifique, nos espaços de parâmetros do exercício anterior, as séries temporais: (a) ST-Sol3GHz, (b)
# ST-surftemp504 e (c) ST-OWS_NDC_
#
#
# Entradas
#
# Parâmetros gerais de entrada
# - is_plotar_kmeans: (Boolean) True para plotar o kmeans na tela
#
# espacos ESPB e EDF ~~~~~~~~~
# - nome_arquivo_espaco_param_ESPB: (String) Nome do arquivo de espaços de parâmetros ESPB gerados no exercicio6_1.py
# - nome_arquivo_espaco_param_EDF: (String) Nome do arquivo de espaços de parâmetros EDF gerados no exercicio6_1.py
#
# # covid 19 ~~~~~~~~~~~~~~~~~
# - is_atualizar_arquivo_covid: (Boolean) True para baixar o arquivo da covid com dados atuais
# - url_owid_covid_data: (String) Url dos dados de covid (Ex. 'https://covid.ourworldindata.org/data/owid-covid-data.csv')
# - nome_arq_covid_completo: (String) Nome arquivo da covid a ser baixado da url do parâmetro url_owid_covid_data
# - country_iso_code: (String) Iso_code do país a analisar (Ex. 'USA')
# - nome_arquivo_estatisticas_covid_ndc_espb: (String) Nome do arquivo de estatísticas da série no espaco ESPB, a gerar
# - nome_arquivo_estatisticas_covid_ndc_edf: (String) Nome do arquivo de estatísticas da série no espaco EDF, a gerar
#
# # sol  ~~~~~~~~~~~~~~~~~~~~~
# - nome_arquivo_sol = './sol3ghz.dat'
# - nome_arquivo_estatisticas_sol_espb: (String) Nome do arquivo de estatísticas da série no espaco ESPB, a gerar
# - nome_arquivo_estatisticas_sol_edf: (String) Nome do arquivo de estatísticas da série no espaco EDF, a gerar
#
# # surf_temp  ~~~~~~~~~~~~~~~
# - nome_arquivo_surf_temp = './surftemp504.txt'
# - nome_arquivo_estatisticas_surf_temp_espb: (String) Nome do arquivo de estatísticas da série no espaco ESPB, a gerar
# - nome_arquivo_estatisticas_surf_temp_edf: (String) Nome do arquivo de estatísticas da série no espaco EDF, a gerar
#
#
# Saídas
#
# - Arquivos de saídas contendo as estatísticas dentro dos espaços de parâmetros, de nomes definidos nas variáveis
#   nome_arquivo_estatisticas_<serie>_<espaco>, onde série é o nome da série e <espaco> é o espaço de parâmetros, ESPB
#   ou EDF.
# - Arquivo de nome "<serie>_<espaco>_k_2.png", contendo o agrupamento K-means da serie no espaço de parâmetros, ESPB ou
#   EDF.

import datetime
import shutil

import pandas as pd

from Exercicio1.exercicio1_3 import k_means_e_metodo_do_cotovelo
from Exercicio4.exercicio4_2_2 import ler_serie_generica_de_arquivo_ou_url
from Exercicio6.exercicio6_1 import calcula_df_estatistico


def serie_no_espaco_param(label_serie, df_serie, label_espaco_param, df_espaco_param,
                          nome_arquivo_estatisticas_espaco_param, is_plotar_kmeans, k_array, metodos_do_cotovelo):
    if label_espaco_param == 'espb':
        coluna_espaco_param = 'beta'
    else:
        coluna_espaco_param = 'alfa'

    # para comparar com o espaço gerado com a série incluída ...
    nome_arq_dummy = 'dummy_tmp.csv'
    df_espaco_param[['assimetria_ao_quadrado', 'curtose', coluna_espaco_param]].to_csv(nome_arq_dummy, index=False)
    arr_kmeans = k_means_e_metodo_do_cotovelo(nome_arq_dummy, k_array, metodos_do_cotovelo, is_plotar_kmeans)
    for k in k_array:
        try:
            shutil.move('./k_{}.png'.format(k), './k_{}_{}.png'.format(k, label_serie))
        except FileNotFoundError:
            pass
    shutil.move('./distorcao_yellowbrick.png', './distorcao_yellowbrick_{}.png'.format(label_serie))

    # ... (com a série inclída)
    df_serie_espaco_param = pd.concat(
        [df_serie[['assimetria_ao_quadrado', 'curtose', coluna_espaco_param]], df_espaco_param])
    df_serie_espaco_param.to_csv(nome_arquivo_estatisticas_espaco_param, index=False)

    arr_kmeans, melhor_k = k_means_e_metodo_do_cotovelo(nome_arquivo_estatisticas_espaco_param, k_array, metodos_do_cotovelo,
                                              is_plotar_kmeans)
    for k in k_array:
        try:
            shutil.move('./k_{}.png'.format(k), './k_{}_{}_{}.png'.format(k, label_espaco_param, label_serie))
        except FileNotFoundError:
            pass
    shutil.move('./distorcao_yellowbrick.png',
                './distorcao_yellowbrick_{}_{}.png'.format(label_espaco_param, label_serie))

    print('Clusters serie {}, espaco {}'.format(label_serie, label_espaco_param), arr_kmeans[melhor_k - 2].predict(
        df_serie[['assimetria_ao_quadrado', 'curtose', coluna_espaco_param]].to_numpy()))
    return arr_kmeans


def filtra_e_insere_datas_faltantes(dados_, df_covid_pais):
    df_covid_pais_date = pd.DataFrame()
    df_covid_pais_date[dados_.coluna_data] = pd.to_datetime(df_covid_pais[dados_.coluna_data])

    mascara_data = (df_covid_pais_date[dados_.coluna_data] >= dados_.data_inicial) & (
            df_covid_pais_date[dados_.coluna_data] <= dados_.data_final)
    df_covid_pais_real = df_covid_pais.loc[mascara_data]

    # insere datas faltantes
    dates_list = pd.date_range(start=dados_.data_inicial, end=dados_.data_final)
    df_dates = pd.DataFrame(dates_list, columns=["date"])
    df_dates[dados_.coluna_agrupadora_covid] = dados_.valor_coluna_agrupador
    df_dates[dados_.coluna_serie_covid] = 0
    df_covid_pais_real = df_covid_pais_real.dropna()
    for index_c, row_c in df_covid_pais_real.iterrows():
        for index, row in df_dates.iterrows():
            date_time_str = row_c[dados_.coluna_data]
            date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
            if row[dados_.coluna_data] < date_time_obj:
                continue
            elif date_time_obj == row[dados_.coluna_data]:
                df_dates.at[index, dados_.coluna_agrupadora_covid] = row_c[dados_.coluna_agrupadora_covid]
                df_dates.at[index, dados_.coluna_serie_covid] = row_c[dados_.coluna_serie_covid]
                break
    df_covid_pais_real = df_dates
    return df_covid_pais_real


def get_dados_covid_por_agrupador(dados_):
    # obtém dados da covid e atualiza se especificado
    if dados_.is_atualizar_arquivo_covid:
        df_covid_completo = ler_serie_generica_de_arquivo_ou_url(dados_.url_owid_covid_data,
                                                                 is_obter_csv_como_dataframe=True,
                                                                 is_url=True)
    else:
        df_covid_completo = ler_serie_generica_de_arquivo_ou_url(dados_.nome_arq_covid_completo,
                                                                 is_obter_csv_como_dataframe=True)
    # seleciona por agrupador (Ex. location)
    df_covid_completo = df_covid_completo[
        [dados_.coluna_agrupadora_covid, dados_.coluna_data, dados_.coluna_serie_covid]]
    is_pais = df_covid_completo[dados_.coluna_agrupadora_covid] == dados_.valor_coluna_agrupador
    df_covid_pais = df_covid_completo[is_pais]

    df_covid_pais_real = filtra_e_insere_datas_faltantes(dados_, df_covid_pais)
    return df_covid_pais_real


def normalizar_estat_no_espaco(df_serie, df_espaco):
    for col in ['curtose', 'assimetria_ao_quadrado']:
        df_serie[col] = (df_serie[col] - df_espaco[col].min()) / (df_espaco[col].max() - df_espaco[col].min())
    return df_serie


class DadosConfigCovid:

    def __init__(self, valor_col_agrup, data_ini, data_fim):
        self.valor_coluna_agrupador = valor_col_agrup
        self.data_inicial = data_ini
        self.data_final = data_fim
        self.coluna_agrupadora_covid = 'iso_code'
        self.coluna_serie_covid = 'new_cases'
        self.coluna_data = 'date'
        self.is_atualizar_arquivo_covid = True
        self.url_owid_covid_data = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
        # nome arquivo covid a salvar
        self.nome_arq_covid_completo = './owid-covid-data.csv'


# início do programa principal
if __name__ == '__main__':
    # Parâmetros de entrada ===========================================================================================
    # Parâmetros gerais de entrada
    is_plotar_kmeans = False
    k_array = range(2, 15)
    metodos_do_cotovelo = ['distorcao_yellowbrick']
    nome_arquivo_todos_sinais = './files_6_1_sem_noise/todos_sinais.csv'

    # espacos ESPB e EDF gerados no Ex. 6.1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    nome_arquivo_espaco_param_ESPB = './files_6_1/espaco_param_ESPB.csv'
    nome_arquivo_espaco_param_EDF = './files_6_1/espaco_param_EDF.csv'

    # covid 19 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    dados_covid = DadosConfigCovid('USA', '2020-03-10', '2020-05-28')
    nome_arquivo_estatisticas_covid_ndc_espb = './estatisticas_covid_ndc_espb.csv'
    nome_arquivo_estatisticas_covid_ndc_edf = './estatisticas_covid_ndc_edf.csv'

    # sol  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    nome_arquivo_sol = './sol3ghz.dat'
    nome_arquivo_estatisticas_sol_espb = './estatisticas_sol_espb.csv'
    nome_arquivo_estatisticas_sol_edf = './estatisticas_sol_edf.csv'

    # surf_temp  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    nome_arquivo_surf_temp = './surftemp504.txt'
    nome_arquivo_estatisticas_surf_temp_espb = './estatisticas_surf_temp_espb.csv'
    nome_arquivo_estatisticas_surf_temp_edf = './estatisticas_surf_temp_edf.csv'
    # =================================================================================================================

    # lendo serie espaco espb e edf, gerados no exercício 6.1
    df_espaco_param_ESPB = ler_serie_generica_de_arquivo_ou_url(nome_arquivo_espaco_param_ESPB,
                                                                is_obter_csv_como_dataframe=True)
    df_espaco_param_EDF = ler_serie_generica_de_arquivo_ou_url(nome_arquivo_espaco_param_EDF,
                                                               is_obter_csv_como_dataframe=True)

    # serie covid_ndc =================================================================================================
    label_serie = 'covid_ndc'
    df_covid_eua = get_dados_covid_por_agrupador(dados_covid)
    arr_covid_ndc_eua = df_covid_eua[dados_covid.coluna_serie_covid].values
    df_covid_ndc_eua = calcula_df_estatistico(pd.Series(arr_covid_ndc_eua))
    df_covid_ndc_eua = normalizar_estat_no_espaco(df_covid_ndc_eua, df_espaco_param_ESPB)

    print("Estatísticas da serie {}: ".format(label_serie), df_covid_ndc_eua)
    arr_kmeans = serie_no_espaco_param(label_serie, df_covid_ndc_eua, 'espb', df_espaco_param_ESPB,
                                       nome_arquivo_estatisticas_covid_ndc_espb, is_plotar_kmeans, k_array,
                                       metodos_do_cotovelo)
    serie_no_espaco_param(label_serie, df_covid_ndc_eua, 'edf', df_espaco_param_EDF,
                          nome_arquivo_estatisticas_covid_ndc_edf, is_plotar_kmeans, k_array, metodos_do_cotovelo)

    # serie sol  ======================================================================================================
    label_serie = 'sol'
    arr_sol = ler_serie_generica_de_arquivo_ou_url(nome_arquivo_sol)
    df_sol = calcula_df_estatistico(pd.Series(arr_sol))
    df_sol = normalizar_estat_no_espaco(df_sol, df_espaco_param_ESPB)
    print("Estatísticas da serie {}: ".format(label_serie), df_sol)
    serie_no_espaco_param(label_serie, df_sol, 'espb', df_espaco_param_ESPB, nome_arquivo_estatisticas_sol_espb,
                          is_plotar_kmeans, k_array, metodos_do_cotovelo)
    serie_no_espaco_param(label_serie, df_sol, 'edf', df_espaco_param_EDF, nome_arquivo_estatisticas_sol_edf,
                          is_plotar_kmeans, k_array, metodos_do_cotovelo)

    # serie surf_temp  ================================================================================================
    label_serie = 'surf_temp'
    arr_surf_temp = ler_serie_generica_de_arquivo_ou_url(nome_arquivo_surf_temp)
    df_surf_temp = calcula_df_estatistico(pd.Series(arr_surf_temp))
    df_surf_temp = normalizar_estat_no_espaco(df_surf_temp, df_espaco_param_ESPB)
    print("Estatísticas da serie {}: ".format(label_serie), df_surf_temp)
    serie_no_espaco_param(label_serie, df_surf_temp, 'espb', df_espaco_param_ESPB,
                          nome_arquivo_estatisticas_surf_temp_espb, is_plotar_kmeans, k_array, metodos_do_cotovelo)
    serie_no_espaco_param(label_serie, df_surf_temp, 'edf', df_espaco_param_EDF,
                          nome_arquivo_estatisticas_surf_temp_edf, is_plotar_kmeans, k_array, metodos_do_cotovelo)
