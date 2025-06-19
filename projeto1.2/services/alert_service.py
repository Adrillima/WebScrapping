# services/alert_service.py

import smtplib
from email.message import EmailMessage
from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_SMTP, EMAIL_PORT


def enviar_alerta(destinatario, nome_produto, url, preco_atual, preco_desejado):
    try:
        msg = EmailMessage()
        msg['Subject'] = f"[Alerta de Preço] {nome_produto} agora custa R$ {preco_atual:.2f}"
        msg['From'] = EMAIL_SENDER
        msg['To'] = destinatario

        corpo = f"""
            O preço de '{nome_produto}' caiu!

        Preço atual: R$ {preco_atual:.2f}
        Preço desejado: R$ {preco_desejado:.2f}

        Veja o produto aqui: {url}

        Este é um alerta automático do seu sistema de monitoramento de preços.
        """

        msg.set_content(corpo)

        with smtplib.SMTP_SSL(EMAIL_SMTP, EMAIL_PORT) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print(f"[OK] Alerta enviado para {destinatario}")
        return True

    except Exception as e:
        print(f"[ERRO] Falha ao enviar e-mail: {e}")
        return False
