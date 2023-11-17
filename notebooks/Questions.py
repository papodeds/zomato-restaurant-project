#%% 

#Importanto bibliotecas
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import folium
import numpy as np
import datetime
from PIL import Image 
from datetime import datetime
from streamlit_folium import folium_static
from haversine import haversine
import inflection

#============================================
# Início das funções 
# =========================================== 
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}
def country_name(country_id):
    return COUNTRIES[country_id]

def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]

def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

#============================================ 
# Perfumarias do layout
#============================================

#============================================ 
# Início da estrutura lógica do código 
# ============================================

#%%
# Carregando dataset
df_raw = pd.read_csv('dataset/zomato.csv')

# Copiar a base
df = df_raw.copy()

df = rename_columns(df)


#%%
#Adicionando coluna country e convertendo id em nome dos paíse
df['country_code'] = df['country_code'].apply(country_name)

#%%
#
df['price_range'] = df['price_range'].apply(create_price_type)

#%%
#
df['color_name'] = df['rating_color'].apply(color_name)

#%%

#utils
df = df.rename(columns={'country_code': 'country'})
df = df.rename(columns={'price_range': 'price_type'})
df = df.drop ('switch_to_order_menu', axis=1)

#%%
df = df.dropna()

# %%
df = df.drop_duplicates(subset='restaurant_id')

# %%
df = df.reset_index()

#%%
df['cuisines'] = df.loc[:, 'cuisines'].apply(lambda x: x.split(",")[0])


#%%
df.head()

# %% 
df.tail()

# %%
df.shape

#%%
df.dtypes

#%%
df.info()
# %%

#%%
df.isnull().sum()

# %%
df.describe()

# %%
df.nunique()

#============================================ 
# Perguntas Gerais
#============================================
# %%
#1. Quantos restaurantes únicos estão registrados?
df.restaurant_id.nunique()

# %%
#2. Quantos países únicos estão registrados?
df.country.nunique()

# %%
#3. Quantas cidades únicas estão registradas?
df.city.nunique()

# %%
#4. Qual o total de avaliações feitas?
df.votes.sum()

# %%
#5. Qual o total de tipos de culinária registrados?
df.cuisines.nunique()

#============================================ 
# Perguntas Países
#============================================
# %%
#1. Qual o nome do país que possui mais cidades registradas?
df_aux = (df.loc[:, ['country', 'city']]
                 .groupby(['country'])
                 .nunique()
                 .sort_values('city', ascending=False)
                 .reset_index())

df_aux.loc[0,'country']

# %%
#2. Qual o nome do país que possui mais restaurantes registrados?

df_aux = (df.loc[:, ['country', 'restaurant_id']]
            .groupby(['country'])
            .nunique()
            .sort_values('restaurant_id', ascending=False)
            .reset_index())

df_aux.loc[0,'country']

# %%
#3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados?
cleaner = df['aggregate_rating'] == 4
df1 = df.loc[cleaner, :].copy()

df_aux = (df1.loc[:, ['country', 'aggregate_rating']]
            .groupby(['country'])
            .count()
            .sort_values('aggregate_rating', ascending=False)
            .reset_index())

df_aux.loc[0,'country']

# %%
#4. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos?

df_aux = (df.loc[:, ['country', 'cuisines']]
            .groupby(['country'])
            .nunique()
            .sort_values('cuisines', ascending=False)
            .reset_index())

df_aux.loc[0, 'country']

# %%
#5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
cleaner = df['aggregate_rating'] != 0
df1 = df.loc[cleaner, :]

df_aux = (df1.loc[:, ['country', 'aggregate_rating']]
            .groupby(['country'])
            .count()
            .sort_values('aggregate_rating', ascending=False)
            .reset_index()
          )

df_aux.loc[0, 'country']
# %%
#6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega?
cleaner = df['has_online_delivery'] == 1
df1 = df.loc[cleaner, :]

df_aux = (df1.loc[:, ['country', 'has_online_delivery']]
          .groupby(['country'])
          .count()
          .sort_values('has_online_delivery', ascending=False)
          .reset_index())

df_aux.loc[0, 'country']

