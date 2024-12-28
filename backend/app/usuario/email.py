import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_password_reset_email(to_email: str, token: str):
    from_email = "budgetzy@gmail.com"
    subject = "Redefinição de Senha"
    body = f"Você solicitou a redefinição de senha. Use o seguinte token para redefinir sua senha: {token}\n\n" \
           f"Este token é válido por 1 hora."

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
            server.login("budgetzy@gmail.com", "")  # Informações do servidor de e-mail
            server.sendmail(from_email, to_email, msg.as_string())
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")
