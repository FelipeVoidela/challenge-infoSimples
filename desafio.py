# Bibliotecas que nós instalamos manualmente
from bs4 import BeautifulSoup
import requests
import re

# Bibliotecas nativas do Python
import json

# URL do site
url = 'https://infosimples.com/vagas/desafio/commercia/product.html'

# Objeto contendo a resposta final
resposta_final = {}

# Faz o request
response = requests.get(url)

# Parse do responses
parsed_html = BeautifulSoup(response.content, 'html.parser')

# Vamos pegar o título do produto, na tag H2, com ID "product_title"
resposta_final['title'] = parsed_html.select_one('h2#product_title').get_text()

# Aqui você adiciona os outros campos...

# brand
resposta_final['brand'] = parsed_html.select_one('div.brand').get_text()

# categories
categories = []
header = parsed_html.select_one('ul.breadcrumb')
for li in header.select('li'):
    category_text = li.get_text()
    categories.append(category_text)
resposta_final['categories'] = categories

# description 
description = []
text = parsed_html.select_one('div.proddet')
for p in text.select('p'):
   description_text = p.get_text()
   description.append(description_text)
resposta_final['description'] = description

# skus
skus = []
cards = parsed_html.select('.skus-area .card')

for card in cards:

    # name
    name = card.select_one('meta[itemprop="name"]')
    name = name.get('content')
    skus.append(name)

    # current price
    current_price = card.select_one('.prod-pnow')
    if current_price:
        match = re.search(r'[\d.,]+', current_price.get_text())
        if match:
            priceNow = float(match.group(0).replace(',', '.'))
            skus.append(f"R$ {priceNow}")
    else:
        skus.append(None)

    


resposta_final['skus'] = skus









# Gera string JSON com a resposta final
json_resposta_final = json.dumps(resposta_final, indent=2)

# Salva o arquivo JSON com a resposta final
with open('produto.json', 'w') as arquivo_json:
 arquivo_json.write(json_resposta_final)