import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

async def send_reset_email(email: str, reset_token: str):
    """Отправка email для сброса пароля"""
    
    if not settings.smtp_username or not settings.smtp_password:
        print(f"Email sending disabled. Reset token for {email}: {reset_token}")
        return
    
    reset_url = f"http://localhost:8000/reset-password?token={reset_token}"
    
    message = MIMEMultipart()
    message["From"] = settings.from_email
    message["To"] = email
    message["Subject"] = "Сброс пароля - Medical App"
    
    body = f"""
    Здравствуйте!
    
    Вы запросили сброс пароля для вашего аккаунта в Medical App.
    
    Для сброса пароля перейдите по ссылке:
    {reset_url}
    
    Ссылка действительна в течение 1 часа.
    
    Если вы не запрашивали сброс пароля, проигнорируйте это письмо.
    
    С уважением,
    Команда Medical App
    """
    
    message.attach(MIMEText(body, "plain"))
    
    try:
        server = smtplib.SMTP(settings.smtp_server, settings.smtp_port)
        server.starttls()
        server.login(settings.smtp_username, settings.smtp_password)
        text = message.as_string()
        server.sendmail(settings.from_email, email, text)
        server.quit()
        print(f"Reset email sent to {email}")
    except Exception as e:
        print(f"Failed to send email to {email}: {e}")
        # В продакшене здесь должно быть логирование
        raise