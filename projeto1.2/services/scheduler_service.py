# services/scheduler_service.py

from apscheduler.schedulers.background import BackgroundScheduler
from scraper.product_scraper import obter_preco_produto
from database.database import listar_produtos, inserir_preco
from services.alert_service import enviar_alerta
from config import ALERT_EMAIL_DESTINATARIO
import time

scheduler = BackgroundScheduler()

def verificar_preco(produto):
    produto_id, nome, url, preco_desejado, frequencia_horas, categoria = produto

    print(f"[VERIFICAÇÃO] Produto: {nome}")
    preco_atual = obter_preco_produto(url)

    if preco_atual:
        inserir_preco(produto_id, preco_atual)
        print(f"[OK] Preço registrado: R$ {preco_atual:.2f}")

        if preco_atual <= preco_desejado:
            enviar_alerta(
                destinatario=ALERT_EMAIL_DESTINATARIO,
                nome_produto=nome,
                url=url,
                preco_atual=preco_atual,
                preco_desejado=preco_desejado
            )

def iniciar_agendador():
    produtos = listar_produtos()
    if not produtos:
        print("[INFO] Nenhum produto cadastrado para monitorar.")
        return

    for produto in produtos:
        produto_id, nome, url, preco_desejado, frequencia_horas, categoria = produto
        job_id = f"verificar_{produto_id}"

        scheduler.add_job(
            verificar_preco,
            trigger='interval',
            hours=frequencia_horas,
            id=job_id,
            args=[produto],
            replace_existing=True
        )
        print(f"[AGENDADO] {nome} a cada {frequencia_horas} hora(s)")

    scheduler.start()
    print("[AGENDADOR INICIADO] Verificações agendadas.")