# %%
df.has_online_delivery.value_counts()

# %%
#7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas?
cleaner = df['has_table_booking'] == 1
df1 = df.loc[cleaner, :]

df_aux = (df1.loc[:, ['country', 'has_table_booking']]
          .groupby(['country'])
          .count()
          .sort_values('has_table_booking', ascending=False)
          .reset_index())

df_aux.loc[0, 'country']

# %%
#8. Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada?
df_aux = (df.loc[:, ['country', 'votes']]
            .groupby(['country'])
            .mean()
            .sort_values('votes', ascending=False)
            .reset_index())

df_aux.loc[0, 'country']

# %%
#9. Qual o nome do país que possui, na média, a maior nota média registrada?
df_aux = round((df.loc[:, ['country', 'aggregate_rating']]
            .groupby(['country'])
            .mean()
            .sort_values('aggregate_rating', ascending=False)
            .reset_index()),3)

df_aux.loc[0, 'country']

# %%
df.describe()

# %%
#10. Qual o nome do país que possui, na média, a menor nota média registrada?
df_aux = round((df.loc[:, ['country', 'aggregate_rating']]
            .groupby(['country'])
            .mean()
            .sort_values('aggregate_rating', ascending=True)
            .reset_index()),3)

df_aux.loc[0, 'country']

# %%
# 11. Qual a média de preço de um prato para dois por país?
df_aux = round((df.loc[:, ['country', 'average_cost_for_two']]
            .groupby(['country'])
            .mean()
            .sort_values('average_cost_for_two', ascending=True)
            .reset_index()),2)

df_aux

#============================================ 
# Perguntas Cidades
#============================================
# %%
#1. Qual o nome da cidade que possui mais restaurantes registrados?
df_aux = (df.loc[:, ['city', 'restaurant_id']]
             .groupby(['city'])
             .count()
             .sort_values('restaurant_id', ascending=False)
             .reset_index())

df_aux

# %%
#2. Qual o nome da cidade que possui mais restaurantes com nota média acima de 4?
filtro = df['aggregate_rating'] > 4
df1 = df.loc[filtro, :]

df_aux = (df1.loc[:, ['city', 'aggregate_rating']]
             .groupby(['city'])
             .count()
             .sort_values('aggregate_rating', ascending=False)
             .reset_index())

df_aux.loc[0, 'city']

# %%
#3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?
filtro = df['aggregate_rating'] < 2.5
df1 = df.loc[filtro, :]

df_aux = (df1.loc[:, ['city', 'aggregate_rating']]
             .groupby(['city'])
             .count()
             .sort_values('aggregate_rating', ascending=False)
             .reset_index())

df_aux.loc[0, 'city']

# %%
#4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
df_aux = (df.loc[:, ['city', 'average_cost_for_two']]
            .groupby(['city'])
            .mean()
            .sort_values('average_cost_for_two', ascending=False)
            .reset_index())

df_aux.loc[0, 'city']


# %%
#5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas?
df_aux = (df.loc[:, ['city', 'cuisines']]
            .groupby(['city'])
            .nunique()
            .sort_values('cuisines', ascending=False)
            .reset_index())

df_aux.loc[0, 'city']

# %%
#6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas?
filtro = df['has_table_booking'] == 1
df1 = df.loc[filtro, :]

df_aux = (df1.loc[:, ['city', 'has_table_booking']]
             .groupby(['city'])
             .count()
             .sort_values('has_table_booking', ascending=False)
             .reset_index())

df_aux

# %%
#7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem entregas?
filtro = df['has_table_booking'] == 0
df1 = df.loc[filtro, :]

df_aux = (df1.loc[:, ['city', 'has_table_booking']]
             .groupby(['city'])
             .count()
             .sort_values('has_table_booking', ascending=False)
             .reset_index())

df_aux

# %%
#8. Qual o nome da cidade que possui a maior quantidade de restaurantes que aceitam pedidos online?
filtro = df['has_online_delivery'] == 1
df1 = df.loc[filtro, :]

df_aux = (df1.loc[:, ['city', 'has_online_delivery']]
             .groupby(['city'])
             .count()
             .sort_values('has_online_delivery', ascending=False)
             .reset_index())

