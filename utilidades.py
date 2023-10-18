from PIL.ExifTags import GPSTAGS
from datetime import datetime
import hashlib
import sqlite3
import streamlit as st
import re
from classificador_lixo import model, transform
from ml import predict_image_lixo
from utilidades_login import haversine_distance, are_points_close
from rich import print


def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging


def get_exif_data(image_path):
    date = "Unknown"
    geotagging = "Unknown"

    image = Image.open(image_path)
    image.verify()
    exif_data = image._getexif()
    if exif_data is not None:
        for (tag, value) in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == "DateTime":
                date = value
            if tag_name == "GPSInfo":
                geotagging = get_geotagging(exif_data)
    return date, geotagging



from PIL import Image
from PIL.ExifTags import TAGS

def display_exif_data(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()
    if exif_data is not None:
        for (tag, value) in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            print(f"{tag_name:25}: {value}")
    else:
        print("No EXIF data found.")



class Denuncia():
    def __init__(self, tipo, nome, local, bairro, cidade, estado, telefone, email):
        self.tipo = tipo
        self.nome = nome
        self.local = local
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.telefone = telefone
        self.email = email
        self.img_byte = None
        self.img_hash = None
        self.img_latitude = None
        self.img_longitude = None
        self.img_classificacao = None
        self.data_denuncia = None
        self.ip_denunciante = None
        self.status = "Em análise"

    def set_image_bytes(self, img_bytes):
        self.img_byte = img_bytes

    def calculate_image_hash(self):
        if self.img_byte:
            # Calcular o hash da imagem (exemplo usando hashlib e SHA-256)
            hash_object = hashlib.sha256(self.img_byte)
            self.img_hash = hash_object.hexdigest()

    def update_data_denuncia(self):
        self.data_denuncia = datetime.today()

    def update_database(self):
        # Conectar ao banco de dados SQLite (substitua 'my_database.db' pelo nome do seu arquivo de banco de dados)
        conn = sqlite3.connect('base_dados/cadastro.db')
        cursor = conn.cursor()

        # Verificar se a tabela 'denuncias' existe; se não, você deve criá-la primeiro

        # Inserir ou atualizar um registro na tabela com base no nome (ou outro campo exclusivo)
        cursor.execute('''
               INSERT OR REPLACE INTO denunciantes (tipo, nome, local, bairro, cidade, estado, telefone, email, img_byte, img_hash, img_latitude, img_longitude, img_classificacao, data_denuncia, status, ip_denunciante)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
           ''', (self.tipo, self.nome, self.local, self.bairro, self.cidade, self.estado, self.telefone, self.email, self.img_byte,
                 self.img_hash, self.img_latitude, self.img_longitude, self.img_classificacao , self.data_denuncia, self.status ,self.ip_denunciante))

        # Commit e fechar a conexão com o banco de dados
        conn.commit()
        conn.close()

    def valida_telefone(self):
        # Defina uma expressão regular para um número de telefone válido
        # Este exemplo assume um formato de telefone com 8 ou 9 dígitos
        # e os dígitos podem estar separados por espaços, traços ou nada.
        padrao_telefone = r"^\d{8,9}$"

        if not re.match(padrao_telefone, self.telefone):
            return False  # Retorna False se o telefone não for válido

        return True  # Retorna True se o telefone for válido


    def valida_email(self):
        # Defina uma expressão regular para um email válido
        padrao_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        if not re.match(padrao_email, self.email):
            return False  # Retorna False se o telefone não for válido

        return True  # Retorna True se o telefone for válido

    def valida_cadastro(self):
        erro_validacao = False  # Inicialmente, não há erro

        if self.nome is None or self.nome == "":
            st.error("Nome não pode ser vazio")
            erro_validacao = True  # Marca que ocorreu um erro


        elif self.local is None or self.local == "":
            st.error("Local da denúncia não informado")
            erro_validacao = True  # Marca que ocorreu um erro

        elif self.bairro is None or self.bairro == "":
            st.error("Bairro da denúncia não informado")
            erro_validacao = True  # Marca que ocorreu um erro

        elif self.cidade is None or self.cidade == "":
            st.error("Cidade da denúncia não informado")
            erro_validacao = True  # Marca que ocorreu um erro

        elif self.estado is None or self.estado == "":
            st.error("Estado da denúncia não informado")
            erro_validacao = True  # Marca que ocorreu um erro

        elif self.telefone is None or self.telefone == "":
            st.error("Telefone do denunciante não informado")
            erro_validacao = True  # Marca que ocorreu um erro

        elif not self.valida_telefone():
            st.error("Telefone do denunciante não é válido")
            erro_validacao = True  # Marca que ocorreu um erro


        elif self.email is None or self.email == "":
            st.error("Email do denunciante não informado")
            erro_validacao = True  # Marca que ocorreu um erro


        elif not self.valida_email():
            st.error("Email não é válido")
            erro_validacao = True  # Marca que ocorreu um erro


        elif self.img_byte is None or self.img_byte == "":
            st.error("Foto não informada")
            erro_validacao = True  # Marca que ocorreu um erro

        elif not self.valida_img_byte():
            st.error("Foto já constante no banco de dados")
            erro_validacao = True  # Marca que ocorreu um erro

        elif self.img_hash is None or self.img_hash == "":
            st.error("Não foi possível verificar o hash da foto")
            erro_validacao = True  # Marca que ocorreu um erro

        elif not self.valida_img_hash():
            st.error("Foto já constante no banco de dados (Hash)")
            erro_validacao = True  # Marca que ocorreu um erro

        return erro_validacao

    def valida_img_hash(self):
        # Conexão com o banco de dados SQLite
        conn = sqlite3.connect('base_dados/cadastro.db')
        cursor = conn.cursor()

        try:
            # Procura a imagem pelo hash no banco de dados
            cursor.execute("SELECT * FROM denunciantes WHERE img_hash = ?", (self.img_hash,))
            result = cursor.fetchone()

            # Se 'result' não for None, uma imagem com o mesmo hash já existe
            if result is not None:
                return False
            else:
                return True

        except sqlite3.Error as e:
            print(f"Erro ao acessar o banco de dados: {e}")
            return False

        finally:
            # Sempre certifique-se de fechar a conexão com o banco de dados
            conn.close()

    def valida_img_byte(self):
        # Conexão com o banco de dados SQLite
        conn = sqlite3.connect('base_dados/cadastro.db')
        cursor = conn.cursor()

        try:
            # Procura a imagem pelo hash no banco de dados
            cursor.execute("SELECT * FROM denunciantes WHERE img_hash = ?", (self.img_byte,))
            result = cursor.fetchone()

            # Se 'result' não for None, uma imagem com o mesmo hash já existe
            if result is not None:
                return False
            else:
                return True

        except sqlite3.Error as e:
            print(f"Erro ao acessar o banco de dados: {e}")
            return False

        finally:
            conn.close()

    def valida_img_distance(self):
        erro_validacao = False

        if self.cidade not in ["Canguaretama", "Vila Flor", "Pedro Velho", "Baía Formosa"]:
            st.error("Cidade não abrangida pelo sistema")
            erro_validacao = True  # Marca que ocorreu um erro


        elif self.cidade == "Canguaretama":
            print('entrei aqui ')
            lat = -6.38285
            long = -35.1249

        elif self.cidade == "Vila Flor":
            lat = -6.31287
            long = -35.067

        elif self.cidade == "Pedro Velho":
            lat = -6.43969
            long = -35.2219

        elif self.cidade == "Baía Formosa":
            lat = -6.37124
            long = -35.00528



        if not are_points_close(self.img_latitude, self.img_longitude, lat, long, 30000):
            st.error("Área da foto/denunciante além dos limites territoriais do sistema")
            erro_validacao = True

        return erro_validacao

    def valida_qtd_denuncias(self, numero):
        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect('base_dados/cadastro.db')
        cursor = conn.cursor()

        # Obtenha a data atual para filtrar as denúncias do dia
        data_atual = datetime.now().strftime('%Y-%m-%d')

        # Consulta para contar quantas denúncias foram feitas pelo IP no dia atual
        cursor.execute('''
            SELECT COUNT(*)
            FROM denunciantes
            WHERE ip_denunciante = ? AND date(data_denuncia) = ?
        ''', (self.ip_denunciante, data_atual))

        # Obtém o resultado da consulta
        count = cursor.fetchone()[0]

        # Fecha a conexão com o banco de dados
        conn.close()

        # Verifica a condição e retorna True ou False
        if count >= numero:
            st.error("Quantidade de denúncias ultrapassadas")
            return False
        else:
            return True



class Fiscalizacao(Denuncia):
    def __init__(self, id_denuncia, nome, local, bairro, cidade, estado, uploaded_file, latitude, longitude):
        self.id_denuncia = id_denuncia
        self.nome = nome
        self.local = local
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.foto = uploaded_file

        self.img_byte = None  # Inicialização padrão
        self.img_hash = None

        if uploaded_file:
            self.set_image_bytes(uploaded_file.getbuffer())
            self.calculate_image_hash()

            with open("temp_img.jpg", "wb") as f:
                f.write(uploaded_file.getbuffer())

            class_idx = predict_image_lixo("temp_img.jpg", model, transform)
            classes = ['Lixo', 'Sem Lixo']
            self.img_classificacao = classes[class_idx]

            # Se o método update_data_denuncia for necessário
            self.data_denuncia = self.update_data_denuncia()

        self.img_latitude = latitude
        self.img_longitude = longitude

    def update_database(self):
        # Conectar ao banco de dados SQLite (substitua 'my_database.db' pelo nome do seu arquivo de banco de dados)
        conn = sqlite3.connect('base_dados/cadastro.db')
        cursor = conn.cursor()

        # Verificar se a tabela 'denuncias' existe; se não, você deve criá-la primeiro

        # Inserir ou atualizar um registro na tabela com base no nome (ou outro campo exclusivo)
        cursor.execute('''
               INSERT OR REPLACE INTO fiscalizacao (id_denuncia, nome, local, bairro, cidade, estado, img_byte, img_hash,
                img_latitude, img_longitude, img_classificacao, data_fiscalizacao)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
           ''', (self.id_denuncia, self.nome, self.local, self.bairro, self.cidade, self.estado, self.img_byte,
                 self.img_hash, self.img_latitude, self.img_longitude, self.img_classificacao , self.data_denuncia))

        # Commit e fechar a conexão com o banco de dados
        conn.commit()
        conn.close()



from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx


def get_remote_ip() -> str:
    """Get remote ip."""
    try:
        ctx = get_script_run_ctx()
        if ctx is None:
            return None

        session_info = runtime.get_instance().get_client(ctx.session_id)
        if session_info is None:
            return None
    except Exception as e:
        return None
    return session_info.request.remote_ip


