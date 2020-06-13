# Matemática Computacional I - parte B - Exercício 7.1 e 7.2
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1o período 2020
# Autores: Denis Eiras
# 18/05/2020 - V1.0
#
#
# Descrição
#
# Considere o programa mfdfa.py. Aprimore o programa para que o mesmo calcule o índice Ψ = Δα/α max .
#
# Entradas:
#
#
# Saídas:
#

import shutil

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime

from Codigos.mfdfa_ss_m2 import getMSSByUpscaling
from Exercicio1.exercicio1_1 import gerador_de_sinais_aleatorios
from Exercicio1.exercicio1_3 import k_means_e_metodo_do_cotovelo
from Exercicio2.exercicio2 import gerador_de_sinais_colored_noise
from Exercicio3.exercicio3 import gerador_de_sinais_pmodel
from Exercicio4.exercicio4_2_2 import ler_serie_generica_de_arquivo_ou_url
from Exercicio5.exercicio5_1 import gerador_de_sinais_logisticos, gerador_de_sinais_henon


def espectro_de_singularidades_todos(dic_df_sinais, is_plot_sing=False):
    plt.clf()
    fig, ax = plt.subplots()
    colors = plt.rcParams["axes.prop_cycle"]()
    for tipo_sinal, df_sinais in dic_df_sinais.items():
        print('Generating singularity spectrum of {}'.format(tipo_sinal))
        stats = get_stat_mfmda(df_sinais['valor'].tolist())
        c = next(colors)["color"]
        ax.plot(stats['LH'], stats['f'], 'ko-', label=tipo_sinal, color=c)
        print('Espectro de singularidades {}.\nalpha_0 = {:.2f} : Delta_alpha = {:.2f} : psi = {:.2f}'
              ' : A_alpha = {:.2f}'.format(tipo_sinal, stats['alfa_0'], stats['delta_alfa'], stats['psi'],
                                           stats['a_alfa']))

    plt.title('Espectro de singularidades todos os sinais')
    plt.xlabel(r'$\alpha$')
    plt.ylabel(r'$f(\alpha)$')
    plt.grid('on', which='major')
    plt.legend()
    plt.savefig('./espectro_de_singularidades.png')
    if is_plot_sing:
        plt.show()


def get_stat_mfmda(valores):
    [_, _, _, stats, _] = getMSSByUpscaling(valores, isNormalised=0)
    return stats


def espectro_de_singularidades(df_sinais, tipo_sinal, is_plot_sing=False):
    # Obter o espectro de singularidades  f(Alfa) x Alfa e Psi
    print('Generating singularity spectrum of {}'.format(tipo_sinal))
    stats = get_stat_mfmda(df_sinais['valor'].tolist())
    # [_, _, _, stats, _] = getMSSByUpscaling(df_sinais['valor'].tolist(), normType=0, isNormalised=1)
    plt.clf()
    plt.plot(stats['LH'], stats['f'], 'ko-')
    plt.title(
        'Espectro de singularidades {}.\n$\\alpha$0 = {:.2f} : $\\Delta$$\\alpha$ = {:.2f} : $\\psi$ = {:.2f}'
        ' : A$\\alpha$ = {:.2f}'.format(tipo_sinal, stats['alfa_0'], stats['delta_alfa'], stats['a_alfa'],
                                        stats['psi']))
    plt.xlabel(r'$\alpha$')
    plt.savefig('./espectro_de_singularidades_{}.png'.format(tipo_sinal))
    plt.ylabel(r'$f(\alpha)$')
    plt.grid('on', which='major')
    if is_plot_sing:
        plt.show()


def calcula_df_estatistico_por_familia_e_sinal(df_sinais, nome_arq_tabela_estatistica):
    df_stats = None
    for familia in df_sinais.familia.unique():
        for sinal in df_sinais.sinal.unique():
            # elementos pertencentes à família e sinal:
            df_is_elem_da_familia_e_sinal = (df_sinais['familia'] == familia) & (
                    df_sinais['sinal'] == sinal)
            df = df_sinais[df_is_elem_da_familia_e_sinal]
            valores = df.valor
            df = calcula_df_estatistico(valores)
            df_stats = pd.concat([df_stats, df])

    corrigir_valores_estatisticos_invalidos(df_stats)
    df_stats = normalizar_valor(df_stats, 's2')

    df_stats.to_csv(nome_arq_tabela_estatistica, index=False)
    return df_stats


