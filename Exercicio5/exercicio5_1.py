# Matemática Computacional I - parte B - Exercício 5.1
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1o período 2020
# Autores: Denis Eiras
# 28/04/2020 - V1.0
#
# O exercício 3 consiste em
#
# Entradas:
#
#
# Saídas:
##
#
# Observações
#
# Utilização dos programas:
#
# Gerador de Mapa Logístico Caótico 1D: Atrator e Série Temporal
# 1D Chaotic Logistic Map Generator: Attractor and Time Series
# Reinaldo R. Rosa - LABAC-INPE
# Version 1.0 for CAP239-2020
#
# Gerador de Mapa Logístico Caótico 2D (Henon Map): Atrator e Série Temporal
# 2D Chaotic Logistic Map Generator (Henon Map): Attractor and Time Series
# Reinaldo R. Rosa - LABAC-INPE
# Version 1.0 for CAP239-2020

# TODO - checar se henon a série está em y mesm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from Exercicio4.exercicio4_2_1 import plot_histograma_e_gev


# chaotic logistic map is f(x) = rho*x*(1-x)  with rho in (3.81,4.00)
def Logistic(rho,tau,x,y):
    return rho*x*(1.0-x), tau*x


def HenonMap(a, b, x, y):
    return y + 1.0 - a * x * x, b * x


def gerador_de_sinais_logisticos(num_sinais, num_valores_por_sinal, rho_min=3.81, rho_max=4.00, tau=1.1, x_ini=0.001,
                                 y_ini=0.001, is_plot_sinais_log=False):
    arr_rho = (rho_max - rho_min) * np.random.random_sample(num_sinais) + rho_min
    df_sinais = pd.DataFrame()
    num_sinal = 0
    for rho in arr_rho:

        # Initial Condition
        xtemp = x_ini
        ytemp = y_ini
        x = [xtemp]
        y = [ytemp]

        for i in range(0, num_valores_por_sinal):
            xtemp, ytemp = Logistic(rho, tau, xtemp, ytemp)
            x.append(xtemp)
            y.append(ytemp)

        # Plot the time series
        if is_plot_sinais_log:
            plt.plot(x)
            plt.title("Logistic Chaotic Noise")
            plt.ylabel("Valores de Amplitude: A(t)")
            plt.xlabel("N passos no tempo")
            plt.show()

        df = pd.DataFrame()
        df['valor'] = x
        df['familia'] = 'logistic'
        df['sinal'] = num_sinal
        df_sinais = pd.concat([df_sinais, df])
        num_sinal = num_sinal + 1
    return df_sinais


def gerador_de_sinais_henon(num_sinais, num_valores_por_sinal, a_min=1.350, a_max=1.420, b_min=0.210, b_max=0.310,
                            x_ini=0.001, y_ini=0.001, is_plot_sinais=False):

    df_sinais = pd.DataFrame()

    for num_sinal in range(num_sinais):
        a = (a_max - a_min) * np.random.random() + a_min
        b = (b_max - b_min) * np.random.random() + b_min

        # Initial Condition
        xtemp = x_ini
        ytemp = y_ini
        x = [xtemp]
        y = [ytemp]

        for i in range(num_valores_por_sinal):
            xtemp, ytemp = HenonMap(a, b, xtemp, ytemp)
            x.append(xtemp)
            y.append(ytemp)

        # Plot the time series
        if is_plot_sinais:
            plt.plot(y)
            plt.title("Henon Chaotic Noise")
            plt.ylabel("Valores de Amplitude: Y")
            plt.xlabel("N passos no tempo")
            plt.show()

        df = pd.DataFrame()
        df['valor'] = y
        df['familia'] = 'henon'
        df['sinal'] = num_sinal
        df_sinais = pd.concat([df_sinais, df])
    return df_sinais


# início do programa principal
if __name__ == '__main__':

    # ==== Entrada de dados ======================================================
    num_sinais = 30
    valores_por_sinal = 8192
    # ============================================================================

    df_sinais = gerador_de_sinais_logisticos(num_sinais, valores_por_sinal)
    plot_histograma_e_gev('Logistic_Chaotic_Noise', df_sinais, c, loc, scale, num_inicio, num_final, num_total)
    # plt.plot(df_sinais["valor"].to_numpy())
    # plt.title("Logistic Chaotic Noise")
    # plt.ylabel("Valores de Amplitude: A(t)")
    # plt.xlabel("N passos no tempo")
    # plt.show()
    # graph(df_sinais['valor'], boot=100)




    # execute o programa, que irá executar o trecho abaixo para encontrar melhores parametros c, loc e scale,
    # num_inicio, num_final, num_total. O prompt solicitará esses parâmtetros. Vá executando até conseguir ajustar ao
    # histograma. Faça para log noise e henon noise
    # ========INICIO=================================================================================================
    while True:
        loc = 1.0
        # c = 0.2
        # scale = 1.0
        # num_inicio = 0.01
        # num_final = 0.99
        # num_total = 100
        c = float(input("c"))
        # loc = float(input("loc"))
        scale = float(input("scale"))
        num_inicio = float(input('num inicial'))
        num_final = float(input('num_final'))
        num_total = int(input('num_total'))

        plot_histograma_e_gev('Logistic_Chaotic_Noise', df_sinais, c, loc, scale, num_inicio, num_final, num_total)
    # ========FIM=================================================================================================




    df_sinais = gerador_de_sinais_henon(num_sinais, valores_por_sinal)

    plt.plot(df_sinais["valor"].to_numpy())
    plt.title("Henon Chaotic Noise")
    plt.ylabel("Valores de Amplitude: A(t)")
    plt.xlabel("N passos no tempo")
    plt.show()
    graph(df_sinais['valor'], boot=100)
    plot_histograma_e_gev('Henon_Chaotic_Noise', df_sinais, c, loc, scale, num_inicio, num_final, num_total)