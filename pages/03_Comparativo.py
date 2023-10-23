import streamlit as st
from utilidades_antes_e_depois import *
import io


st.header("Comparativo de Registros Fotográficos")
st.markdown("""<br>""", unsafe_allow_html=True)

results = get_images()

for fiscalizacao_img, denunciantes_img in results:
    col1, col2 = st.columns(2)

    # Se suas imagens estiverem em formato BLOB (bytes), você pode usar io.BytesIO para converter para um stream:

    fiscalizacao_stream = io.BytesIO(fiscalizacao_img)
    denunciantes_stream = io.BytesIO(denunciantes_img)

    col1.image(denunciantes_stream, caption="Denúncia", use_column_width=True)
    col2.image(fiscalizacao_stream, caption="Fiscalização", use_column_width=True)
    st.markdown("---")  # Outra linha horizontal

