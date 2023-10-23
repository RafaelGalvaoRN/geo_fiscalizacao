import streamlit as st
from utilidades_controle import (generate_login_block, clean_blocks,
                                 is_authenticated, get_data, trata_df, delete_all_rows,
                                 delete_row_by_id)
import os



st.set_page_config(layout="wide")  # Usa o layout mais largo disponível



password = st.text_input("Digite a senha:", type='password')
blocks = generate_login_block()

if password != "":
    if is_authenticated(password):
        clean_blocks(blocks)
        st.success("Autenticação realizada com sucesso!")
        data = get_data()
        print(data)
        print(type(data))

        data_tratado = trata_df(data, drop_column=True, rename_column=True, filter_status=True)

        st.title("Tabela Controle das Denúncias")
        st.table(data_tratado)



        linha = st.number_input("Escolha um id", step=1)

        if st.button("Deletar linha"):
            if linha:
                delete_row_by_id(linha)
            else:
                st.error("Escolha o id a ser deletado")

        if st.button("Deletar tabela"):
            delete_all_rows()





    else:
        st.error("Senha incorreta ou não foi possível autenticar.")