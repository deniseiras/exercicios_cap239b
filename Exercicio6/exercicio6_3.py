# Matemática Computacional I - parte B - Exercício 6.3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1o período 2020
# Autores: Denis Eiras
# 18/05/2020 - V1.0
#
# 6.3. Aplique k-means para todas as series ST-OWS_NDC_Covid1 considerando os seguintes
# Espaços de atributos: S 2 x α e K x α. Obtenha os melhores agrupamentos, identifique os grupos
# e discuta os resultados.
#
# Entradas
#

import datetime
import os
import shutil

import numpy as np
import pandas as pd

from Codigos.specplus import dfa1d
from Exercicio1.exercicio1_3 import k_means_e_metodo_do_cotovelo
from Exercicio4.exercicio4_2_2 import ler_serie_generica_de_arquivo_ou_url


def filtra_e_insere_datas_faltantes(dados_, df_covid_pais, valor_coluna_agrupadora):
    df_covid_pais_date = pd.DataFrame()
    df_covid_pais_date[dados_.coluna_data] = pd.to_datetime(df_covid_pais[dados_.coluna_data])

    mascara_data = (df_covid_pais_date[dados_.coluna_data] >= dados_.data_inicial) & (
            df_covid_pais_date[dados_.coluna_data] <= dados_.data_final)
    df_covid_pais_real = df_covid_pais.loc[mascara_data]

    # insere datas faltantes
    dates_list = pd.date_range(start=dados_.data_inicial, end=dados_.data_final)
    df_dates = pd.DataFrame(dates_list, columns=["date"])
    df_dates[dados_.coluna_agrupadora_covid] = valor_coluna_agrupadora
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


def corrigir_valores_estatisticos_invalidos(df_todas_series):
    df_todas_series.replace('', np.nan, inplace=True)
    df_todas_series.replace(np.inf, np.nan, inplace=True)
    df_todas_series.replace(-np.inf, np.nan, inplace=True)
    df_todas_series.dropna(inplace=True)


def normalizar_valor(df, coluna):
    df[coluna] = (df[coluna] - df[coluna].min()) / (df[coluna].max() - df[coluna].min())
    return df


def calcula_df_estatistico(df_covid, cfg_covid):
    df_stats = pd.DataFrame()
    for grupo in df_covid[cfg_covid.coluna_agrupadora_covid].unique():
        if str(grupo) == 'nan' or grupo in cfg_covid.grupos_a_rejeitar:
            continue
        is_df_covid_grupo = (df_covid[cfg_covid.coluna_agrupadora_covid] == grupo)
        df_covid_grupo = df_covid[is_df_covid_grupo]
        df_covid_grupo = filtra_e_insere_datas_faltantes(cfg_covid, df_covid_grupo, grupo)

        serie = df_covid_grupo[cfg_covid.coluna_serie_covid]
        df_serie = pd.DataFrame()
        df_serie[cfg_covid.coluna_agrupadora_covid] = pd.Series(str(grupo))
        df_serie['assimetria_ao_quadrado'] = serie.skew() ** 2
        df_serie['curtose'] = serie.kurtosis()
        alfa, vetoutput, x, y, reta, erro = dfa1d(serie, 1)
        df_serie['alfa'] = alfa
        df_stats = pd.concat([df_stats, df_serie])

    corrigir_valores_estatisticos_invalidos(df_stats)
    # df_stats = normalizar_valor(df_stats, 'assimetria_ao_quadrado')
    # df_stats = normalizar_valor(df_stats, 'curtose')

    return df_stats


