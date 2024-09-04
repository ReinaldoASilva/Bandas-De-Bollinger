# Bibliotecas
from datetime import date
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as matplotlib
import numpy as np

# Obter dados históricos

ticker = '^GSPC'
inicio = '2015-01-01'
fim = '2024-08-31'

df = yf.download(ticker, start=inicio, end=fim)

df.head()

# Gráfico

df['Adj Close'].plot(grid = True, figsize=(20,15), linewidth = 3, fontsize = 15, color = 'darkblue')
plt.xlabel('data', fontsize= 15)
plt.ylabel('Pontos', fontsize=15)
plt.title('Ibovespa', fontsize = 15)
plt.legend()

# Calculando as Bandas de Bollinger

#Parâmetros iniciais
periodo = 50
desvios = 2

df['desvio'] = df['Adj Close'].rolling(periodo).std()
df['MM'] = df['Adj Close'].rolling(periodo).mean()
df['Banda_sup'] = df['MM'] + (df['desvio']*desvios)
df['Banda_inf'] = df['MM'] - (df['desvio']*desvios)

# Filtrando os valores missing
df = df.dropna(axis=0)

# Gráfico das Bandas

df[['Adj Close','MM','Banda_sup','Banda_inf']].plot(grid=True
        , figsize=(20,15)
        , linewidth=2
        , fontsize=15
        ,color=['darkblue','orange','green','red'])
plt.xlabel('Data', fontsize=15)
plt.ylabel('Pontos', fontsize=15)
plt.title('Ibovespa')
plt.legend()

# Contrução de Alvos

periodos = 3
df.loc[:,'Retorno'] = df['Adj Close'].pct_change(periodos)
df.loc[:,'Alvo'] = df['Retorno'].shift(-periodos)

# Ler as primeiras linhas 
df.head()

# Ler as últimas linhas
df.tail()

# Filtrando os valores missing
df = df.dropna(axis=0)

# Criando a regra de trade
df.loc[:, 'Regra'] = np.where(df.loc[:, 'Adj Close'] > df.loc[:, 'Banda_sup'], 1,0)
df.loc[:, 'Regra'] = np.where(df.loc[:, 'Adj Close'] < df.loc[:, 'Banda_inf'],-1, df.loc[:, 'Regra'])

# Aplicando a regra do Alvo
df.loc[:,'Trade'] = df.loc[:,'Regra']*df.loc[:,'Alvo']

# Calculando o Resultado acumulado em juros simples

df.loc[:,'Retorno_Trade_BB'] = df['Trade'].cumsum()

# Plotando o Resultado

df['Retorno_Trade_BB'].plot( figsize=(20,15)
        , linewidth=3
        , fontsize=15
        , color='darkblue')

plt.xlabel('Data', fontsize=15)
plt.ylabel('Retorno Acumulado em Juros Simples', fontsize=15)
plt.title('Retorno Acumulado em Juros Simples com Alvos', fontsize=15)
plt.legend()
