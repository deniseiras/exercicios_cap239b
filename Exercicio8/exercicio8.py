# Matemática Computacional I - parte B - Exercício 8
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1o período 2020
# Autores: Denis Eiras
# 18/05/2020 - V1.0
#
#
# Descrição
#
# 8.1. Utilize o Waipy para obter o GWS (Morlet) de todos as ST do exercício 6.2.
#
# Entradas:
#
#
# Saídas:

import os
import numpy as np
import matplotlib.pyplot as plt
from Codigos.waipy.lib import waipy
from Exercicio4.exercicio4_2_2 import ler_serie_generica_de_arquivo_ou_url
from Exercicio6.exercicio6_2 import get_dados_covid_por_agrupador


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


def main():
    # Henon map not used as it causes issues with the waipy module.

    # serie covid_ndc =================================================================================================
    dados_covid = DadosConfigCovid('USA', '2020-03-10', '2020-05-28')
    df_covid_eua = get_dados_covid_por_agrupador(dados_covid)
    arr_covid_ndc_eua = df_covid_eua[dados_covid.coluna_serie_covid].values

    # serie sol  ======================================================================================================
    label_serie = 'sol'
    nome_arquivo_sol = './sol3ghz.dat'
    arr_sol = ler_serie_generica_de_arquivo_ou_url(nome_arquivo_sol)

    # serie surf_temp  ================================================================================================
    label_serie = 'surf_temp'
    nome_arquivo_surf_temp = './surftemp504.txt'
    arr_surf_temp = ler_serie_generica_de_arquivo_ou_url(nome_arquivo_surf_temp)

    arr_labels = ['covid_ndc', 'sol', 'surf_temp']
    arr_data = [arr_covid_ndc_eua, arr_sol, arr_surf_temp]
    for (label_serie, data) in zip(arr_labels, arr_data):
        try:
            result = waipy.cwt(data, 1, 1, 0.25, 4, 4 / 0.25, 0.72, 6, mother='Morlet', name='test name')
            waipy.wavelet_plot(label_serie, np.linspace(0, len(data), len(data)), data, 0.03125, result)
        except Exception as e:
            raise e
        try:
            result = waipy.cwt(data, 1, 1, 0.25, 4, 4 / 0.25, 0.72, 6, mother='DOG', name='test name')
            waipy.wavelet_plot('{}_DOG'.format(label_serie), np.linspace(0, len(data), len(data)), data, 0.03125, result)
        except Exception as e:
            plt.close('all')


# Sample execution:
if __name__ == '__main__':

    main()
