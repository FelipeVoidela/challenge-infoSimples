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
    sku = {}

    # name
    name = card.select_one('meta[itemprop="name"]')
    name = name.get('content')
    #skus.append(name)
    sku['name'] = name


    # current price
    current_price = card.select_one('.prod-pnow')
    if current_price:
        match = re.search(r'[\d.,]+', current_price.get_text())
        if match:
            priceNow = float(match.group(0).replace(',', '.'))
            #skus.append(f"Preco atual: R$ {priceNow}")
            sku['current price'] = priceNow
    else:
        #skus.append(None)
        sku['current price'] = None


     # old price
    old_price = card.select_one('.prod-pold')
    if old_price:
        match = re.search(r'[\d.,]+', old_price.get_text())
        if match:
            priceOld = float(match.group(0).replace(',', '.'))
            #skus.append(f"Preco antigo: R$ {priceOld}")
            sku['old price'] = priceOld
    else:
        #skus.append(None)
        sku['old price'] = None

    # available
    not_available = 'not-avaliable'

    if  not_available in card.get('class'):
        #skus.append(None)
        sku['available'] = None
    else:
        #skus.append(True)
        sku['available'] = True

    skus.append(sku)
resposta_final['skus'] = skus

# properties
product_properties = parsed_html.select('table.pure-table.pure-table-bordered')

# pega primeira tabela div(sem nome)
product_properties_table = product_properties[0]

properties = []

# percorre cada linha que contenha a tag tr
for row in product_properties_table.find_all('tr'):
    propertie = {}

    # encontra colunas que contenham a tag td
    find_td = row.find_all('td')
   
    label_element = find_td[0].find('b') # valor label esta em tag b dentro da primeira tag td
    value_element = find_td[1]  # O value esta em td

   
    label_txt = label_element.get_text()
    value_txt = value_element.get_text()

    propertie['label'] = label_txt
    propertie['value'] = value_txt

    properties.append(propertie)

resposta_final['properties'] = properties

# reviews
reviews_comments = parsed_html.select('#comments .analisebox')
reviews = []

for review_comment in reviews_comments:
    review = {}

    # name
    name = review_comment.select_one('.analiseusername')
    review['name'] = name.get_text()

    # date
    date = review_comment.select_one('.analisedate')
    review['date'] = date.get_text()

    # score
    score = review_comment.select_one('.analisestars')
    star_count = score.get_text().count('★')
    review['score'] = star_count

    # text
    text = review_comment.select_one('p')
    review['text'] = text.get_text() 
    
    reviews.append(review)
resposta_final['reviews'] = reviews



















































# Gera string JSON com a resposta final
json_resposta_final = json.dumps(resposta_final, indent=2)

# Salva o arquivo JSON com a resposta final
with open('produto.json', 'w') as arquivo_json:
 arquivo_json.write(json_resposta_final)