#Gerador de Mapa Logístico Caótico 2D (Henon Map): Atrator e Série Temporal
#2D Chaotic Logistic Map Generator (Henon Map): Attractor and Time Series
#Reinaldo R. Rosa - LABAC-INPE
#Version 1.0 for CAP239-2020

import matplotlib.pyplot as plt

#2D Henon logistic map is noise-like with "a" in (1.350,1.420) and "b" in (0.210,0.310)

def HenonMap(a,b,x,y):

    return y + 1.0 - a *x*x, b * x
 
# Map dependent parameters
a = 1.40
b = 0.210
N = 100

# Initial Condition
xtemp = 0.1
ytemp = 0.3
x = [xtemp]
y = [ytemp]


for i in range(0,N):
  xtemp, ytemp = HenonMap(a,b,xtemp,ytemp)
  x.append( xtemp )
  y.append( ytemp )

# Plot the time series
plt.plot(x,y, 'b,')
plt.title("Henon Chaotic Attractor")
plt.ylabel("Valores de Amplitude: Y")
plt.xlabel("Valores de Amplitude: X")
plt.show()

# Plot the time series
plt.plot(y)
plt.title("Henon Chaotic Noise")
plt.ylabel("Valores de Amplitude: Y")
plt.xlabel("N passos no tempo")
plt.show()
