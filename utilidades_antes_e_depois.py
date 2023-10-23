import sqlite3



def get_images():
    # Conexão com o banco de dados SQLite
    conn = sqlite3.connect('base_dados/cadastro.db')
    cursor = conn.cursor()

    result = None

    try:
        cursor.execute("SELECT fiscalizacao.img_byte AS img_byte_fiscalizacao, denunciantes.img_byte AS img_byte_denunciantes "
                       "FROM fiscalizacao "
                       "JOIN denunciantes ON fiscalizacao.id_denuncia = denunciantes.id")
        result = cursor.fetchall()

    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return False

    finally:
        # Sempre certifique-se de fechar a conexão com o banco de dados
        conn.close()

    return result


