import streamlit as st
from classificador_lixo import model, transform
from ml import predict_image_lixo
from utilidades import get_exif_data, Denuncia, get_remote_ip, convert_rgba_to_rgb
from streamlit_js_eval import streamlit_js_eval, get_geolocation
from streamlit_frag import menu, select_captura, oculta_elementos
import pandas as pd
import time
from rich import print


st.set_page_config("🌎 Radar Ambiental" , layout="wide", initial_sidebar_state='collapsed')


oculta_elementos()

st.title("Denúncia Ambiental ♻️")


denunciante, local, bairro, cidade, estado, telefone, email, tipo = menu()

uploaded_file = select_captura()


if uploaded_file is not None:
    denuncia = Denuncia(tipo, denunciante, local, bairro, cidade, estado, telefone, email)

    st.image(uploaded_file, caption="Imagem carregada.", use_column_width=True)


    # Salve o arquivo carregado temporariamente e faça a previsão
    with open("temp_img.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    with open("temp_img.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    convert_rgba_to_rgb("temp_img.jpg").save("temp_img.jpg")

    class_idx = predict_image_lixo("temp_img.jpg", model, transform)

    # Exibindo os resultados
    classes = ['Lixo', 'Sem Lixo']
    # st.write(f"A imagem foi classificada como contendo: **{classes[class_idx]}**.")
    denuncia.img_classificacao = classes[class_idx]

    # Get and display the date and geotagging
    try:
        date, geotagging = get_exif_data("temp_img.jpg")
        # st.write(f"The photo was taken on: {date}")
        # st.write(f"Geotagging info: {geotagging}")
    except Exception as e:
        st.write("Could not retrieve all EXIF data.")
        st.write(str(e))

    # st.write(f"Screen width is {streamlit_js_eval(js_expressions='screen.width', key='SCR')}")


    max_retries = 5
    delay = 2  # 2 segundos
    latitude, longitude = None, None
    for i in range(max_retries):
        with st.spinner('Obtendo geolocalização...'):
            loc = get_geolocation(component_key=f"getLocation_{i}")
        if loc and 'coords' in loc:
            latitude = loc['coords']['latitude']
            longitude = loc['coords']['longitude']
            st.write("Imagem Analisada")
            break
        time.sleep(delay)

    if not latitude and not longitude:
        st.error("Não foi possível obter a geolocalização.")
        latitude, longitude = None, None

    # loc = get_geolocation()
    #
    # # st.write(f"Your coordinates are {loc}")
    #
    # # st.markdown(f"The remote ip is {get_remote_ip()}")
    #
    #
    #
    # from rich import print
    #
    # latitude = loc['coords']['latitude']
    # print(latitude)
    # longitude = loc['coords']['longitude']
    # print(longitude)


    denuncia.img_latitude = latitude
    denuncia.img_longitude = longitude
    denuncia.ip_denunciante = get_remote_ip()

    # Criando um mapa com um marcador baseado nas coordenadas obtidas
    map_data = pd.DataFrame({'lat': [latitude], 'lon': [longitude]})
    st.map(map_data)

    # Atualize a instância da classe Denuncia com os dados da imagem

    denuncia.set_image_bytes(uploaded_file.getbuffer())

    denuncia.calculate_image_hash()
    denuncia.update_data_denuncia()

    if st.button("Cadastrar Denúncia"):
        erro_validacao = denuncia.valida_cadastro()
        erro_area_img = denuncia.valida_img_distance()
        erro_qtd_denuncia = denuncia.valida_qtd_denuncias(10)

        if not erro_validacao and not erro_area_img and not erro_qtd_denuncia:
            denuncia.update_database()
            st.success("Cadastro Realizado com sucesso")





