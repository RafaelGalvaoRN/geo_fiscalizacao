from utilidades import get_exif_data, Denuncia, get_remote_ip, convert_rgba_to_rgb
from utilidades_audio import *
from streamlit_js_eval import get_geolocation
from streamlit_frag import menu, select_captura, oculta_elementos
import pandas as pd
import time

st.set_page_config("🌎 Radar Ambiental", layout="wide", initial_sidebar_state='collapsed')

oculta_elementos()

st.title("Denúncia Ambiental ♻️")

denunciante, local, bairro, cidade, estado, telefone, email, tipo = menu()

uploaded_file = select_captura()


is_audio_valid_for_registration = True
if tipo == "Poluição Sonora":
    is_audio_valid_for_registration = False
    uploaded_audio = st.file_uploader("Escolha um arquivo de áudio", type=['mp3', 'wav'])
    if uploaded_audio is not None:
        error_message = check_audio_conditions_with_librosa(uploaded_audio)
        if error_message:
            st.error(error_message)
            is_audio_valid_for_registration = False
        else:
            is_audio_valid_for_registration = True
            st.success("O arquivo de áudio atende aos requisitos!")
            st.audio(uploaded_audio, format='audio/wav')


if uploaded_file is not None:
    denuncia = Denuncia(tipo, denunciante, local, bairro, cidade, estado, telefone, email)

    st.image(uploaded_file, caption="Imagem carregada.", use_column_width=True)

    # Salve o arquivo carregado temporariamente e faça a previsão
    with open("temp_img.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    convert_rgba_to_rgb("temp_img.jpg").save("temp_img.jpg")

    # classifica a imagem de acordo com o tipo da denúncia e seta o atributo da classe
    denuncia.classifica_imagem()

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
        st.error("Não foi possível obter a geolocalização da foto, inviabilizando a denúncia.")
        st.warning("Tente ativar a Geolocalização do seu aparelho!")

        latitude, longitude = None, None

    if latitude and longitude:
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

        # cadastro com filtros para deploy
        # if st.button("Cadastrar Denúncia"):
        #     erro_validacao = denuncia.valida_cadastro()
        #     erro_area_img = denuncia.valida_img_distance()
        #     erro_qtd_denuncia = denuncia.valida_qtd_denuncias(10)
        #
        #     if not erro_validacao and not erro_area_img and not erro_qtd_denuncia and is_audio_valid_for_registration:
        #         denuncia.update_database()
        #         st.success("Cadastro Realizado com sucesso")
        #
        #     else:
        #         st.success("Obrigado por usar nosso aplicativo")

        # cadastro sem filtro para testes

        st.write(denuncia.img_classificacao)
        if st.button("Cadastrar Denúncia"):
            denuncia.update_database()
            st.success("Cadastro Realizado com sucesso")
