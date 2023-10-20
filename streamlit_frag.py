
import streamlit as st
from ml import predict_image_lixo
from classificador_lixo import model, transform
from utilidades import get_exif_data
from streamlit_js_eval import streamlit_js_eval, get_geolocation



def noticias(noticia, data):
    st.markdown(f"**{data}**")
    # Adicionando bullet point manualmente para destaque
    st.markdown(
        f"- {noticia}.")
    st.markdown("---")  # Outra linha horizontal


def oculta_elementos():
    st.markdown("""
    <style>    
    
    
    .st-emotion-cache-164nlkn.ea3mdgi1
    {
        visibility:hidden;
    }
    </style>
    """, unsafe_allow_html=True)


def menu():
    tipo = st.selectbox("Tipo", ["Lixo", "Desmatamento",
                                 "Construção Irregular", "Represamento de Rio"])

    denunciante = st.text_input("Denunciante", max_chars=150)

    local = st.text_input("Local da ocorrência", max_chars=150)

    bairro = st.text_input("Bairro", max_chars=50)

    col1, col2 = st.columns(2)
    with col1:
        cidade = st.selectbox("Cidade", ["Canguaretama", "Vila Flor", "Pedro Velho", "Baía Formosa"])
    with col2:
        estado = st.selectbox("Estado", ["RN", "CE", "PB"])

    col3, col4 = st.columns(2)

    with col3:
        telefone = st.text_input("Telefone", max_chars=9)

    with col4:
        email = st.text_input("Email", max_chars=30)

    return denunciante, local, bairro, cidade, estado, telefone, email, tipo


def menu_fiscalizacao():
    id = st.number_input("Selecione identificação da Denúncia", step=1)

    nome_fiscal = st.text_input("Nome do fiscal", max_chars=60)

    local = st.text_input("Local da fiscalização", max_chars=150)

    bairro = st.text_input("Bairro", max_chars=50)

    col1, col2 = st.columns(2)
    with col1:
        cidade = st.text_input("Cidade", max_chars=30)
    with col2:
        estado = st.selectbox("Estado", ["RN", "CE", "PB"])

    return id, nome_fiscal, local, bairro, cidade, estado


def cadastrador_foto():
    uploaded_file = st.file_uploader(
        "Escolha uma foto para fins de análise e registro da denúncia...",
        type=["jpg", "jpeg", "jfif", "png"]
    )
    return uploaded_file


def select_captura():
    opcao = st.radio("Selecione enviar foto ou Captura", ["Enviar", "Capturar"])
    if opcao == "Enviar":
        return cadastrador_foto()

    return st.camera_input("Camera?")



def cadastro_fiscalizacao(id, uploaded_file):
        st.image(uploaded_file, caption="Imagem carregada.", use_column_width="auto")
        st.write("Analisando a imagem...")

        # Salve o arquivo carregado temporariamente e faça a previsão
        with open("temp_img.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())

        class_idx = predict_image_lixo("temp_img.jpg", model, transform)

        # Exibindo os resultados
        classes = ['Lixo', 'Sem Lixo']
        st.write(f"A imagem foi classificada como **{classes[class_idx]}**.")


        # Get and display the date and geotagging
        try:
            date, geotagging = get_exif_data("temp_img.jpg")
            st.write(f"The photo was taken on: {date}")
            st.write(f"Geotagging info: {geotagging}")
        except Exception as e:
            st.write("Could not retrieve all EXIF data.")
            st.write(str(e))

        st.write(f"Screen width is {streamlit_js_eval(js_expressions='screen.width', key='SCR')}")
        loc = get_geolocation()
        st.write(f"Your coordinates are {loc}")

        st.write(f"Latitude: {loc['coords']['latitude']}")
        st.write(f"Longitude: {loc['coords']['longitude']}")

        latitude = loc['coords']['latitude']
        longitude = loc['coords']['longitude']


        st.write(f"Cadastrar fiscalizacao para denúncia nº {id}")


        return classes[class_idx], date, geotagging, loc, latitude, longitude



        # denuncia.update_data_denuncia()