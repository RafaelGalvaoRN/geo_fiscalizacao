import streamlit as st
import sqlite3
import os
import pandas as pd



if "STREAMLIT_PASSWORD" in os.environ:
    password_from_env = os.environ.get("STREAMLIT_PASSWORD")
else:
    password_from_env = st.secrets["STREAMLIT_PASSWORD"]

# def is_authenticated(password):
#     return password == os.environ.get("STREAMLIT_PASSWORD1")
def is_authenticated(password):
    return password == password_from_env




def generate_login_block():
    block1 = st.empty()
    block2 = st.empty()
    block3 = st.empty()

    return block1, block2, block3

def clean_blocks(blocks):
    for block in blocks:
        block.empty()




def get_data():
    # Conexão com o banco de dados SQLite
    conn = sqlite3.connect('base_dados/cadastro.db')
    cursor = conn.cursor()

    result = None


    try:
        cursor.execute("SELECT id, tipo, local, bairro, cidade, estado, img_latitude, img_longitude, "
                       "img_classificacao, data_denuncia, img_byte, status FROM denunciantes")
        result = cursor.fetchall()

        # Obtendo os nomes das colunas e criando um DataFrame
        col_names = [description[0] for description in cursor.description]
        result = pd.DataFrame(result, columns=col_names)
        result = result.set_index('id')  # Definindo 'id' como índice


    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return False

    finally:
        # Sempre certifique-se de fechar a conexão com o banco de dados
        conn.close()
        return result



def trata_df(df, drop_column = False, rename_column = False, filter_status=False):

    #renomeia as colunas
    if rename_column:
        df = df.rename(columns={'tipo': 'Tipo de Denúncia', 'local': 'Logradouro',
                                "bairro": "Bairro", "cidade": "Cidade", "estado": "Estado",
                                "img_classificacao": "Classificação da Imagem", "data_denuncia": "Data da Denúncia",
                                "status": "Status", "img_latitude": "Latitude", "img_longitude": "Longitude"})

    if drop_column:
        #exclui do df a coluna img_byte
        df = df.drop(columns=["img_byte"])

    if filter_status and rename_column:
        #exclui do df as demandas baixadas
        filter = df["Status"] != "Demanda Analisada e Baixada"
        df = df[filter]

    elif filter_status:
        # exclui do df as demandas baixadas
        filter = df["status"] != "Demanda Analisada e Baixada"
        df = df[filter]


    return df


def delete_all_rows():
    try:
        # Estabelecendo a conexão com o banco de dados
        conn = sqlite3.connect('base_dados/cadastro.db')
        cursor = conn.cursor()

        # Executando o comando SQL para deletar todas as linhas
        cursor.execute("DELETE FROM denunciantes")

        # Confirmando as alterações
        conn.commit()

    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")

    finally:
        # Sempre certifique-se de fechar a conexão com o banco de dados
        conn.close()


def delete_row_by_id(row_id):
    try:
        # Estabelecendo a conexão com o banco de dados
        conn = sqlite3.connect('base_dados/cadastro.db')
        cursor = conn.cursor()

        # Executando o comando SQL para deletar a linha com o ID especificado
        cursor.execute("DELETE FROM denunciantes WHERE id=?", (row_id,))

        # Confirmando as alterações
        conn.commit()

    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")

    finally:
        # Sempre certifique-se de fechar a conexão com o banco de dados
        conn.close()