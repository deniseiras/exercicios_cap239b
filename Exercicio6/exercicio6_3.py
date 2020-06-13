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

import os
import shutil

import pandas as pd

from Exercicio1.exercicio1_3 import k_means_e_metodo_do_cotovelo
from Exercicio4.exercicio4_2_2 import ler_serie_generica_de_arquivo_ou_url
from Codigos.Specplus import dfa1d


def calcula_df_estatistico(df_covid, coluna_agrupadora_covid, grupos_a_rejeitar, coluna_serie_covid):
    df_todas_series = pd.DataFrame()
    for grupo in df_covid[coluna_agrupadora_covid].unique():
        if str(grupo) == 'nan' or grupo in grupos_a_rejeitar:
            continue
        is_df_covid_grupo = (df_covid[coluna_agrupadora_covid] == grupo)
        df_covid_grupo = df_covid[is_df_covid_grupo]
        serie = df_covid_grupo[coluna_serie_covid]
        df_serie = pd.DataFrame()
        df_serie[coluna_agrupadora_covid] = pd.Series(str(grupo))
        df_serie['variancia_ao_quadrado'] = serie.var() ** 2
        df_serie['curtose'] = serie.kurtosis()
        alfa, vetoutput, x, y, reta, erro = dfa1d(serie, 1)
        df_serie['alfa'] = alfa

        df_todas_series = pd.concat([df_todas_series, df_serie])

    return df_todas_series


def serie_no_espaco_param(df_covid, coluna_agrupadora_covid, grupos_a_rejeitar, coluna_serie_covid, label_espaco_param,
                          arr_momentos_estat, k_array, metodos_do_cotovelo, is_plotar_kmeans):
    df_estatistico_completo = calcula_df_estatistico(df_covid, coluna_agrupadora_covid, grupos_a_rejeitar,
                                                     coluna_serie_covid)
    nome_arq_momentos_estat = './momentos_estat_{}.csv'.format(label_espaco_param)
    df_estatistico_completo.to_csv(nome_arq_momentos_estat, index=False)

    df_estatistico = df_estatistico_completo[arr_momentos_estat]
    nome_arq_momentos_estat_dummy = './momentos_estat_dummy.csv'
    df_estatistico.to_csv(nome_arq_momentos_estat_dummy, index=False)
    k_means_e_metodo_do_cotovelo(nome_arq_momentos_estat_dummy, k_array, metodos_do_cotovelo, is_plotar_kmeans)
    for k in k_array:
        shutil.move('./k_{}.png'.format(k), './{}_k_{}.png'.format(label_espaco_param, k))
        shutil.move('./silhueta_yellowbrick__k_{}.png'.format(k),
                    './silhueta_yellowbrick__{}_k_{}.png'.format(label_espaco_param, k))
    shutil.move('./distorcao_yellowbrick.png', './distorcao_yellowbrick__{}.png'.format(label_espaco_param))
    os.remove(nome_arq_momentos_estat_dummy)


# início do programa principal
if __name__ == '__main__':



    # TODO DATAS DA COVID
    # Parâmetros de entrada ===========================================================================================
    k_array = range(2, 21)
    metodos_do_cotovelo = ['distorcao_yellowbrick', 'silhueta_yellowbrick']
    is_plotar_kmeans = False

    is_atualizar_arquivo_covid = False
    url_owid_covid_data = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
    # nome arquivo covid a salvar
    nome_arq_covid_completo = './owid-covid-data.csv'
    coluna_agrupadora_covid = 'location'
    coluna_serie_covid = 'new_cases'
    grupos_a_rejeitar = ['International', 'World']
    # =================================================================================================================

    if is_atualizar_arquivo_covid:
        df_covid_completo = ler_serie_generica_de_arquivo_ou_url(url_owid_covid_data, is_obter_csv_como_dataframe=True,
                                                                 is_url=True)
    else:
        df_covid_completo = ler_serie_generica_de_arquivo_ou_url(nome_arq_covid_completo,
                                                                 is_obter_csv_como_dataframe=True)
    df_valores_por_agrupador = df_covid_completo[[coluna_agrupadora_covid, coluna_serie_covid]]

    arr_momentos_estat = ['variancia_ao_quadrado', 'alfa']
    label_espaco_param = 'var2_alfa'
    serie_no_espaco_param(df_valores_por_agrupador, coluna_agrupadora_covid, grupos_a_rejeitar, coluna_serie_covid,
                          label_espaco_param, arr_momentos_estat, k_array, metodos_do_cotovelo,
                          is_plotar_kmeans)
    arr_momentos_estat = ['curtose', 'alfa']
    label_espaco_param = 'curtose_alfa'
    serie_no_espaco_param(df_valores_por_agrupador, coluna_agrupadora_covid, grupos_a_rejeitar, coluna_serie_covid,
                          label_espaco_param, arr_momentos_estat, k_array, metodos_do_cotovelo,
                          is_plotar_kmeans)
