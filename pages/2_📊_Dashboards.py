#======================================================================================== 
#                               Bibliotecas necessárias
#======================================================================================== 
import pandas as pd 
import inflection
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
import streamlit as st
from streamlit_folium import folium_static
from PIL import Image

#======================================================================================== 
#                              Parâmetros do layout
#========================================================================================
st.set_page_config(
    page_title='Dashboards',
    page_icon=':bar_chart:',
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

#===============Função para plotar gráfico de barras no painel: Restaurantes================
def rest_countries(df):
    df_aux = (df.loc[:, ['country', 'restaurant_id']]
                 .groupby(['country'])
                 .nunique()
                 .sort_values('restaurant_id', ascending=False)
                 .reset_index())
    fig = px.bar(df_aux,
                 x='country',
                 y='restaurant_id',
                 text = 'restaurant_id',
                 text_auto=".2f",
                 labels = {'country': 'Países', 'restaurant_id':'Total de Restaurantes'}, 
                 title = 'Restaurantes cadastrados por país'
                 )#.update_layout(plot_bgcolor='#f2f2f2')
    return fig

#===============Função para plotar gráfico de barras no painel: Restaurantes================
def cities_countries(df):
    df_aux = (df.loc[:, ['country', 'city']]
                 .groupby(['country'])
                 .nunique()
                 .sort_values('city', ascending=False)
                 .reset_index())
    fig = px.bar(df_aux,
                 x = 'country',
                 y = 'city',
                 text = 'city',
                 text_auto=".2f",
                 labels = {'country': 'Países', 'city':'Total de Cidades'}, 
                 title = 'Cidades atendidas por país'
                 )
    return fig

#===============Função para plotar gráfico de barras no painel: Restaurantes================
def cuisines_countries(df):
    df_aux = (df.loc[:, ['country', 'cuisines']]
                 .groupby(['country'])
                 .nunique()
                 .sort_values('cuisines', ascending=False)
                 .reset_index())
    fig = px.bar(df_aux,
                 x = 'country',
                 y = 'cuisines',
                 text = 'cuisines',
                 text_auto=".2f",
                 labels = {'country': 'Países', 'cuisines':'Tipos de Culinária'}, 
                 title = 'Tipos de culinárias por país'
                 )
    return fig

#===============Função para plotar gráfico de barras no painel: Restaurantes================
def votes_countries(df):
    df_aux = (df.loc[:, ['country', 'votes']]
                 .groupby(['country'])
                 .mean()
                 .sort_values('votes', ascending=False)
                 .reset_index())
    fig = px.bar(df_aux,
                 x = 'country',
                 y = 'votes',
                 text = 'votes',
                 text_auto=".2f",
                 labels = {'country': 'Países', 'votes': 'Média de avaliações'}, 
                 title = 'Média de avaliações por país'
                 )
    return fig

#===============Função para plotar gráfico de barras no painel: Restaurantes================
def costfortwo_countries(df):
    df_aux = (df.loc[:, ['country', 'average_cost_for_two']]
                 .groupby(['country'])
                 .mean()
                 .sort_values('average_cost_for_two', ascending=False)
                 .reset_index())
    fig = px.bar(df_aux,
                 x = 'country',
                 y = 'average_cost_for_two',
                 text = 'average_cost_for_two',
                 text_auto=".2f",
                 labels = {'country': 'Países', 'average_cost_for_two':'Média do custo para duas pessoas'}, 
                 title = 'Média de custo da refeição para duas pessoas por país'
                 )
    return fig

#==================Função para plotar gráfico de barras no painel: Cidades==================
def rest_cities(df, top_cities):
    df_aux = (df.loc[:, ['country', 'city', 'restaurant_id']]
                 .groupby(['city', 'country'])
                 .count()
                 .sort_values(['restaurant_id', 'country'], ascending=False)
                 .reset_index()
                 .head(top_cities))
    fig = px.bar(df_aux,
                 x = 'city',
                 y = 'restaurant_id',
                 color = 'country',
                 text = 'restaurant_id',
                 text_auto=".2f",
                 labels = {'country': 'Países', 'city': 'Cidades', 'restaurant_id': 'Total de restaurantes'}, 
                 title = f'TOP {top_cities} - Cidades com mais restaurantes cadastrados'
                 )
    return fig

#==================Função para plotar gráfico de barras no painel: Cidades==================
def avg_up4_cities(df, top_cities):
    filtro = df['aggregate_rating'] > 4
    df1 = df.loc[filtro, :]

    df_aux = (df1.loc[:, ['city', 'country', 'aggregate_rating']]
             .groupby(['city', 'country'])
             .count()
             .sort_values(['aggregate_rating', 'country'], ascending=False)
             .reset_index()
             .head(top_cities))
    fig = px.bar(df_aux,
                 x = 'city',
                 y = 'aggregate_rating',
                 color = 'country',
                 text = 'aggregate_rating',
                 text_auto=".2f",
                 labels = {'country': 'Países', 'city': 'Cidades', 'aggregate_rating': 'Avaliação média'}, 
                 title = f'TOP {top_cities} - Cidades com mais restaurantes avaliados acima de 4'
                 )
    return fig

#==================Função para plotar gráfico de barras no painel: Cidades==================
def avg_low25_cities(df, top_cities):
    filtro = df['aggregate_rating'] < 2.5
    df1 = df.loc[filtro, :]

    df_aux = (df1.loc[:, ['city', 'country', 'aggregate_rating']]
             .groupby(['city', 'country'])
             .count()
             .sort_values(['aggregate_rating', 'country'], ascending=False)
             .reset_index()
             .head(top_cities))
    fig = px.bar(df_aux,
                 x = 'city',
                 y = 'aggregate_rating',
                 color = 'country',
                 text = 'aggregate_rating',
                 text_auto=".2f",
                 labels = {'country': 'Países', 'city': 'Cidades', 'aggregate_rating': 'Avaliação média'}, 
                 title = f'TOP {top_cities} - Cidades com mais restaurantes avaliados abaixo de 2.5'
                 )
    return fig

#==================Função para plotar gráfico de barras no painel: Cidades==================
def topcuisines_cities(df, top_cities):
    df_aux = (df.loc[:, ['city', 'country', 'cuisines']]
            .groupby(['city', 'country'])
            .nunique()
            .sort_values(['cuisines', 'country'], ascending=False)
            .reset_index()
            .head(top_cities))
    fig = px.bar(df_aux,
                 x = 'city',
                 y = 'cuisines',
                 color = 'country',
                 text = 'cuisines',
                 text_auto=".2f",
                 labels = {'country': 'Países', 'city': 'Cidades', 'cuisines': 'Tipos de culinária'}, 
                 title = f'TOP {top_cities} - Cidades com mais tipos de culinária disponíveis'
                 )
    return fig

#===============Função para plotar gráfico de barras no painel: Restaurantes================
def top_rest(df, top_restaurants):
    df_aux = (df.loc[:, ['restaurant_name', 'country', 'aggregate_rating']]
            .groupby(['restaurant_name', 'country'])
            .mean()
            .sort_values(['aggregate_rating', 'country'], ascending= False)
            .reset_index()
            .head(top_restaurants))
    fig = px.bar(df_aux,
                 x = 'restaurant_name',
                 y = 'aggregate_rating',
                 color = 'country',
                 text = 'aggregate_rating',
                 text_auto=".2f",
                 labels = {'country': 'Países', 'restaurant_name': 'Restaurante', 'aggregate_rating': 'Avaliação média'}, 
                 title = f'TOP {top_restaurants} - Restaurantes com a melhor média de avaliação'
                 )
    return fig 

#===============Função para plotar gráfico de barras no painel: Restaurantes================
def top_cost_for_two(df, top_restaurants, rank):
    if rank == 'max':
        df_aux = (df.loc[:, ['restaurant_name', 'country', 'average_cost_for_two']]
                .groupby(['restaurant_name', 'country'])
                .max()
                .sort_values(['average_cost_for_two', 'country'], ascending=False)
                .reset_index()
                .head(top_restaurants))
        fig = px.bar(df_aux,
                    x = 'restaurant_name',
                    y = 'average_cost_for_two',
                    color = 'country',
                    text = 'average_cost_for_two',
                    text_auto=".2f",
                    labels = {'restaurant_name': 'Restaurante', 'country': 'Países', 'average_cost_for_two': 'Preço do prato para 2'}, 
                    title = f'TOP {top_restaurants} - Restaurantes com o prato para duas pessoas mais caro'
                    )
    else:
        df_aux = (df.loc[:, ['restaurant_name', 'country', 'average_cost_for_two']]
                .groupby(['restaurant_name', 'country'])
                .min()
                .sort_values(['average_cost_for_two', 'country'], ascending=True)
                .reset_index()
                .head(top_restaurants))
        fig = px.bar(df_aux,
                    x = 'restaurant_name',
                    y = 'average_cost_for_two',
                    color = 'country',
                    text = 'average_cost_for_two',
                    text_auto=".2f",
                    labels = {'restaurant_name': 'Restaurante', 'country': 'Países', 'average_cost_for_two': 'Preço do prato para 2'}, 
                    title = f'TOP {top_restaurants} - Restaurantes com o prato para duas pessoas mais barato'
                    )
    return fig

#================Função para plotar gráfico de pizza no painel: Restaurantes================
def online_delivery(df):
    df_aux = (df[['has_online_delivery', 'restaurant_id']].groupby('has_online_delivery')
                                                          .count()
                                                          .reset_index()
                                                          .head(top_restaurants))
    df_aux['Has_Delivery_Perc'] = (df_aux['restaurant_id'] / df_aux['restaurant_id'].sum())

    def create_faz_ou_nao(delivery):
        if delivery == 1:
            return "Entregam"
        else:
            return "Não entregam"
        
    df_aux['faz_ou_nao'] = df_aux['has_online_delivery'].apply(create_faz_ou_nao)
    
    fig = px.pie(df_aux, 
                 values='Has_Delivery_Perc', 
                 names='faz_ou_nao',
                 labels = {'faz_ou_nao': 'Faz entregas', 'Has_Delivery_Perc': 'Percentual'},
                 title = 'Restaurantes que fazem entregas online'
                 )
    fig.update_traces(textposition='outside', textinfo='percent+label')
    return fig

#================Função para plotar gráfico de pizza no painel: Restaurantes================
def table_booking(df):
    df_aux = (df[['has_table_booking', 'restaurant_id']].groupby('has_table_booking')
                                                        .count()
                                                        .reset_index()
                                                        .head(top_restaurants))
    df_aux['Has_table_booking_Perc'] = (df_aux['restaurant_id'] / df_aux['restaurant_id'].sum())

    def create_table_booking(tb):
        if tb == 1:
            return "Reservam"
        else:
            return "Não reservam"
        
    df_aux['faz_ou_nao_tb'] = df_aux['has_table_booking'].apply(create_table_booking)
    
    fig = px.pie(df_aux, 
                 values='Has_table_booking_Perc', 
                 names='faz_ou_nao_tb',
                 labels = {'faz_ou_nao_tb': 'Fazem reservas', 'Has_table_booking_Perc': 'Percentual'},
                 title = 'Restaurantes que fazem reservas de mesa'
                 )
    fig.update_traces(textposition='outside', textinfo='percent+label')
    return fig

#================Função para retornar um dataframe para o painel: Culinárias================
def top_rest_cuisine(df, culinaria):
    filtro = df['cuisines'] == culinaria
    df1 = df.loc[filtro, :]

    df_aux = (df1.loc[:, ['restaurant_name', 'aggregate_rating']]
                  .groupby(['restaurant_name'])
                  .mean()
                  .sort_values('aggregate_rating', ascending=False)
                  .reset_index()) 
    return df_aux

#================Função para retornar um dataframe para o painel: Culinárias================
def top_c(df, top_cuisines): 
    df = (df.loc[:, ['cuisines', 'aggregate_rating', 'votes']]
            .groupby(['cuisines', 'votes'])
            .mean()
            .sort_values(['aggregate_rating', 'votes'], ascending=False).reset_index())
    return df.head(top_cuisines)

#================Função para retornar um dataframe para o painel: Culinárias================
def top_c_cost(df, top_cuisines):
    df_aux = round((df.loc[:, ['restaurant_name', 'cuisines', 'country', 'average_cost_for_two']]
                .groupby(['cuisines', 'restaurant_name', 'country'])
                .mean()
                .sort_values('average_cost_for_two', ascending=False)
                .reset_index()),2)
    return df_aux.head(top_cuisines)

#================Função para retornar um dataframe para o painel: Culinárias================
def top_c_has(df, top_cuisines):
    filtro = ((df['has_online_delivery'] == 1 ) & (df['is_delivering_now'] == 1))
    df1 = df.loc[filtro, :]

    df_aux = (df1.loc[: ,['cuisines', 'restaurant_id']]
              .groupby(['cuisines'])
              .count()
              .sort_values('restaurant_id', ascending=False)
              .reset_index())
    return df_aux.head(top_cuisines)

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

#--------------------------------Título da aba "Dashboards"------------------------------
st.write('# :bar_chart: Dashboards')

#----------------------------Construindo os 5 painéis dinâmicos--------------------------
tab1, tab2, tab3, tab4 = st.tabs([':earth_americas: Países', 
                                  ':city_sunrise: Cidades', 
                                  ':convenience_store: Restaurantes',
                                  ':green_salad: Culinárias'])

#-------------------------------Construindo o painel: Países-----------------------------
with tab1:
    with st.container():
        fig = rest_countries(df)
        st.plotly_chart(fig, use_container_width=True)
    
    with st.container():
        col1, col2 = st.columns(2, gap='small')

        with col1:
            fig = cities_countries(df)
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            fig = cuisines_countries(df)
            st.plotly_chart(fig, use_container_width=True)

    with st.container():
        col1, col2 = st.columns(2, gap='small')

        with col1:
            fig = votes_countries(df)
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            fig = costfortwo_countries(df)
            st.plotly_chart(fig, use_container_width=True)

#------------------------------Construindo o painel: Cidades-----------------------------
with tab2: 
    with st.container():
        st.markdown('### Filtros:')
        top_cities = st.slider('Defina a quantidade de cidades que deseja visualizar:'
                               ,1, 20, 10)
    st.markdown('---')
    
    with st.container():
        fig = rest_cities(df, top_cities)
        st.plotly_chart(fig, use_container_width=True)
    
    with st.container():
        col1, col2 = st.columns(2, gap='small')

        with col1:
            fig = avg_up4_cities(df, top_cities)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = avg_low25_cities(df, top_cities)
            st.plotly_chart(fig, use_container_width=True)

    with st.container():
        fig = topcuisines_cities(df, top_cities)
        st.plotly_chart(fig, use_container_width=True)

#----------------------------Construindo o painel: Restaurantes--------------------------
with tab3:
    with st.container():
        st.markdown('### Filtros:')
        top_restaurants = st.slider('Defina a quantidade de restaurantes que deseja visualizar:'
                                    ,1, 20, 10)
    st.markdown('---')

    with st.container():
        fig = top_rest(df, top_restaurants)
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        col1, col2 = st.columns(2, gap='small')

        with col1:
            rank = 'max'
            fig = top_cost_for_two(df, top_restaurants, rank)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            rank = 'min'
            fig = top_cost_for_two(df, top_restaurants, rank)
            st.plotly_chart(fig, use_container_width=True)

    with st.container():
        col1, col2 = st.columns(2, gap='small')

        with col1:
            fig = online_delivery(df)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = table_booking(df)
            st.plotly_chart(fig, use_container_width=True)

#-----------------------------Construindo o painel: Culinárias---------------------------            
with tab4:
    with st.container():
        st.markdown('### Filtros:')
        top_cuisines = st.slider('Defina a quantidade de culinárias que deseja visualizar:'
                                 ,1, 20, 10)
    
    st.markdown('---')

    with st.container():
        st.markdown('###### Restaurante cadastrado com a melhor avaliação média por tipo de culinária:')
        col1, col2, col3 = st.columns(3, gap='small')

        with col1:
            culinaria = 'Continental'
            top = top_rest_cuisine(df, culinaria)
            if top.empty:
                col1.metric(label = 'Continental: Sem cadastro', value = '0.0/5.0')
            else:
                name = top.loc[0, 'restaurant_name']
                aggregate = top.loc[0, 'aggregate_rating']
                col1.metric(label = f'Continental: {name}', value = f'{aggregate}/5.0')

        with col2:
            culinaria = 'European'
            top = top_rest_cuisine(df, culinaria)
            if top.empty:
                col2.metric(label = 'Européia: Sem cadastro', value = '0.0/5.0')
            else:
                name = top.loc[0, 'restaurant_name']
                aggregate = top.loc[0, 'aggregate_rating']
                col2.metric(label = f'Européia: {name}', value = f'{aggregate}/5.0')
            
        with col3:
            culinaria = 'BBQ'
            top = top_rest_cuisine(df, culinaria)
            if top.empty:
                col3.metric(label = 'Barbecue: Sem cadastro', value = '0.0/5.0')
            else:
                name = top.loc[0, 'restaurant_name']
                aggregate = top.loc[0, 'aggregate_rating']
                col3.metric(label = f'Barbecue: {name}', value = f'{aggregate}/5.0')
            
    with st.container():
        col4, col5, col6 = st.columns(3, gap='small')

        with col4:
            culinaria = 'North Indian'
            top = top_rest_cuisine(df, culinaria)
            if top.empty:
                col4.metric(label = 'Indiana: Sem cadastro', value = '0.0/5.0')
            else:
                name = top.loc[0, 'restaurant_name']
                aggregate = top.loc[0, 'aggregate_rating']
                col4.metric(label = f'Indiana: {name}', value = f'{aggregate}/5.0')

        with col5:
            culinaria = 'Sushi'
            top = top_rest_cuisine(df, culinaria)
            if top.empty:
                col5.metric(label = 'Sushi: Sem cadastro', value = '0.0/5.0')
            else:
                name = top.loc[0, 'restaurant_name']
                aggregate = top.loc[0, 'aggregate_rating']
                col5.metric(label = f'Sushi: {name}', value = f'{aggregate}/5.0')

        with col6:
            culinaria = 'Coffee and Tea'
            top = top_rest_cuisine(df, culinaria)
            if top.empty:
                col6.metric(label = 'Cafeteria: Sem cadastro', value = '0.0/5.0')
            else:
                name = top.loc[0, 'restaurant_name']
                aggregate = top.loc[0, 'aggregate_rating']
                col6.metric(label = f'Cafeteria: {name}', value = f'{aggregate}/5.0')
    
    st.markdown('---')

    with st.container():
        st.markdown(f'###### TOP {top_cuisines} - Culinárias com melhor média de avaliação e mais votos:')
        df1 = top_c(df, top_cuisines)
        st.dataframe(df1, use_container_width=True)

    with st.container():
        st.markdown(f'###### TOP {top_cuisines} - Culinária com maior preço médio de prato para duas pessoas:')
        df1 = top_c_cost(df, top_cuisines)
        st.dataframe(df1, use_container_width=True)

    with st.container():
        st.markdown(f'###### TOP {top_cuisines} - Culinárias, cujos restaurantes aceitam pedidos on-line e fazem entregas:')
        df1 = top_c_has(df, top_cuisines)
        st.dataframe(df1, use_container_width=True)

st.markdown('---')
#======================================================================================== 
#                        Final do layout para o Streamlit
#========================================================================================