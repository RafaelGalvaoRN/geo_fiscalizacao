import streamlit as st
from streamlit_frag import noticias

st.subheader("Atualizações 🚀")  # Adicionando emoji para dar destaque
st.markdown("---")  # Linha horizontal para separar o conteúdo



noticias("19/10/2023", "Inclusão da aba Painel no menu")
noticias("17/10/2023", "Melhoramento do sistema de controle de denúncias e do controle de fiscalização")
noticias("16/10/2023", "1º Versão do sistema, que se encontra em fase de ajustes")

