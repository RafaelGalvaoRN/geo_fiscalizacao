from utilidades_login import *
from streamlit_folium import folium_static
from streamlit_frag import menu_fiscalizacao, \
    select_captura, cadastro_fiscalizacao
from utilidades import Fiscalizacao

st.set_page_config(layout="wide")  # Usa o layout mais largo disponível

password = st.text_input("Digite a senha:", type='password')
blocks = generate_login_block()

if password != "":
    if is_authenticated(password):
        clean_blocks(blocks)
        st.success("Autenticação realizada com sucesso!")
        data = get_data()

        data_tratado = trata_df(data, drop_column=True, rename_column=True, filter_status=True)

        st.title("Tabela Controle das Denúncias")
        st.table(data_tratado)

        st.title("Mapa das Denúncias")
        data = trata_df(data, filter_status=True)
        mapa = plot_denuncias_map(data)
        with st.expander("Geolocalização e Fotos"):
            folium_static(mapa, width=1500, height=600)



        st.title("Registro de Fiscalização")
        id_denuncia, nome_fiscal, local, bairro, cidade, estado = menu_fiscalizacao()

        upload_file = select_captura()
        if upload_file is not None:
            date, geotagging, loc, latitude, longitude = cadastro_fiscalizacao(id_denuncia, upload_file)
            fiscalizacao = Fiscalizacao(id_denuncia, nome_fiscal, local, bairro,
                                        cidade, estado, upload_file, latitude, longitude)

            if st.button("Cadastrar fiscalização"):
                fiscalizacao.update_data_denuncia()
                fiscalizacao.update_database()
                st.success("Cadastro de Fiscalização realizado com sucesso!")

                # verifica distancia entre a foto da denuncia, pelo id, com a foto juntada pela fiscalizacao - maximo 500 metros
                ponto_fiscalizacao = (fiscalizacao.img_latitude, fiscalizacao.img_longitude)
                ponto_denuncia = get_lat_long_denuciante(id_denuncia)[0]
                max_meters = 500

                if are_points_close(*ponto_fiscalizacao, *ponto_denuncia, max_meters):
                    st.success("Foto juntada pela fiscalização corresponde à área da foto juntada pela denúncia")

                    if "Sem" in fiscalizacao.img_classificacao:
                        st.success("Fiscalização validada")
                        update_status_denunciantes_by_id(id_denuncia, "Demanda Analisada e Baixada")
                        st.success("Cadastro bem sucedido. Demanda Finalizada")

                    else:
                        st.error(F"Foto classificada como {fiscalizacao.img_classificacao}")
                        st.error("Fiscalização não foi validada pelo sistema")

                else:
                    st.write(
                        "A foto juntada pela fiscalização não corresponde com a área da foto juntada pela denúncia")


    else:
        st.error("A senha que você inseriu está incorreta. Tente novamente.")
