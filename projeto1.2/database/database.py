# database/database.py

import sqlite3
from datetime import datetime

DB_NAME = 'price_monitor.db'

def conectar():
    return sqlite3.connect(DB_NAME)

# criar um script que faça a 

def criar_tabelas(): # não está sendo executado
    conn = conectar() # excluir
    cursor = conn.cursor() # 

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            url TEXT NOT NULL,
            preco_desejado REAL NOT NULL,
            frequencia_horas INTEGER NOT NULL,
            categoria TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Historico_Precos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            preco REAL NOT NULL,
            data TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(produto_id) REFERENCES Produtos(id)
        )
    ''')

    conn.commit()
    conn.close()

#InserirProdutos
def inserir_produto(nome, url, preco_desejado, frequencia_horas, categoria=None):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Produtos (nome, url, preco_desejado, frequencia_horas, categoria)
        VALUES (?, ?, ?, ?, ?)
    ''', (nome, url, preco_desejado, frequencia_horas, categoria))
    conn.commit()
    conn.close()

#ListarProdutos
def listar_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Produtos')
    produtos = cursor.fetchall()
    conn.close()
    return produtos

#Inserir preço
def inserir_preco(produto_id, preco):
    conn = conectar()
    cursor = conn.cursor()
    data = datetime.now().isoformat(sep=' ', timespec='seconds')
    cursor.execute('''
        INSERT INTO Historico_Precos (produto_id, preco, data)
        VALUES (?, ?, ?)
    ''', (produto_id, preco, data))
    conn.commit()
    conn.close()

#ConsultarHistórico
def consultar_historico(produto_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT preco, data FROM Historico_Precos
        WHERE produto_id = ?
        ORDER BY data DESC
    ''', (produto_id,))
    historico = cursor.fetchall()
    conn.close()
    return historico