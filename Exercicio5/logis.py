#Gerador de Mapa Logístico Caótico 1D: Atrator e Série Temporal
#1D Chaotic Logistic Map Generator: Attractor and Time Series
#Reinaldo R. Rosa - LABAC-INPE
#Version 1.0 for CAP239-2020

import numpy as np
#import pandas as pd
import matplotlib.pyplot as plt

#chaotic logistic map is f(x) = rho*x*(1-x)  with rho in (3.81,4.00)
def Logistic(rho,tau,x,y):

    return rho*x*(1.0-x), tau*x


# Map dependent parameters
rho = 3.88
tau = 1.1
N = 256

# Initial Condition
xtemp = 0.001
ytemp = 0.001
x = [xtemp]
y = [ytemp]


for i in range(1,N):
  xtemp, ytemp = Logistic(rho,tau,xtemp,ytemp)
  x.append( xtemp )
  y.append( ytemp )


# Plot the Attractor
plt.plot(x,y, 'b,')
plt.title("Logistic Chaotic Attractor")
plt.ylabel("Valores de Amplitude: A(t)")
plt.xlabel("Valores de Amplitude: A(t+tau)")
plt.show()

# Plot the time series
plt.plot(x)
plt.title("Logistic Chaotic Noise")
plt.ylabel("Valores de Amplitude: A(t)")
plt.xlabel("N passos no tempo")
plt.show()

