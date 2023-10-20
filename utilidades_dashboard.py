import streamlit as st
import matplotlib.pyplot as plt

def plot_denuncias(df):
    # Contando o total de denúncias
    total_denuncias = df.shape[0]

    # Filtrando denúncias que estão em aberto
    denuncias_em_aberto = df.query("status == 'Em análise'").shape[0]

    # Valores para o eixo Y
    y_values = [total_denuncias, denuncias_em_aberto]

    # Criando o gráfico de barras
    fig, ax = plt.subplots(figsize=(8, 6))

    cores_sobrias = ['#2c3e50', '#5a7d9a']

    ax.bar(['Total de Denúncias', 'Denúncias em Aberto'], y_values, color=cores_sobrias)
    ax.set_title('Denúncias Cadastradas vs Denúncias em Aberto')
    ax.set_ylabel('Número de Denúncias')

    # Mostrando o gráfico no Streamlit
    st.pyplot(fig)


def plot_tipo_denuncias(df):
    # Contando o total de denúncias por tipo
    qtd_tipo = df["tipo"].value_counts()

    # Criando o gráfico de barras
    fig, ax = plt.subplots(figsize=(8, 6))

    # Usando os índices (tipos de denúncias) e valores (quantidades) da série qtd_tipo
    ax.bar(qtd_tipo.index, qtd_tipo.values, color='#5a7d9a')
    ax.set_title('Qtd de Denúncias por Tipo')
    ax.set_ylabel('Número de Denúncias')
    ax.set_xlabel('Tipo de Denúncia')

    # Rotacionando os rótulos do eixo X para melhor visualização
    plt.xticks(rotation=45, ha="right")

    # Mostrando o gráfico no Streamlit
    st.pyplot(fig)


def menu_cidades(df):
    opcao= st.selectbox("Escolha uma cidade", ["Todas", "Canguaretama", "Vila Flor", "Pedro Velho",
                                       "Baía Formosa"])

    st.markdown("""<br><br>""", unsafe_allow_html=True)

    if opcao == "Todas":
        return df

    elif opcao == "Canguaretama":
        df = df.query("cidade == 'Canguaretama'")
        return df

    elif opcao == "Vila Flor":
        df = df.query("cidade == 'Vila Flor'")
        return df

    elif opcao == "Pedro Velho":
        df = df.query("cidade == 'Pedro Velho'")
        return df

    elif opcao == "Baía Formosa":
        df = df.query("cidade == 'Baía Formosa'")
        return df