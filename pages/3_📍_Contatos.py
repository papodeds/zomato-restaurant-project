#======================================================================================== 
#                               Bibliotecas necessárias
#======================================================================================== 
import streamlit as st
from PIL import Image

#======================================================================================== 
#                              Parâmetros do layout
#======================================================================================== 
st.set_page_config(
    page_title='Contatos',
    page_icon=':round_pushpin:',
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
st.write('# :round_pushpin: Onde você me encontra:')
#st.markdown("<h1 style='text-align: left; color: #256fef;'> 📍 Onde me encontrar:</h1>", unsafe_allow_html=True)
st.markdown("""---""")

st.markdown(
    """
        - Portfólio:
            - http://papodeds.github.io/portfolio
        - Linkedin:
            - https://www.linkedin.com/in/phcastro03/
        - GitHub:
            - https://github.com/papodeds
        - E-mail: 
            - phcastro03@yahoo.com.br
        - Instagram:
            - https://www.instagram.com/phcastro03
        - Discord:
            - @phcastro03
    """
)

st.markdown('---')