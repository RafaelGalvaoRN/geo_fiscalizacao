import streamlit as st
from classificador_lixo import model, transform
from ml import predict_image_lixo
from utilidades import get_exif_data, Denuncia
from streamlit_js_eval import streamlit_js_eval, get_geolocation
from streamlit_frag import menu, select_captura, oculta_elementos
import pandas as pd
from rich import print


st.set_page_config("🌎 Radar Ambiental" , layout="wide", initial_sidebar_state='collapsed')


oculta_elementos()

st.title("Denúncia Ambiental ♻️")


denunciante, local, bairro, cidade, estado, telefone, email, tipo = menu()

uploaded_file = select_captura()


if uploaded_file is not None:
    denuncia = Denuncia(tipo, denunciante, local, bairro, cidade, estado, telefone, email)

    st.image(uploaded_file, caption="Imagem carregada.", use_column_width=True)
    st.write("Analisando a imagem...")

    # Salve o arquivo carregado temporariamente e faça a previsão
    with open("temp_img.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    class_idx = predict_image_lixo("temp_img.jpg", model, transform)

    # Exibindo os resultados
    classes = ['Lixo', 'Sem Lixo']
    st.write(f"A imagem foi classificada como **{classes[class_idx]}**.")
    denuncia.img_classificacao = classes[class_idx]

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
    st.write(f"Latitude: {loc['coords']['longitude']}")

    latitude = loc['coords']['latitude']
    longitude = loc['coords']['longitude']

    denuncia.img_latitude = latitude
    denuncia.img_longitude = longitude

    # Criando um mapa com um marcador baseado nas coordenadas obtidas
    map_data = pd.DataFrame({'lat': [latitude], 'lon': [longitude]})
    st.map(map_data)

    # Atualize a instância da classe Denuncia com os dados da imagem

    denuncia.set_image_bytes(uploaded_file.getbuffer())

    denuncia.calculate_image_hash()
    denuncia.update_data_denuncia()

    if st.button("Cadastrar Denúncia"):
        erro_validacao = denuncia.valida_cadastro()

        if not erro_validacao:
            denuncia.update_database()
            st.success("Cadastro Realizado com sucesso")





