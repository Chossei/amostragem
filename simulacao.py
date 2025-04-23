import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import random


def simulacao():
      # Com reposição
      medias_cr = []
      tiras = [1, 2, 3, 4]
      for i in range(1, 5):
        for j in range(1, 2501):
          lista_cr = random.choices(population = tiras, weights = None,
                            cum_weights = None, k = i)
          medias_cr.append(np.mean(lista_cr))

      # Sem reposição
      medias_sr = []
      tiras = [1,2,3,4]

      for i in range(1, 5):
        for j in range(1, 2501):
          lista_sr = random.sample(population = tiras, k = i)
          medias_sr.append(np.mean(lista_sr))

      return medias_cr, medias_sr

def histograma(data):
  fig, ax = plt.subplots()
  sns.histplot(data = data, stat = 'probability', ax = ax)
  ax.set_xlabel('Médias')
  ax.set_ylabel('Proporção')
  plt.close(fig)
  return fig

# definindo as variáveis e as figuras
reposicao, sem_reposicao = simulacao()
fig_rep = histograma(reposicao)
fig_srep = histograma(sem_reposicao)

# Calculando as métricas ----------------------
# Com reposição
minimo_cr = float(np.min(reposicao))
esperado_cr = float(np.mean(reposicao))
mediana_cr = float(np.median(reposicao))
dp_cr = float(np.std(reposicao))
max_cr = float(np.max(reposicao))

# Sem reposição

minimo_sr = float(np.min(sem_reposicao))
esperado_sr = float(np.mean(sem_reposicao))
mediana_sr = float(np.median(sem_reposicao))
dp_sr = float(np.std(sem_reposicao))
max_sr = float(np.max(sem_reposicao))

# Cálculo da diferença para uso no st.metric

metric_min = round(minimo_sr - minimo_cr, ndigits=2)
metric_mean = round(esperado_sr - esperado_cr, ndigits=2)
metric_median = round(mediana_sr - mediana_cr, ndigits=2)
metric_dp = round(dp_sr - dp_cr, ndigits=2)
metric_max = round(max_sr - max_cr, ndigits=2)

# ---------------------------------------------
# Criando a estrutura do programa

st.set_page_config(
    page_title="Simulação 1",
    layout="wide",
    page_icon="🎲",
    initial_sidebar_state="collapsed"  # opcional, se quiser a sidebar já aberta
)

st.title('🎲 Simulação - Amostragem A - 2025.1')
st.markdown("""
<div style='text-align: justify'>
<p>Neste experimento, realizamos amostragens com e sem reposição a partir de uma caixa contendo quatro números: {1, 2, 3, 4}. 
Foram selecionadas amostras de tamanhos variando entre 1 e 4, e para cada tamanho, foram feitas 250 repetições, totalizando 1000 amostras em cada tipo de amostragem.

<p>Para cada amostra, calculou-se a média dos valores selecionados. Em seguida, as distribuições dessas médias foram analisadas por meio de métricas descritivas e histogramas comparativos.
</div>
""", unsafe_allow_html=True)

st.divider()

st.subheader('🔁 Com reposição')

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
   st.metric(label = 'Mínimo',
      value = round(minimo_cr, ndigits = 4))

with c2:
   st.metric(label = 'Valor esperado',
      value = round(esperado_cr, ndigits = 4))

with c3:
   st.metric(label = 'Mediana',
      value = round(mediana_cr, ndigits = 4))

with c4:
   st.metric(label = 'Desvio padrão',
      value = round(dp_cr, ndigits = 4))

with c5:
   st.metric(label = 'Máximo',
      value = round(max_cr, ndigits = 4))
   
st.divider()

st.subheader('🚫 Sem reposição')

s1, s2, s3, s4, s5 = st.columns(5)

with s1:
   st.metric(label = 'Mínimo',
      value = round(minimo_sr, ndigits = 4),
      delta=metric_min)

with s2:
   st.metric(label = 'Valor esperado',
      value = round(esperado_sr, ndigits = 4),
      delta=metric_mean)

with s3:
   st.metric(label = 'Mediana',
      value = round(mediana_sr, ndigits = 4),
      delta=metric_median)

with s4:
   st.metric(label = 'Desvio padrão',
      value = round(dp_sr, ndigits = 4),
      delta=metric_dp)

with s5:
   st.metric(label = 'Máximo',
      value = round(max_sr, ndigits = 4),
      delta=metric_max)


# Exibição dos gráficos

st.divider()

hist1, hist2 = st.columns(2, gap = 'medium',
                          vertical_alignment='center',
                          border=False)

with hist1:
   st.subheader('Distribuição das médias com reposição')
   st.pyplot(fig_rep)

with hist2:
   st.subheader('Distribuição das médias sem reposição')
   st.pyplot(fig_srep)