def calcula_df_estatistico(valores):
    df = pd.DataFrame()
    df['s2'] = pd.Series(valores.skew() ** 2)
    stats = get_stat_mfmda(valores.tolist())
    df['psi'] = stats['psi']
    return df


def calcula_df_estatistico_covid(df_covid, coluna_agrupadora_covid, grupos_a_rejeitar, coluna_serie_covid, coluna_data,
                                 data_inicial, data_final):
    df_todas_series = pd.DataFrame()
    for grupo in df_covid[coluna_agrupadora_covid].unique():
        if str(grupo) == 'nan' or grupo in grupos_a_rejeitar:
            continue
        is_df_covid_grupo = (df_covid[coluna_agrupadora_covid] == grupo)
        df_covid_grupo = df_covid[is_df_covid_grupo]

        # filtra datas inicial e final
        df_covid_pais_date = pd.DataFrame()
        df_covid_pais_date[coluna_data] = pd.to_datetime(df_covid_grupo[coluna_data])
        mascara_data = (df_covid_pais_date[coluna_data] >= data_inicial) & (
                df_covid_pais_date[coluna_data] <= data_final)
        df_covid_grupo_na_data = df_covid_grupo.loc[mascara_data]

        # date_time_str = '2018-06-29 08:15:27.243860'
        # insere datas faltantes
        dates_list = pd.date_range(start=data_inicial, end=data_final)
        df_dates = pd.DataFrame(dates_list, columns=["date"])
        df_dates[coluna_agrupadora_covid] = grupo
        df_dates[coluna_serie_covid] = 0
        for index_c, row_c in df_covid_grupo_na_data.iterrows():
            for index, row in df_dates.iterrows():
                date_time_str = row_c[coluna_data]
                date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
                if row[coluna_data] < date_time_obj:
                    continue
                elif date_time_obj == row[coluna_data]:
                    df_dates.at[index, coluna_agrupadora_covid] = row_c[coluna_agrupadora_covid]
                    df_dates.at[index, coluna_serie_covid] = row_c[coluna_serie_covid]
                    break

        # calcula estatisticas
        serie = df_dates[coluna_serie_covid]
        df_stats_grupo = calcula_df_estatistico(serie)
        df_stats_grupo[coluna_agrupadora_covid] = pd.Series(str(grupo))
        df_todas_series = pd.concat([df_todas_series, df_stats_grupo])

    corrigir_valores_estatisticos_invalidos(df_todas_series)
    df_todas_series = normalizar_valor(df_todas_series, 's2')

    return df_todas_series


def corrigir_valores_estatisticos_invalidos(df_todas_series):
    df_todas_series.replace('', np.nan, inplace=True)
    df_todas_series.replace(np.inf, np.nan, inplace=True)
    df_todas_series.replace(-np.inf, np.nan, inplace=True)
    df_todas_series[df_todas_series['psi'] < 0] = np.nan
    df_todas_series.dropna(inplace=True)


def normalizar_valor(df, coluna):
    df[coluna] = (df[coluna] - df[coluna].min()) / (df[coluna].max() - df[coluna].min())
    return df


