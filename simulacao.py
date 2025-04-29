import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import random


def simulacao(amostra, populacao, n = 100000):
      # Com reposição
      medias_cr = []
      tiras = range(1, populacao+1)
      
      for j in range(n):
          lista_cr = random.choices(population = tiras, weights = None,
                            cum_weights = None, k = amostra)
          medias_cr.append(np.mean(lista_cr))

      # Sem reposição
      medias_sr = []

      for j in range(n):
          lista_sr = random.sample(population = tiras, k = amostra)
          medias_sr.append(np.mean(lista_sr))

      return medias_cr, medias_sr

def histograma(data, bins):
  fig, ax = plt.subplots()
  sns.histplot(data = data, stat = 'probability', ax = ax, bins = bins)
  ax.set_xlabel('Médias')
  ax.set_ylabel('Proporção')
  plt.close(fig)
  return fig

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
<p>Neste experimento, realizamos amostragens com e sem reposição a partir de uma caixa contendo <b>N</b> números diferentes, representando a população. Por exemplo, se N = 4, a população será {1, 2, 3, 4}. 

<p> Para cada tamanho de amostra de 1 até <b>n</b>, foram realizadas 2500 repetições, totalizando <b>n × 2500</b> amostras para cada tipo de amostragem.
            
<p>Em cada repetição, calcula-se a média dos valores selecionados. As distribuições dessas médias são então analisadas por meio de métricas descritivas e histogramas comparativos.
</div>
""", unsafe_allow_html=True)

st.divider()


amostra = st.sidebar.slider(label = 'Selecione o tamanho da amostra:', min_value = 1,
                    max_value = 10, value = 3, step = 1)

populacao = st.sidebar.slider(label = 'Selecione o tamanho da população:', min_value = 1,
                    max_value = 10, value = 5, step = 1)

bins = st.sidebar.slider(label = 'Selecione o tamanho de bins:', min_value = 10,
                    max_value = 500, value = 30, step = 10)

n = st.sidebar.radio(label = 'Selecione a quantidade de repetições do experimento:',
                     options = [100, 1000, 10000, 100000, 1000000, 10000000], index = 2)


if st.sidebar.button('Repetir experimento'):
   st.rerun()

# definindo as variáveis e as figuras
try:
   with st.spinner(show_time=True):
         reposicao, sem_reposicao = simulacao(amostra, populacao, int(n))
   fig_rep = histograma(reposicao, bins)
   fig_srep = histograma(sem_reposicao, bins)

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

   # Reproduzindo os resultados ---------------

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
      st.markdown("<h3 style='text-align: center;'>Distribuição das médias com reposição</h3>", unsafe_allow_html=True)
      st.pyplot(fig_rep)

   with hist2:
      st.markdown("<h3 style='text-align: center;'>Distribuição das médias sem reposição</h3>", unsafe_allow_html=True)
      st.pyplot(fig_srep)

   st.divider()
   # Criando o gráfico de densidade

   esp1, esp2, esp3 = st.columns([1.25, 2, 1.25])
      
   with esp2:
         valores = reposicao + sem_reposicao
      
         grupos = ['Com reposição'] * len(reposicao) + ['Sem reposição'] * len(sem_reposicao)
      
         dicionario = {'Média': valores, 'Amostra': grupos}
      
         base = pd.DataFrame(dicionario)
            
         fig, ax = plt.subplots()
         sns.kdeplot(data=base, x='Média', hue='Amostra', fill=True, common_norm=False, alpha=0.25, ax=ax)
            
         # Configurações do gráfico
         ax.set_xlabel('Média')
         ax.set_ylabel('Densidade')
      
         # Reproduzindo o gráfico
         st.markdown("<h3 style='text-align: center;'>Curvas de densidade de Kernel por Amostra</h3>", unsafe_allow_html=True)
      
         st.pyplot(fig, dpi=200, bbox_inches='tight')


except ValueError:
      st.error('🚨 *ATENÇÃO*: o tamanho da amostra **não** pode ser maior que o da população!')
