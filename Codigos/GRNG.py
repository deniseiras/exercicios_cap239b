#Gerador de Série Temporal Estocástica - V.1.2 por R.R.Rosa
#Trata-se de um gerador randômico não-gaussiano sem classe de universalidade via PDF.
#Input: n=número de pontos da série
#res: resolução
import numpy as np
import pandas as pd
from numpy import sqrt
import matplotlib.pyplot as plt

n=128
res = n/12

df = pd.DataFrame(np.random.randn(n) * sqrt(res) * sqrt(1 / 128.)).cumsum()
#df = pd.Series(np.random.randn(n) * sqrt(res) * sqrt(1 / 128.)).cumsum()
a=df[0].tolist()
plt.plot(a)
plt.ylabel("Valores de Amplitude, A(t)")
plt.xlabel("Tempo (t)")
plt.show()

b=int(n/10)
plt.subplot(1, 1, 1)
plt.style.use("ggplot")
#plt.figure(figsize = (10, 6))
plt.hist(a, bins=b, ec="k", alpha=0.6, color='royalblue')
plt.xlabel("Valores de Amplitude")
plt.ylabel("Contagem")

#Printing the Time Series
#print('\n'.join(map(str, a)))