df_aux

#============================================ 
# Perguntas Restaurantes
#============================================
# %%
#1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
df_aux = (df.loc[:, ['restaurant_name', 'votes']]
            .groupby(['restaurant_name'])
            .count()
            .sort_values('votes', ascending=False)
            .reset_index())

df_aux

# %%
#2. Qual o nome do restaurante com a maior nota média?
df_aux = (df.loc[:, ['restaurant_name', 'aggregate_rating']]
            .groupby(['restaurant_name'])
            .mean()
            .sort_values('aggregate_rating', ascending=False)
            .reset_index())

df_aux

# %%
#3. Qual o nome do restaurante que possui o maior valor de uma prato para duas pessoas?
df_aux = (df.loc[:, ['restaurant_name', 'average_cost_for_two']]
            .groupby(['restaurant_name'])
            .max()
            .sort_values('average_cost_for_two', ascending=False)
            .reset_index())

df_aux

# %%
#4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor média de avaliação?
filtro = df['cuisines'] == 'Brazilian'
df1 = df.loc[filtro, :]

df_aux = (df1.loc[:, ['restaurant_name', 'aggregate_rating']]
             .groupby('restaurant_name')
             .mean()
             .sort_values('aggregate_rating', ascending=True)
             .reset_index())

df_aux

# %%
#5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que possui a maior média de avaliação?
filtro = (df['cuisines'] == 'Brazilian') & (df['country'] == 'Brazil')
df1 = df.loc[filtro, :]

df_aux = (df1.loc[:, ['restaurant_name', 'aggregate_rating']]
             .groupby(['restaurant_name'])
             .mean()
             .sort_values('aggregate_rating', ascending=False)
             .reset_index())

df_aux

# %%
#6. Os restaurantes que aceitam pedido online são também, na média, os restaurantes que mais possuem avaliações registradas?
df_aux = round(df[['has_online_delivery', 'votes']].groupby('has_online_delivery')
                                                   .mean()
                                                   .reset_index(),3)

df_aux

# %%
#7. Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas?
df_aux = round(df[['has_table_booking', 'average_cost_for_two']].groupby('has_table_booking')
                                                   .mean()
                                                   .reset_index(),3)

df_aux

# %%
#8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América 
# possuem um valor médio de prato para duas pessoas maior que as churrascarias americanas (BBQ)?
df_aux = df[(df['country'] == 'United States of America') & ((df['cuisines'] == 'Japanese') | (df['cuisines'] == 'BBQ'))]

round(df_aux[['cuisines','average_cost_for_two']].groupby('cuisines').mean(),3)

#============================================ 
# Perguntas de Culinárias
#============================================
# %%
#1. Dos restaurantes que possuem o tipo de culinária italiana, 
# qual o nome do restaurante com a maior média de avaliação?
filtro = df['cuisines'] == 'Italian'
df1 = df.loc[filtro, :]

df_aux = (df1.loc[:, ['restaurant_name', 'aggregate_rating']]
             .groupby(['restaurant_name'])
             .mean()
             .sort_values('aggregate_rating', ascending=False)
             .reset_index())

df_aux

# %%
#2. Dos restaurantes que possuem o tipo de culinária italiana, 
# qual o nome do restaurante com a menor média de avaliação?
filtro = df['cuisines'] == 'Italian'
df1 = df.loc[filtro, :]

df_aux = (df1.loc[:, ['restaurant_name', 'aggregate_rating']]
             .groupby(['restaurant_name'])
             .mean()
             .sort_values('aggregate_rating', ascending=True)
             .reset_index())

df_aux

# %%
#3. Dos restaurantes que possuem o tipo de culinária americana, 
# qual o nome do restaurante com a maior média de avaliação?
filtro = df['cuisines'] == 'American'
df1 = df.loc[filtro, :]

df_aux = (df1.loc[:, ['restaurant_name', 'aggregate_rating']]
             .groupby(['restaurant_name'])
             .mean()
             .sort_values('aggregate_rating', ascending=False)
             .reset_index())

df_aux

