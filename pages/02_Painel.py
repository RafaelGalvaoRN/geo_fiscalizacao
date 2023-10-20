import streamlit as st
from base_dados.crud import get_dataframe
from utilidades_dashboard import plot_denuncias, plot_tipo_denuncias, menu_cidades

st.header("Painel de Denúncias")
st.markdown("""<br>""", unsafe_allow_html=True)

df = get_dataframe()
df = menu_cidades(df)



col1, col2 = st.columns(2)

with col1:
    plot_denuncias(df)
with col2:
    plot_tipo_denuncias(df)


