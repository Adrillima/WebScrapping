# scraper/product_scraper.py
# Requisitos adicionais

'''
Para o Selenium funcionar com Chrome headless, instale o driver:

pip install selenium

Instale o ChromeDriver compatível com sua versão do Chrome e adicione ao PATH, ou configure o caminho explicitamente em webdriver.Chrome(executable_path="CAMINHO").
'''

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import re
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/114.0.0.0 Safari/537.36'
}

def extrair_preco_com_bs4(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        texto = soup.get_text()
        precos = re.findall(r'R?\$ ?\d{1,3}(?:\.\d{3})*,\d{2}', texto)

        if precos:
            preco_raw = precos[0]
            preco_float = float(preco_raw.replace("R$", "").replace(".", "").replace(",", ".").strip())
            return preco_float
        else:
            print("[BS4] Nenhum preço encontrado.")
            return None
    except Exception as e:
        print(f"[BS4] Erro ao extrair preço de {url}: {e}")
        return None

def extrair_preco_com_selenium(url):
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')

        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(5)  # aguarda carregar JS

        texto = driver.find_element(By.TAG_NAME, 'body').text
        driver.quit()

        precos = re.findall(r'R?\$ ?\d{1,3}(?:\.\d{3})*,\d{2}', texto)

        if precos:
            preco_raw = precos[0]
            preco_float = float(preco_raw.replace("R$", "").replace(".", "").replace(",", ".").strip())
            return preco_float
        else:
            print("[SELENIUM] Nenhum preço encontrado.")
            return None
    except WebDriverException as e:
        print(f"[SELENIUM] Erro no WebDriver: {e}")
        return None
    except Exception as e:
        print(f"[SELENIUM] Erro ao extrair preço: {e}")
        return None

def obter_preco_produto(url):
    preco = extrair_preco_com_bs4(url)
    if preco is not None:
        print(f"[OK] Preço encontrado com BeautifulSoup: R$ {preco:.2f}")
        return preco

    print("[INFO] Tentando com Selenium...")
    preco = extrair_preco_com_selenium(url)
    if preco is not None:
        print(f"[OK] Preço encontrado com Selenium: R$ {preco:.2f}")
        return preco

    print(f"[ERRO] Não foi possível extrair o preço de: {url}")
    return None
