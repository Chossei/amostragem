import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import random


def simulacao(amostra, populacao):
      # Com reposição
      medias_cr = []
      tiras = range(1, populacao+1)
      for i in range(1, amostra+1):
        for j in range(1, 2501):
          lista_cr = random.choices(population = tiras, weights = None,
                            cum_weights = None, k = i)
          medias_cr.append(np.mean(lista_cr))

      # Sem reposição
      medias_sr = []
      tiras = range(1, populacao+1)

      for i in range(1, amostra+1):
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

amos, popu = st.columns(2, gap = 'large')

with amos:
      amostra = st.slider(label = 'Selecione o tamanho (acumulativo) da amostra:', min_value = 1,
                    max_value = 10, value = 3, step = 1)
with popu:
   populacao = st.slider(label = 'Selecione o tamanho da população:', min_value = 1,
                    max_value = 10, value = 5, step = 1)

# definindo as variáveis e as figuras
try: 
   reposicao, sem_reposicao = simulacao(amostra, populacao)
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

   valores = medias_cr + medias_sr

   grupos = ['Com reposição'] * len(medias_cr) + ['Sem reposição'] * len(medias_sr)

   dicionario = {'Média': valores, 'Amostra': grupos}

   base = pd.DataFrame(dicionario)
      
   fig, ax = plt.subplots(figzise(8,6))
   sns.kdeplot(data=base, x='Média', hue='Amostra', fill=True, common_norm=False, alpha=0.25, ax=ax)
      
   # Configurações do gráfico
   ax.set_xlabel('Média')
   ax.set_ylabel('Densidade')
   ax.grid(True)

   # Reproduzindo o gráfico
   st.subheader('Curvas de densidade de Kernel por Amostra')
   st.pyplot(fig)


except ValueError:
      st.error('🚨 *ATENÇÃO*: o tamanho da amostra **não** pode ser maior que o da população!')
