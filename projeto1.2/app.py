import time
from flask import Flask, render_template, request, redirect, url_for
from database.database import criar_tabelas, inserir_produto, listar_produtos, consultar_historico
from services.scheduler_service import iniciar_agendador
from scraper.product_scraper import obter_preco_produto
from datetime import datetime
from services.scheduler_service import iniciar_agendador
from database.database import criar_tabelas

app = Flask(__name__)

@app.route("/")
def index():
    produtos = listar_produtos()
    return render_template("index.html", produtos=produtos)

@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():
    if request.method == "POST":
        nome = request.form["nome"]
        url = request.form["url"]
        preco_desejado = float(request.form["preco_desejado"])
        frequencia = int(request.form["frequencia"])
        categoria = request.form.get("categoria", "")

        inserir_produto(nome, url, preco_desejado, frequencia, categoria)
        return redirect(url_for("index"))
    return render_template("adicionar.html")

@app.route("/produto/<int:produto_id>")
def detalhes(produto_id):
    historico = consultar_historico(produto_id)
    datas = [registro[0] for registro in historico]
    precos = [registro[1] for registro in historico]
    return render_template("detalhes.html", produto_id=produto_id, datas=datas, precos=precos)

@app.route("/alertas")
def alertas():
    produtos = listar_produtos()
    alertas = []
    for p in produtos:
        produto_id, nome, url, preco_desejado, freq, cat = p
        historico = consultar_historico(produto_id)
        if historico and historico[-1][1] <= preco_desejado:
            alertas.append((nome, url, historico[-1][1], preco_desejado))
    return render_template("alertas.html", alertas=alertas)

# if __name__ == "__main__":
#     criar_tabelas()
#     iniciar_agendador()
#     app.run(debug=True)

if __name__ == "__main__":
    criar_tabelas()
    iniciar_agendador()

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("\n[ENCERRADO] Scheduler interrompido.")