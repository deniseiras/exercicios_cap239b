# Matemática Computacional I - parte B - Exercício 9
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1o período 2020
# Autores: Denis Eiras
# 18/05/2020 - V1.0
#
#
# Descrição
#
# 9- Self-Organized Criticality (SOC).
# 10.1. Gere 100 ST (50 exo e 50 endo) com p-model para N=8192
# e aplique SOC.py para as 50 de cada grupo.
# 10.2. Aplique o SOC.py para todas as ST do exercício 6.3.
#
# Entradas:
#
#
# Saídas:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Codigos import soc
from Exercicio3.exercicio3 import gerador_de_sinais_pmodel
from Exercicio4.exercicio4_2_2 import ler_serie_generica_de_arquivo_ou_url
from Exercicio6.exercicio6_3 import calcula_df_estatistico


def addplot(data, label, ymin=None):
    np.seterr(divide='ignore')
    # prob_gamma, counts = soc.soc_main(data)
    prob_gamma, counts = soc.SOC(data)
    log_prob = np.log10(prob_gamma)
    p = np.array(prob_gamma)
    p = p[np.nonzero(p)]
    c = counts[np.nonzero(counts)]
    log_p = np.log10(p)
    a = (log_p[np.argmax(c)] - log_p[np.argmin(c)]) / (np.max(c) - np.min(c))
    b = log_prob[0]
    y = b * np.power(10, (a * counts))
    x = np.log10(counts)
    order = np.argsort(x)
    x = x[order]
    y = y[order]
    if ymin is None:
        plt.plot(x, y, marker=".", label=label)
    elif True in (yt < ymin for yt in y):
        plt.plot(x, y, marker=".", label=label)
    np.seterr(divide='warn')


class SeriePmodelConfig():

    def __init__(self, label, arr_p, beta, num_valores_por_sinal):
        self.label = label
        self.arr_p_cfg = arr_p
        self.num_valores_por_sinal = num_valores_por_sinal
        self.beta = beta


class DadosConfigCovid:

    def __init__(self, data_ini, data_fim):
        self.data_inicial = data_ini
        self.data_final = data_fim
        self.coluna_agrupadora_covid = 'location'
        self.grupos_a_rejeitar = ['International', 'World']
        self.coluna_serie_covid = 'new_cases'
        self.coluna_data = 'date'
        self.is_atualizar_arquivo_covid = True
        self.url_owid_covid_data = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
        # nome arquivo covid a salvar
        self.nome_arq_covid_completo = './owid-covid-data.csv'


if __name__ == '__main__':

    # Exercicio 9.1
    num_valores_por_sinal = [8192]
    num_sinais = 50

    p_min = 0.32
    p_max = 0.42
    arr_p = (p_max - p_min) * np.random.random_sample(num_sinais) + p_min
    endo_cfg = SeriePmodelConfig('Endogena', arr_p, 0.4, num_valores_por_sinal)
    p_min = 0.18
    p_max = 0.28
    arr_p = (p_max - p_min) * np.random.random_sample(num_sinais) + p_min
    exo_cfg = SeriePmodelConfig('Exogena', arr_p, 0.7, num_valores_por_sinal)

    arr_serie_cfg = [endo_cfg, exo_cfg]
    for s in arr_serie_cfg:
        plt.figure()
        for p in s.arr_p_cfg:
            df = gerador_de_sinais_pmodel(s.num_valores_por_sinal, s.beta, [p], 1)
            addplot(df.to_numpy(), s.label)
        plt.grid('both')
        plt.xlabel('log(ni)')
        plt.ylabel('log(Yi)')
        plt.tight_layout()
        plt.title("SOC para Série {}".format(s.label))
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=3)
        plt.savefig('{}.png'.format(s.label))
        plt.draw()


    # Exercicio 9.2:
    config_covid = DadosConfigCovid('2020-03-10', '2020-05-28')
    if config_covid.is_atualizar_arquivo_covid:
        df_covid_completo = ler_serie_generica_de_arquivo_ou_url(config_covid.url_owid_covid_data,
                                                                 is_obter_csv_como_dataframe=True,
                                                                 is_url=True)
    else:
        df_covid_completo = ler_serie_generica_de_arquivo_ou_url(config_covid.nome_arq_covid_completo,
                                                                 is_obter_csv_como_dataframe=True)
    df_valores_por_agrupador = df_covid_completo[
        [config_covid.coluna_agrupadora_covid, config_covid.coluna_serie_covid, config_covid.coluna_data]]
    # df_estatistico_completo = calcula_df_estatistico(df_valores_por_agrupador, config_covid)

    paises = list(set(df_valores_por_agrupador[config_covid.coluna_agrupadora_covid].to_list()))
    # column_list = ['skewness²', 'kurtosis', r'$\alpha$', r'$\beta$', r'$\beta_t$', 'name']
    excluded = list()
    plt.figure()
    for pais in paises:
        df_cada_pais = df_valores_por_agrupador[df_valores_por_agrupador[config_covid.coluna_agrupadora_covid] == pais]
        data = df_cada_pais[config_covid.coluna_serie_covid].to_list()
        try:
            addplot(data, pais)
        except Exception as e:
            pass
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=3, fontsize=6)
    plt.grid('both')
    plt.xlabel('log(ni)')
    plt.ylabel('log(Yi)')
    plt.title("SOC para a série COVID-19")
    plt.tight_layout()
    plt.savefig('covid.png')
    plt.draw()
