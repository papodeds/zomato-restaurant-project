#======================================================================================== 
#                               Bibliotecas necessárias
#======================================================================================== 
import streamlit as st
from PIL import Image

#======================================================================================== 
#                              Parâmetros do layout
#========================================================================================
st.set_page_config(
    page_title='Home',
    page_icon=':large_blue_circle:',
    layout='centered'
)

#======================================================================================== 
#                               Construção da barra lateral
#========================================================================================
image=Image.open('./img/logo_zomato.png')
st.sidebar.image(image)

st.sidebar.markdown("""---""")

st.sidebar.markdown('###### Powered by Pedro Castro | papodeds®')

#======================================================================================== 
#                        Construção do layout para o Streamlit
#======================================================================================== 
st.write('# :large_blue_circle: ZOMATO restaurant partner®')
st.markdown('---')

st.markdown(
        """
        ### Seja bem-vindo ao dashboard interativo!

        Este dashboard foi construído para facilitar o acompanhamento das principais métricas sobre o nosso negócio através de 5 painéis interativos: Geral, Países, Cidades, Restaurantes e Culinárias.
        
        #### Sobre a ZOMATO restaurant partner®:

        Lançada em 2010, nossa plataforma tecnológica é como um elo entre clientes, restaurantes e entregadores, atendendo a várias necessidades. 
        
        Os clientes usam a plataforma para descobrir restaurantes, fazer avaliações, ver fotos, pedir comida, reservar mesas e pagar suas refeições.

        Para os parceiros de restaurantes, oferecemos ferramentas de marketing especiais para ajudar a expandir seus negócios, além de um serviço de entrega confiável. 
        
        A Hyperpure, nossa solução exclusiva de aquisição, fornece ingredientes de alta qualidade.

        E não esquecemos dos parceiros de entrega, que têm a chance de ganhar dinheiro de forma transparente e flexível. Queremos que todos façam parte dessa experiência!

        #### Fonte dos dados:

        Ainda que a ZOMATO restaurant partner® seja uma empresa real, o estudo e a construção
        deste dashboard dinâmico foi realizado através de uma base de dados pública e disponibilizada no site 
        Kaggle, através do link a seguir:  https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv .

        Assim sendo, é importante ressaltar que a construção do dashboard tem por finalidade resolver problemas
        de negócios num estudo de caso a partir de um negócio real, porém sem relação direta com a empresa.
    
        #### Como utilizar este Dashboard?

        - :large_blue_circle: Home:
            - Aqui você encontra uma breve descrição sobre a ideia e construção do projeto.
        - :mag: Geral:
            - Na aba "Geral" você terá acesso a métricas consolidadas sobre países, cidades, restaurantes, 
            culinárias e avaliações, além de um mapa para localizar o restaurante mais próximo de você.
        - :bar_chart: Dashboards:
            - Na aba "Dashboards" você terá acesso aos 4 painéis interativos construídos para apresentar os dados analisados.
                - Você terá acesso a métricas, gráficos e tabelas segmentados em países, cidades, restaurantes, culinárias.
        - :round_pushpin: Contatos:
            - Já na aba "Contatos" você encontrará os principais canais de contato onde poderá entrar em contato comigo.

    """
) 
st.markdown('---')