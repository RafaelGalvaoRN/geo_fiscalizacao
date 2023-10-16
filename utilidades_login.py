import streamlit as st
import sqlite3
import pandas as pd
import folium
import base64
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calcula a distância em metros entre dois pontos (latitude e longitude) usando a fórmula de Haversine.
    """
    R = 6371000  # raio da Terra em metros

    # Converte graus decimais para radianos
    lat1, lon1, lat2, lon2 = map(math.radians, [float(lat1), float(lon1), float(lat2), float(lon2)])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

def are_points_close(lat1, lon1, lat2, lon2, max_distance=500):
    """
    Verifica se dois pontos (latitude e longitude) estão a uma distância máxima especificada (em metros).
    """
    distance = haversine_distance(lat1, lon1, lat2, lon2)
    return distance <= max_distance




def is_authenticated(password):
    return password == "123"

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
    conn = sqlite3.connect(r'C:\Users\User\PycharmProjects\pythonProject4\base_dados\cadastro.db')
    cursor = conn.cursor()

    result = None


    try:
        cursor.execute("SELECT tipo, local, bairro, cidade, estado, img_latitude, img_longitude, "
                       "img_classificacao, data_denuncia, img_byte, status FROM denunciantes")
        result = cursor.fetchall()

        # Obtendo os nomes das colunas e criando um DataFrame
        col_names = [description[0] for description in cursor.description]
        result = pd.DataFrame(result, columns=col_names)

    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return False

    finally:
        # Sempre certifique-se de fechar a conexão com o banco de dados
        conn.close()
        return result


def plot_denuncias_map(df):
    m = folium.Map(location=[-6.38139, -35.1281], zoom_start=12)

    for _, denuncia in df.iterrows():
        if 'img_latitude' in denuncia and 'img_longitude' in denuncia:
            # Convertendo bytes para base64
            img_bytes = denuncia['img_byte']
            img_b64 = base64.b64encode(img_bytes).decode()

            # Criando HTML para o popup
            html = f"""
            <h1>{denuncia['tipo']}</h1>
            <p>{denuncia['data_denuncia']}</p>
            <img src="data:image/jpeg;base64,{img_b64}" alt="Denuncia img" width="300">
            """

            # Criando popup com HTML
            popup = folium.Popup(html, max_width=400)

            # Criando e adicionando o marcador ao mapa
            folium.Marker(
                location=[denuncia['img_latitude'], denuncia['img_longitude']],
                popup=popup,
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(m)

    return m


def get_lat_long_denuciante(id):
    # Conexão com o banco de dados SQLite
    conn = sqlite3.connect(r'C:\Users\User\PycharmProjects\pythonProject4\base_dados\cadastro.db')
    cursor = conn.cursor()

    result = None

    try:
        cursor.execute("SELECT img_latitude, img_longitude "
                       "FROM denunciantes WHERE id == ?", (id,))

        result = cursor.fetchall()


    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return False

    finally:
        # Sempre certifique-se de fechar a conexão com o banco de dados
        conn.close()
        return result


def update_status_denunciantes_by_id(id, new_status):
    # Conexão com o banco de dados SQLite
    conn = sqlite3.connect(r'C:\Users\User\PycharmProjects\pythonProject4\base_dados\cadastro.db')
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE denunciantes SET status = ? WHERE id == ?", (new_status, id))
        conn.commit()  # Commit das alterações ao banco de dados

    except sqlite3.Error as e:
        print(f"Erro ao atualizar o banco de dados: {e}")
        return False

    finally:
        # Sempre certifique-se de fechar a conexão com o banco de dados
        conn.close()

    return True  # Retorne True para indicar sucesso na atualização