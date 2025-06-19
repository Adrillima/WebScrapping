# models/price_history.py

class PriceHistory:
    def __init__(self, id, produto_id, preco, data):
        self.id = id
        self.produto_id = produto_id
        self.preco = preco
        self.data = data
