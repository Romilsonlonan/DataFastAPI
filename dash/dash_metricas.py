import pandas as pd  # Importa a biblioteca pandas para manipulação de DataFrames
import matplotlib.pyplot as plt  # Importa a biblioteca matplotlib para plotagem de gráficos
import seaborn as sns  # Importa a biblioteca seaborn para visualização de dados

# Configurar o estilo do Seaborn para um fundo escuro
sns.set(style="darkgrid")

# Carregue seu arquivo CSV
df2 = pd.read_csv('data/novas_metricas_clientes_transformadas.csv')  # Carrega o DataFrame a partir do arquivo CSV

# Certifique-se de que as datas estão no formato datetime
df2['Data_Vendas'] = pd.to_datetime(df2['Data_Vendas'], errors='coerce')  # Converte a coluna 'Data_Vendas' para o tipo datetime

# Filtrar apenas as colunas necessárias
df2 = df2[['Nome_Clientes', 'Data_Vendas', 'Satisfação']]  # Seleciona apenas as colunas necessárias

# Agrupar dados por ano e mês
df2['Ano_Mes'] = df2['Data_Vendas'].dt.to_period('M')  # Agrupa as datas por ano e mês

# Agrupar dados por Ano_Mes e Satisfação e contar a quantidade de ocorrências
df_grouped = df2.groupby(['Ano_Mes', 'Satisfação']).size().reset_index(name='counts')  # Agrupa e conta as ocorrências

# Converter a coluna Ano_Mes de volta para datetime para fins de plotagem
df_grouped['Ano_Mes'] = df_grouped['Ano_Mes'].dt.to_timestamp()

# Configurar o estilo do gráfico para ter um fundo escuro
plt.style.use('dark_background')

# Crie um gráfico de barras separado para cada categoria
plt.figure(figsize=(15, 8))  # Define o tamanho da figura
sns.barplot(data=df_grouped, x='Ano_Mes', y='counts', hue='Satisfação')  # Plota o gráfico de barras

plt.xlabel('Data (Ano-Mês)', color='white')  # Define o rótulo do eixo x
plt.ylabel('Contagem', color='white')  # Define o rótulo do eixo y
plt.title('Contagem das Datas por Categoria', color='white')  # Define o título do gráfico
plt.xticks(rotation=40, color='white')  # Rotaciona e colore os rótulos do eixo x
plt.yticks(color='white')  # Colore os rótulos do eixo y
plt.legend(title='Pesquisa de Satisfação', facecolor='black', edgecolor='black')  # Adiciona uma legenda com fundo preto
plt.tight_layout()  # Ajusta o layout para não cortar elementos

plt.show()  # Mostra o gráfico








