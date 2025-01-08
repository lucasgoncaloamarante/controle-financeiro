import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from email_validator import validate_email, EmailNotValidError
import os

# Carregar variáveis do .env
load_dotenv()

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
RESET_PASSWORD_URL = os.getenv("RESET_PASSWORD_URL", "http://localhost:3000/reset-password")

def send_password_reset_email(to_email: str, token: str):
    from_email = SMTP_EMAIL
    subject = "Redefinição de Senha"
    body = f"""
Olá,

Você solicitou a redefinição de senha. Clique no link abaixo para redefinir sua senha:

{RESET_PASSWORD_URL}?token={token}

Se você não solicitou a redefinição, ignore este e-mail.

Este link é válido por 1 hora.
"""

    # Criar a mensagem de e-mail
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Enviar o e-mail usando o servidor SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)  # Informações do servidor de e-mail
            server.sendmail(from_email, to_email, msg.as_string())
        print("E-mail enviado com sucesso para:", to_email)
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

def send_email_verification(email: str, verification_link: str):
    try:
        # Validando o e-mail do destinatário
        validate_email(email)
        
        # Configuração da mensagem
        from_email = SMTP_EMAIL
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = email
        msg['Subject'] = "Verificação de E-mail"

        body = f"""
        Olá,

        Clique no link abaixo para verificar seu e-mail:

        {verification_link}

        Caso não tenha solicitado a verificação, ignore este e-mail.

        Atenciosamente,
        Sua Equipe
        """
        msg.attach(MIMEText(body, 'plain'))

        # Conectando ao servidor SMTP e enviando o e-mail
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)  # Informações do servidor de e-mail
            server.sendmail(from_email, email, msg.as_string())

        print("E-mail de verificação enviado com sucesso!")

    except EmailNotValidError as e:
        print(f"Erro de e-mail inválido: {e}")
    except Exception as e:
        print(f"Ocorreu um erro ao enviar o e-mail: {e}")