def serie_no_espaco_param(df_serie, df_espaco_param, nome_arq_esp_param, nome_arquivo_estatisticas_espaco_param,
                          is_plotar_kmeans,
                          metodos_do_cotovelo, k_array):
    # para comparar com o espaço gerado com a série incluída ...
    df_espaco_param.to_csv(nome_arq_esp_param, index=False)
    k_means_e_metodo_do_cotovelo(nome_arq_esp_param, k_array, metodos_do_cotovelo, is_plotar_kmeans)
    for k in k_array:
        try:
            shutil.move('./k_{}.png'.format(k), './k_{}_espaco_param.png'.format(k))
            shutil.move('./silhueta_yellowbrick__k_{}.png'.format(k),
                        './silhueta_yellowbrick__k_{}_ESP_PARAM.png'.format(k))
        except FileNotFoundError:
            pass
    shutil.move('./distorcao_yellowbrick.png', './distorcao_yellowbrick_ESP_PARAM.png')

    # ... (com a série inclída)
    df_serie_espaco_param = pd.concat([df_serie, df_espaco_param])
    df_serie_espaco_param.to_csv(nome_arquivo_estatisticas_espaco_param, index=False)
    k_means_e_metodo_do_cotovelo(nome_arquivo_estatisticas_espaco_param, k_array, metodos_do_cotovelo, is_plotar_kmeans)
    for k in k_array:
        try:
            shutil.move('./k_{}.png'.format(k), './k_{}_espaco_param_e_serie.png'.format(k))
            shutil.move('./silhueta_yellowbrick__k_{}.png'.format(k),
                        './silhueta_yellowbrick__k_{}_SERIE_NO_ESPACO.png'.format(k))
        except FileNotFoundError:
            pass

    shutil.move('./distorcao_yellowbrick.png', './distorcao_yellowbrick_SERIE_NO_ESPACO.png')


