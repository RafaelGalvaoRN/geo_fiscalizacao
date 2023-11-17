import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import streamlit as st





if "STREAMLIT_EMAIL" in os.environ:
    password_from_env = os.environ.get("STREAMLIT_EMAIL")
else:
    password_from_env = st.secrets["STREAMLIT_EMAIL"]



def enviar_email(destinatario):
    # Informações do remetente
    remetente_email = "rafaelgalvaorn@hotmail.com"
    remetente_senha = password_from_env

    # Configurações do servidor SMTP
    # smtp_server = "smtp.gmail.com"
    smtp_server = "smtp-mail.outlook.com"
    port = 587  # Para SSL use 465, para TLS use 587

    # Criando a mensagem
    mensagem = MIMEMultipart("alternative")
    mensagem["Subject"] = "Aviso - Nova Denúncia - Geoambiental"
    mensagem["From"] = remetente_email
    mensagem["To"] = destinatario

    # Corpo do email
    texto = """
    Aviso - Nova Denúncia cadastrada no sistema Geoambiental!
    
    Favor acessar o sistema e analisar o registro de ilícito, enviando foto que comprove a remoção do dano ambiental
    
    Att. GeoAmbiental    
    """

    parte = MIMEText(texto, "plain")
    mensagem.attach(parte)

    # Enviando o email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  # Ativa a segurança
        server.login(remetente_email, remetente_senha)
        server.sendmail(remetente_email, destinatario, mensagem.as_string())
        print("Email enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
    finally:
        server.quit()