# %%
#4. Dos restaurantes que possuem o tipo de culinária americana, 
# qual o nome do restaurante com a menor média de avaliação?
filtro = df['cuisines'] == 'American'
df1 = df.loc[filtro, :]

df_aux = (df1.loc[:, ['restaurant_name', 'aggregate_rating']]
             .groupby(['restaurant_name'])
             .mean()
             .sort_values('aggregate_rating', ascending=True)
             .reset_index())

df_aux

# %%
#5. Dos restaurantes que possuem o tipo de culinária árabe, 
# qual o nome do restaurante com a maior média de avaliação?
filtro = df['cuisines'] == 'Arabian'
df1 = df.loc[filtro, :]

df_aux = (df1.loc[:, ['restaurant_name', 'aggregate_rating']]
             .groupby(['restaurant_name'])
             .mean()
             .sort_values('aggregate_rating', ascending=False)
             .reset_index())

df_aux

# %%
#6. Dos restaurantes que possuem o tipo de culinária árabe, 
# qual o nome do restaurante com a menor média de avaliação?
filtro = df['cuisines'] == 'Arabian'
df1 = df.loc[filtro, :]

df_aux = (df1.loc[:, ['restaurant_name', 'aggregate_rating']]
             .groupby(['restaurant_name'])
             .mean()
             .sort_values('aggregate_rating', ascending=True)
             .reset_index())

df_aux

# %%
#7. Dos restaurantes que possuem o tipo de culinária japonesa, 
# qual o nome do restaurante com a maior média de avaliação?
filtro = df['cuisines'] == 'Japanese'
df1 = df.loc[filtro, :]

df_aux = (df1.loc[:, ['restaurant_name', 'aggregate_rating']]
             .groupby(['restaurant_name'])
             .mean()
             .sort_values('aggregate_rating', ascending=False)
             .reset_index())

df_aux

# %%
#8. Dos restaurantes que possuem o tipo de culinária japonesa, 
# qual o nome do restaurante com a menor média de avaliação?
filtro = df['cuisines'] == 'Japanese'
df1 = df.loc[filtro, :]

df_aux = (df1.loc[:, ['restaurant_name', 'aggregate_rating']]
             .groupby(['restaurant_name'])
             .mean()
             .sort_values('aggregate_rating', ascending=True)
             .reset_index())

df_aux

# %%
#9. Dos restaurantes que possuem o tipo de culinária caseira, 
# qual o nome do restaurante com a maior média de avaliação?
filtro = df['cuisines'] == 'Home-made'
df1 = df.loc[filtro, :]

df_aux = (df1.loc[:, ['restaurant_name', 'aggregate_rating']]
             .groupby(['restaurant_name'])
             .mean()
             .sort_values('aggregate_rating', ascending=False)
             .reset_index())

df_aux

# %%
#10. Dos restaurantes que possuem o tipo de culinária caseira, 
# qual o nome do restaurante com a menor média de avaliação?
filtro = df['cuisines'] == 'Home-made'
df1 = df.loc[filtro, :]

df_aux = (df1.loc[:, ['restaurant_name', 'aggregate_rating']]
             .groupby(['restaurant_name'])
             .mean()
             .sort_values('aggregate_rating', ascending=True)
             .reset_index())

df_aux

# %%
#11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas pessoas?
df_aux = (df.loc[:, ['cuisines', 'average_cost_for_two']]
            .groupby(['cuisines'])
            .mean()
            .sort_values('average_cost_for_two', ascending=False)
            .reset_index())

df_aux

# %%
#12. Qual o tipo de culinária que possui a maior nota média?

df_aux = round((df.loc[:, ['cuisines', 'votes']]
            .groupby(['cuisines'])
            .mean()
            .sort_values('votes', ascending=False)
            .reset_index()),3)

df_aux

# %%
#13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos online e fazem entregas?
filtro = ((df['has_online_delivery'] == 1 ) & (df['is_delivering_now'] == 1))
df1 = df.loc[filtro, :]

df_aux = (df1.loc[: ,['cuisines', 'restaurant_id']]
              .groupby(['cuisines'])
              .count()
              .sort_values('restaurant_id', ascending=False)
              .reset_index())

df_aux

# %%