def serie_no_espaco_param(df_estatistico_completo, cfg_covid, label_espaco_param, arr_momentos_estat, k_array, metodos_do_cotovelo,
                          is_plotar_kmeans):
    nome_arq_momentos_estat = './momentos_estatisticos.csv'
    df_estatistico_completo.to_csv(nome_arq_momentos_estat, index=False)

    df_estatistico = df_estatistico_completo[arr_momentos_estat]
    nome_arq_momentos_estat_dummy = './momentos_estat_dummy.csv'
    df_estatistico.to_csv(nome_arq_momentos_estat_dummy, index=False)
    arr_kmeans, melhor_k = k_means_e_metodo_do_cotovelo(nome_arq_momentos_estat_dummy, k_array, metodos_do_cotovelo,
                                                        is_plotar_kmeans)
    for k in k_array:
        shutil.move('./k_{}.png'.format(k), './{}_k_{}.png'.format(label_espaco_param, k))
        shutil.move('./silhueta_yellowbrick__k_{}.png'.format(k),
                    './silhueta_yellowbrick__{}_k_{}.png'.format(label_espaco_param, k))
    shutil.move('./distorcao_yellowbrick.png', './distorcao_yellowbrick__{}.png'.format(label_espaco_param))
    os.remove(nome_arq_momentos_estat_dummy)
    print('Melhor k = {}'.format(melhor_k))

    # imprime os agrupamentos de cada país
    print('Pais\tespaco\tcluster')
    for grupo in df_estatistico_completo[cfg_covid.coluna_agrupadora_covid].unique():
        is_df_covid_grupo = (df_estatistico_completo[cfg_covid.coluna_agrupadora_covid] == grupo)
        df_covid_grupo = df_estatistico_completo[is_df_covid_grupo]
        df_covid_grupo = df_covid_grupo[arr_momentos_estat]
        classe = arr_kmeans[melhor_k - 2].predict(df_covid_grupo.to_numpy())[0]
        print('{}\t{}\t{}'.format(grupo, label_espaco_param, classe))


class DadosConfigCovid:

    def __init__(self, data_ini, data_fim):
        self.data_inicial = data_ini
        self.data_final = data_fim
        self.coluna_agrupadora_covid = 'location'
        self.grupos_a_rejeitar = ['International', 'World']
        self.coluna_serie_covid = 'new_cases'
        self.coluna_data = 'date'
        self.is_atualizar_arquivo_covid = False
        self.url_owid_covid_data = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
        # nome arquivo covid a salvar
        self.nome_arq_covid_completo = './owid-covid-data.csv'


# início do programa principal
if __name__ == '__main__':

    # Parâmetros de entrada ===========================================================================================
    k_array = range(2, 21)
    metodos_do_cotovelo = ['distorcao_yellowbrick', 'silhueta_yellowbrick']
    is_plotar_kmeans = False

    config_covid = DadosConfigCovid('2020-03-10', '2020-05-28')
    # =================================================================================================================

    if config_covid.is_atualizar_arquivo_covid:
        df_covid_completo = ler_serie_generica_de_arquivo_ou_url(config_covid.url_owid_covid_data,
                                                                 is_obter_csv_como_dataframe=True,
                                                                 is_url=True)
    else:
        df_covid_completo = ler_serie_generica_de_arquivo_ou_url(config_covid.nome_arq_covid_completo,
                                                                 is_obter_csv_como_dataframe=True)
    df_valores_por_agrupador = df_covid_completo[
        [config_covid.coluna_agrupadora_covid, config_covid.coluna_serie_covid, config_covid.coluna_data]]

    df_estatistico_completo = calcula_df_estatistico(df_valores_por_agrupador, config_covid)
    arr_momentos_estat = ['assimetria_ao_quadrado', 'alfa']
    label_espaco_param = 's2_alfa'
    serie_no_espaco_param(df_estatistico_completo, config_covid, label_espaco_param, arr_momentos_estat, k_array,
                          metodos_do_cotovelo, is_plotar_kmeans)
    arr_momentos_estat = ['curtose', 'alfa']
    label_espaco_param = 'curtose_alfa'
    serie_no_espaco_param(df_estatistico_completo, config_covid, label_espaco_param, arr_momentos_estat, k_array,
                          metodos_do_cotovelo, is_plotar_kmeans)
