from services.alert_service import enviar_alerta

enviar_alerta(
    destinatario='Email de teste!',
    nome_produto='Produto X',
    url='https://www.magazineluiza.com.br/purificador-de-agua-philco-pbe09-titanium-natural-gelada-bivolt/p/acahh2aaf4/ep/purf/',
    preco_atual=1999.90,
    preco_desejado=2000.00
)