# início do programa principal
if __name__ == '__main__':
    # Parâmetros de entrada gerais ===================================
    is_regerar_sinais = False
    is_atualizar_arquivo_covid = False
    url_owid_covid_data = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
    nome_arq_covid_completo = './owid-covid-data.csv'  # nome arquivo covid a salvar ou ler
    coluna_agrupadora_covid = 'location'
    coluna_serie_covid = 'new_cases'
    grupos_a_rejeitar = ['International', 'World']
    coluna_data = 'date'
    data_inicial = '2020-03-10'
    data_final = '2020-05-28'
    nome_arq_covid_estatisticas = './estatisticas_covid.csv'

    nome_arquivo_estatisticas_espaco_param = './covid_no_espaco_param.csv'
    nome_arq_esp_param = './espaco_param.csv'
    k_array = range(2, 22)  # Tentativa de separar df_serie de df_espaco_param
    metodos_do_cotovelo = ['distorcao_yellowbrick', 'silhueta_yellowbrick']
    is_plotar_kmeans = False
    is_plotar_esp_sing = False
    # ================================================================

    # Criando os espaços de parâmetros S 2 x Ψ. para COVID =======================================
    if is_atualizar_arquivo_covid:
        df_covid_completo = ler_serie_generica_de_arquivo_ou_url(url_owid_covid_data, is_obter_csv_como_dataframe=True,
                                                                 is_url=True)
    else:
        df_covid_completo = ler_serie_generica_de_arquivo_ou_url(nome_arq_covid_completo,
                                                                 is_obter_csv_como_dataframe=True)
    df_covid_por_agrupador = df_covid_completo[[coluna_agrupadora_covid, coluna_serie_covid, coluna_data]]

    # estatisticas covid
    df_estatisticas_covid = calcula_df_estatistico_covid(df_covid_por_agrupador, coluna_agrupadora_covid,
                                                         grupos_a_rejeitar, coluna_serie_covid, coluna_data,
                                                         data_inicial, data_final)
    df_estatisticas_covid.to_csv(nome_arq_covid_estatisticas, index=False)
    # df_estatisticas_covid = pd.read_csv(nome_arq_covid_estatisticas)
    df_estatisticas_covid = df_estatisticas_covid.drop(columns=[coluna_agrupadora_covid])

    # Gerando sinais noise ===========================================
    tipo_sinal = 'noise'
    nome_arq_tabela_estatistica = './estatisticas_noise.csv'
    familias = [64, 128, 256, 512, 1024, 2048, 4096, 8192]
    num_sinais = 10
    nome_arquivo_noise = './noise.csv'
    if is_regerar_sinais:
        df_sinais_noise = gerador_de_sinais_aleatorios(familias, num_sinais, nome_arquivo_noise)
    else:
        df_sinais_noise = pd.read_csv(nome_arquivo_noise)
    df_estatisticas_noise = calcula_df_estatistico_por_familia_e_sinal(df_sinais_noise, nome_arq_tabela_estatistica)

    # Gerando sinais colored noise ===================================
    tipo_sinal = 'colored'
    nome_arq_tabela_estatistica = './estatisticas_colorednoise.csv'
    num_valores_por_sinal = [8192]
    num_sinais = 20
    # beta 0, 1, 2 = white, pink e red noises
    betas_calculados = [0, 1, 2]
    # betas_calculados = [1]
    nome_arquivo_colorednoise = './colored_noise.csv'
    if is_regerar_sinais:
        df_sinais_colored_noise = gerador_de_sinais_colored_noise(num_valores_por_sinal, num_sinais,
                                                                  nome_arquivo_colorednoise,
                                                                  betas_calculados)
    else:
        df_sinais_colored_noise = pd.read_csv(nome_arquivo_colorednoise)
    df_estatisticas_colored_noise = calcula_df_estatistico_por_familia_e_sinal(df_sinais_colored_noise,
                                                                               nome_arq_tabela_estatistica)

    # Gerando sinais pnoise =========================================
    tipo_sinal = 'pnoise'
    nome_arq_tabela_estatistica = './estatisticas_pmnoise.csv'
    nome_arquivo_pnoise = './pnoise.csv'
    num_valores_por_sinal = [8192]
    num_sinais = 10
    # endógenas
    arr_p_endo = [0.32, 0.36, 0.42]
    beta_endo = 0.4
    # exógenas
    arr_p_exo = [0.18, 0.22, 0.28]
    beta_exo = 0.7
    num_sinais_por_familia = len(arr_p_endo) * num_sinais
    if is_regerar_sinais:
        df_endo = gerador_de_sinais_pmodel(num_valores_por_sinal, beta_endo, arr_p_endo, num_sinais)
        df_exo = gerador_de_sinais_pmodel(num_valores_por_sinal, beta_exo, arr_p_exo, num_sinais)
        df_sinais_pnoise = pd.concat([df_endo, df_exo])
        df_sinais_pnoise.to_csv(nome_arquivo_pnoise, index=False)
    else:
        df_sinais_pnoise = pd.read_csv(nome_arquivo_pnoise)
    df_estatisticas_pnoise = calcula_df_estatistico_por_familia_e_sinal(df_sinais_pnoise, nome_arq_tabela_estatistica)

    # Gerando sinais chaosnoise =======================================
    tipo_sinal = 'chaos'
    nome_arquivo_chaos = './chaos_noise.csv'
    nome_arq_tabela_estatistica = './estatisticas_chaosnoise.csv'
    num_sinais = 10
    num_valores_por_sinal = 256
    if is_regerar_sinais:
        df_sinais_log = gerador_de_sinais_logisticos(num_sinais, num_valores_por_sinal)
        df_sinais_henon = gerador_de_sinais_henon(num_sinais, num_valores_por_sinal)
        df_sinais_chaosnoise = pd.concat([df_sinais_log, df_sinais_henon])
        df_sinais_chaosnoise.to_csv(nome_arquivo_chaos, index=False)
    else:
        df_sinais_chaosnoise = pd.read_csv(nome_arquivo_chaos)
    df_estatisticas_chaosnoise = calcula_df_estatistico_por_familia_e_sinal(df_sinais_chaosnoise,
                                                                            nome_arq_tabela_estatistica)
    # espectro de sing. de todos sinais
    dic_df_sinais = {'Noise': df_sinais_noise, 'Colored': df_sinais_colored_noise, 'P-noise': df_sinais_pnoise,
                     'Chaos': df_sinais_chaosnoise}
    espectro_de_singularidades_todos(dic_df_sinais, is_plot_sing=is_plotar_esp_sing)

    # juntando todos espaços de parâmetro de estatísticas
    df_todos_espacos_estat = pd.concat(
        [df_estatisticas_noise, df_estatisticas_colored_noise, df_estatisticas_pnoise, df_estatisticas_chaosnoise])

    # agrupando serie COVID no espaço de parâmetros
    serie_no_espaco_param(df_estatisticas_covid, df_todos_espacos_estat, nome_arq_esp_param,
                          nome_arquivo_estatisticas_espaco_param,
                          is_plotar_kmeans, metodos_do_cotovelo, k_array)
