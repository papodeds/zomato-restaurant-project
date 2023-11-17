#======================================================================================== 
#                               Bibliotecas necessárias
#======================================================================================== 
import pandas as pd 
import inflection
import folium
from folium.plugins import MarkerCluster
import streamlit as st
from streamlit_folium import folium_static
from PIL import Image

#======================================================================================== 
#                              Parâmetros do layout
#========================================================================================
st.set_page_config(
    page_title='Geral',
    page_icon=':mag:',
    layout='wide'
)

#======================================================================================== 
#                                 Início das Funções
#======================================================================================== 

#===================Função para converter o código em nomes dos países===================
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

#===================Função para converter o código em ranking de preços==================
def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

#====================Função para converter o código em nomes das cores===================
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

#==========Função para renomear colunas, eliminando espaços e letras maíusculas=========
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

#=========================Função para tratamento da base de dados=========================
def utils(dataframe):
    df = dataframe.copy()

#--Remove as linhas com dados faltantes, ids duplicados de restaurantes e reseta o índice-
    df = df.dropna()
    df = df.drop_duplicates(subset='restaurant_id', keep='first')
    df = df.loc[df['average_cost_for_two'] != 0, :]
    df = df.reset_index(drop=True)

#----------------------------Convertendo id em nome dos países----------------------------
    df['country_code'] = df['country_code'].apply(country_name)

#------Categorizando a coluna price_range(1=cheap, 2=normal, 3=expensive e gourmet)------- 
    df['price_range'] = df['price_range'].apply(create_price_type)

#---------------------Adicionando a coluna color_name a base de dados---------------------
    df['color_name'] = df['rating_color'].apply(color_name)

#------------------------------Renomeando e removendo colunas-----------------------------
    df = df.rename(columns={'country_code': 'country'})
    df = df.rename(columns={'price_range': 'price_type'})
    df = df.drop('switch_to_order_menu', axis=1)

#----------------Definindo apenas um tipo de culinária para cada restaurante--------------
    df['cuisines'] = df.loc[:, 'cuisines'].apply(lambda x: x.split(",")[0])
    return df

#========================Função para plotar o mapa no painel: Geral========================
def mapa(df):
    cols = [
        'restaurant_id',
        'restaurant_name',
        'city',
        'average_cost_for_two',
        'currency',
        'longitude',
        'latitude',
        'cuisines',
        'aggregate_rating',
        'color_name'
    ]

    df_aux = (df.loc[:,cols]
                .groupby(['restaurant_id'])
                .max()
                .reset_index())
    
    map = folium.Map()
    marker_cluster = MarkerCluster(name = "restaurantes").add_to(map)

    def cor(rating_name):
        cores = df_aux.iloc[rating_name,9]
        return cores
    
    for i, location_info in df_aux.iterrows():
        folium.Marker( [location_info['latitude'],location_info['longitude']],
                      popup=location_info[['restaurant_name',
                      'average_cost_for_two',
                      'currency',
                      'aggregate_rating']],
                      icon = folium.Icon(color = cor(i) , icon='home') ).add_to(marker_cluster) 
        
    folium_static(map, width=740, height = 360)    
    return None

#======================================================================================== 
#                          Início da estrutura lógica do código
#======================================================================================== 

#-------------------------------Carregando a base de dados-------------------------------
df_raw = pd.read_csv('dataset/zomato.csv')

#----------------------------Copiando a base de dados importada---------------------------
df = df_raw.copy()

#------------------------------Renomeando as colunas da base------------------------------
df = rename_columns(df)

#------------------Limpando e alterando nomes das colunas e dados da base----------------- 
df = utils(df)

#======================================================================================== 
#                               Construção da barra lateral
#========================================================================================

#-------------------------------Importando a logo do projeto-----------------------------
image=Image.open('./img/logo_zomato.png')
st.sidebar.image(image)

st.sidebar.markdown("""---""")

#--------------------------Construindo filtros dinâmicos de países------------------------
st.sidebar.markdown('## Filtros:')

country_options = st.sidebar.multiselect(
    'Selecione os países que deseja visualizar:',
    df.loc[:, 'country'].unique().tolist(),
    default=['Brazil', 'Canada', 'England', 'New Zeland', 'Qatar', 'South Africa'],
    placeholder = ('Todos os países estão selecionados!'))

if bool(country_options):
    paises_selecionados = df['country'].isin(country_options)
    df = df.loc[paises_selecionados,:]
else:
    filtro = df.loc[:, 'country'].unique().tolist()
    paises_selecionados = df['country'].isin(filtro)
    df = df.loc[paises_selecionados,:]

st.sidebar.markdown('---')

st.sidebar.markdown("## Dados tratados:")

st.sidebar.download_button(
    label="Download",
    data=df.to_csv(index=False, sep=";"),
    file_name="data.csv",
    mime="text/csv",
    )

st.sidebar.markdown('---')
st.sidebar.markdown('###### Powered by Pedro Castro | papodeds®')

#======================================================================================== 
#                        Construção do layout para o Streamlit
#========================================================================================

#-----------------------------------Título da aba "Geral"--------------------------------
st.write('# :mag: Geral')
st.markdown('---')

with st.container():
    st.markdown('###### Métricas Gerais:') 
    col1, col2, col3, col4, col5 = st.columns(5, gap='small')

    with col1:
        paises = df['country'].nunique()
        col1.metric(label = 'Países Atendidos:', value = paises )

    with col2:
        cidades = df['city'].nunique()
        col2.metric(label = 'Cidades Atendidas:', value = cidades )
        
    with col3:
        restaurantes = f'{df.restaurant_id.nunique():,}'.replace(',','.')
        col3.metric(label = 'Restaurantes cadastrados:', value = restaurantes )

    with col4:
        culinarias = df['cuisines'].nunique()
        col4.metric(label = 'Culinárias oferecidas:', value = culinarias )
        
    with col5:
        avaliacoes = f'{df.votes.sum():,}'.replace(',','.')
        col5.metric(label = 'Avaliações na plataforma:', value = avaliacoes )
            
    st.markdown('---')
  
with st.container():
    st.markdown('###### Encontre nosso restaurante mais próximo de você:')
    mapa(df)

st.markdown('---')
#======================================================================================== 
#                        Final do layout para o Streamlit
#========================================================================================