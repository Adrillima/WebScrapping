from scraper.product_scraper import obter_preco_produto

url = 'https://www.magazineluiza.com.br/purificador-de-agua-philco-pbe09-titanium-natural-gelada-bivolt/p/acahh2aaf4/ep/purf/'  # coloque uma URL real
preco = obter_preco_produto(url)
print(f"Preço extraído: {preco}")
