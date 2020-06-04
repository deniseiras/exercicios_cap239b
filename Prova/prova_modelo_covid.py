# Matemática Computacional I - parte B - Prova - Branch Direita - COVID
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1o período 2020
# Autores: Denis Eiras
# 02/06/2020 - V1.0
#
#
# Descrição
#
# Implemente as equações do MODELO IMC-SF-COVID19 e calcule os valores de g e s para os próximos 20 dias.
#
# Entradas:
#
# - N: (Inteiro) - Número de dias de previsão
# - espectros_de_pesos: (Array de floats) - Espectros de pesos
#


import matplotlib.pyplot as plt
import numpy as np
from Exercicio4.exercicio4_2_2 import ler_serie_generica_de_arquivo_ou_url


def calcula_media_dia(n_nb7, n_k, num_dias_para_media, indice_atual):
    n_nb7[indice_atual] = np.mean(n_k[max(indice_atual - num_dias_para_media + 1, 0): indice_atual + 1])
    return n_nb7


def calcula_media_periodo(n_nb7, n_k, num_dias_para_media, indice_inicial, indice_final):
    for t in range(indice_inicial, indice_final + 1):
        calcula_media_dia(n_nb7, n_k, num_dias_para_media, t)
    return n_nb7


# início do programa principal
if __name__ == '__main__':

    # Parâmetros de entrada ==========================================
    coluna_agrupadora_covid = 'location'
    coluna_serie_covid = 'new_cases'
    # location = 'Bolivia'
    location = 'United States'
    coluna_data = 'date'
    # deve incluir o dia de hoje ( ex. 7 dias de média + hoje = 8 )
    arr_str_datas_inicializacao = ['2020-05-03', '2020-05-04', '2020-05-05', '2020-05-06', '2020-05-07', '2020-05-08',
                                   '2020-05-09', '2020-05-10']
    # arr_str_datas_inicializacao = ['2020-05-21', '2020-05-22', '2020-05-23', '2020-05-24', '2020-05-25', '2020-05-26',
    #                             '2020-05-27', '2020-05-28']
    num_dias_para_media = 7
    N = 20
    g0 = 0.2  # 0.2 0.5 0.8
    espectros_de_pesos = {'espectros_1': [0.5, 0.45, 0.05], 'espectros_2': [0.7, 0.25, 0.05]}
    espectro_a_executar = 'espectros_1'

    fator_aumento_fator_n_min = 1.0
    fator_n_min = [2.0, 4.0, 5.0]
    fator_n_min = [val * fator_aumento_fator_n_min for val in fator_n_min]

    fator_aumento_fator_n_max = fator_aumento_fator_n_min
    fator_n_max = [4.0, 7.0, 10.0]
    fator_n_max = [val * fator_aumento_fator_n_max for val in fator_n_max]

    is_atualizar_arquivo_covid = False
    url_owid_covid_data = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
    # nome arquivo covid a salvar
    nome_arq_covid_completo = './owid-covid-data.csv'
    # ================================================================

    str_data_inicial = arr_str_datas_inicializacao.copy().pop()

    p1 = espectros_de_pesos[espectro_a_executar][0]
    p2 = espectros_de_pesos[espectro_a_executar][1]
    p3 = espectros_de_pesos[espectro_a_executar][2]

    num_dias_inicializacao = len(arr_str_datas_inicializacao)

    # inicializando variáveis
    # número de casos no dia ( depois são adicionados os dias de inicialização no início da lista )
    n_k = [0.0] * (N + 1)
    # fator de supressão no dia
    s = [0.0] * (N + 1 + num_dias_inicializacao)
    # média de 7 dis no dia
    n_nb7 = [0.0] * (N + 1 + num_dias_inicializacao)

    if is_atualizar_arquivo_covid:
        df_covid_completo = ler_serie_generica_de_arquivo_ou_url(url_owid_covid_data, is_obter_csv_como_dataframe=True,
                                                                 is_url=True)
    else:
        df_covid_completo = ler_serie_generica_de_arquivo_ou_url(nome_arq_covid_completo,
                                                                 is_obter_csv_como_dataframe=True)

    df_covid_completo = df_covid_completo[[coluna_agrupadora_covid, coluna_data, coluna_serie_covid]]
    is_pais = df_covid_completo[coluna_agrupadora_covid] == location
    df_covid_pais = df_covid_completo[is_pais]

    is_dias_de_inicializacao = df_covid_pais[coluna_data].isin(arr_str_datas_inicializacao)
    df_covid_pais_datas_inicializacao = df_covid_pais[is_dias_de_inicializacao]

    n_k = df_covid_pais_datas_inicializacao[coluna_serie_covid].to_list() + n_k

    # calcula media dos dias de inicializacao
    n_nb7[0] = n_k[0]
    n_nb7 = calcula_media_periodo(n_nb7, n_k, num_dias_para_media, 1, num_dias_inicializacao - 1)

    # loop t = 0 = today to N days
    for t in range(num_dias_inicializacao - 1, N+num_dias_inicializacao):

        print('Previsão de hoje + {} dias ... ~~~~~~~~~~~~~~~~~~~~~~~~~~~'.format(t - num_dias_inicializacao + 1))
        print('{} = {}'.format(coluna_serie_covid, n_k[t]))

        # formula 3
        n1 = p1 * n_k[t]
        # formula 4
        n2 = p2 * n_k[t]
        # formula 5
        n3 = p3 * n_k[t]

        if n_k[t] > n_nb7[t]:
            # formula 6
            g = n_nb7[t] / n_k[t]
        else:
            # formula 7
            g = n_k[t] / n_nb7[t]

        # formula 1
        # n8_min = g * (2 * n1 + 4 * n2 + 5 * n3)
        n8_min = g * (fator_n_min[0] * n1 + fator_n_min[1] * n2 + fator_n_min[2] * n3)
        # n8_min = g * (fator_n_min[0] * n1 + fator_n_min[1] * n2 + fator_n_min[2] * n3) / sum(fator_n_min)
        # formula 2
        # n8_max = g * (4 * n1 + 7 * n2 + 10 * n3)
        n8_max = g * (fator_n_max[0] * n1 + fator_n_max[1] * n2 + fator_n_max[2] * n3)
        # n8_max = g * (fator_n_max[0] * n1 + fator_n_max[1] * n2 + fator_n_max[2] * n3) / sum(fator_n_max)

        q_g = (1 - g) ** 2
        q_g0 = (1 - g0) ** 2

        if g0 < g:
            delta_g = (g0 - g) - q_g
        else:
            delta_g = (g0 - g) + q_g0

        # formula 8
        delta_n_k = (n_nb7[t] - n_k[t]) / n_k[t]
        # formula 9
        s[t] = (2 * delta_g + delta_n_k) / 3

        print('g0 = {}, g = {} , delta_g = {}'.format(g0, g, delta_g))
        print('Mín de casos = {}'.format(n8_min))
        print('Máx de casos = {}'.format(n8_max))
        print('Média dos últimos {} dias = {}'.format(num_dias_para_media, n_nb7[t]))
        print('Fator de supressão s = {}'.format(s[t]))
        print('')

        # calcula número de casos médio, para amanhã
        n_k[t + 1] = (n8_min + n8_max) / 2
        # calcula média móvel, para amanhã, dos últimos dias
        n_nb7 = calcula_media_dia(n_nb7, n_k, num_dias_para_media, t + 1)
        # TODO atualiza g0 ? Não está fazendo diferença
        g0 = g

    label_serie = coluna_serie_covid.capitalize()
    plt.plot(range(len(n_k)), n_k, label=label_serie)
    plt.plot(range(len(n_nb7)), n_nb7, label='Média')
    plt.title('{} do país {}'.format(label_serie, location))
    plt.xlabel('dias')
    plt.ylabel(label_serie)
    plt.legend()
    plt.show()

