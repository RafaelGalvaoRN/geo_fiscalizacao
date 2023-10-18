
import sqlite3

def create_table():
    conn = sqlite3.connect(r'C:\Users\User\PycharmProjects\pythonProject4\base_dados\cadastro.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS denunciantes (
            id INTEGER PRIMARY KEY,
            tipo TEXT,
            nome TEXT,
            local TEXT,
            bairro TEXT, 
            cidade TEXT,
            estado TEXT, 
            telefone TEXT,
            email TEXT, 
            img_byte BLOB,
            img_hash BLOB, 
            img_latitude TEXT, 
            img_longitude TEXT,
            img_classificacao TEXT,
            data_denuncia DATE, 
            status TEXT   
                    
        )
    ''')

    # Step 4: Commit the changes and close the database connection
    conn.commit()
    conn.close()



def create_table_fiscalizacao():
    conn = sqlite3.connect(r'C:\Users\User\PycharmProjects\pythonProject4\base_dados\cadastro.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fiscalizacao (
            id INTEGER PRIMARY KEY,
            id_denuncia TEXT,
            nome TEXT,
            local TEXT,
            bairro TEXT, 
            cidade TEXT,
            estado TEXT, 
            img_byte BLOB,
            img_hash BLOB, 
            img_latitude TEXT, 
            img_longitude TEXT,
            img_classificacao TEXT,
            data_fiscalizacao DATE, 
            status TEXT,     
            FOREIGN KEY(id_denuncia) REFERENCES denunciantes(id)      
        )
    ''')

    # Step 4: Commit the changes and close the database connection
    conn.commit()
    conn.close()


def insert_table(id, tipo, nome, local, bairro, cidade, estado, telefone, email, img_byte, img_hash, img_latitude,
                 img_longitude, img_classificacao, data_denuncia, status):
    # Conexão com o banco de dados SQLite
    conn = sqlite3.connect(r'C:\Users\User\PycharmProjects\pythonProject4\base_dados\cadastro.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO denunciantes (
                id, tipo, nome, local, bairro, cidade, estado, 
                telefone, email, img_byte, img_hash, img_latitude, 
                img_longitude, img_classificacao, data_denuncia, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
        id, tipo, nome, local, bairro, cidade, estado, telefone, email, img_byte, img_hash, img_latitude, img_longitude,
        img_classificacao, data_denuncia, status))

        # Realiza commit das alterações e fecha a conexão com o banco de dados
        conn.commit()

    except sqlite3.Error as e:
        print(f"Erro ao inserir dados: {e}")

    finally:
        conn.close()


def alter_table_insert_column():
    conn = sqlite3.connect(r'C:\Users\User\PycharmProjects\pythonProject4\base_dados\cadastro.db')
    cursor = conn.cursor()
    cursor.execute('''
    ALTER TABLE denunciantes ADD ip_denunciante TEXT;
    ''')

    # Step 4: Commit the changes and close the database connection
    conn.commit()
    conn.close()

def limpar_tabela_denunciantes():
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(r'C:\Users\User\PycharmProjects\pythonProject4\base_dados\cadastro.db')
    cursor = conn.cursor()

    # Excluir todos os registros da tabela denunciantes
    cursor.execute('DELETE FROM denunciantes;')

    # Commitar as mudanças e fechar a conexão com o banco de dados
    conn.commit()
    conn.close()

def limpar_tabela_fiscalizacao():
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(r'C:\Users\User\PycharmProjects\pythonProject4\base_dados\cadastro.db')
    cursor = conn.cursor()

    # Excluir todos os registros da tabela denunciantes
    cursor.execute('DELETE FROM fiscalizacao;')

    # Commitar as mudanças e fechar a conexão com o banco de dados
    conn.commit()
    conn.close()

# create_table()
# insert_table(0, 'TipoExemplo', 'joao', 'BANANEIRAS', 'BANANEIRAS', 'BANANEIRAS', 'PARAIBA', '1111-2222', 'email@example.com', b'ImagemBytes', 'hashimagem',  -6.38285, -35.1249, 'ClassificacaoExemplo', '2023-10-13', "Em Análise")
# create_table_fiscalizacao()
# alter_table_insert_column()
