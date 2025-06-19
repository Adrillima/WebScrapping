# models/product.py

class Product:
    def __init__(self, id, nome, url, preco_desejado, frequencia_horas, categoria=None):
        self.id = id
        self.nome = nome
        self.url = url
        self.preco_desejado = preco_desejado
        self.frequencia_horas = frequencia_horas
        self.categoria = categoria
