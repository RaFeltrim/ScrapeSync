import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin, urlparse

# URL da página que você deseja fazer o scraping
url = "https://www.cnnbrasil.com.br"

# Faz uma requisição para a página com um cabeçalho de usuário simulado
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# Validate the URL
try:
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        raise ValueError("Invalid URL")
except ValueError as e:
    print(f"Error: Invalid URL ({e})")
    exit()

# Make the HTTP request
try:
    response = requests.get(url, headers=headers, timeout=10)
except requests.exceptions.RequestException as e:
    print(f"Error: Failed to make HTTP request ({e})")
    exit()

# Handle different types of errors
if response.status_code != 200:
    print(f"Error: Failed to get HTTP response (status code: {response.status_code})")
    exit()

# Cria um objeto BeautifulSoup para fazer o parsing do HTML usando html.parser
soup = BeautifulSoup(response.text, 'html.parser')

# Extrai todos os links que contêm a palavra "noticia" no href
links_noticia = soup.find_all('a', href=True, attrs={'href': lambda href: 'noticia' in href.lower()})

# Cria um DataFrame do pandas
df = pd.DataFrame(columns=['Nome da Notícia', 'Link da Matéria'])

# Itera sobre os links e adiciona ao DataFrame
for link in links_noticia:
    nome_noticia = link.get_text(strip=True)
    link_noticia = urljoin(url, link.get('href'))
    df = pd.concat([df, pd.DataFrame({'Nome da Notícia': [nome_noticia], 'Link da Matéria': [link_noticia]})], ignore_index=True)

# Salva o DataFrame como um arquivo CSV
df.to_csv('noticias.csv', index=False, encoding='utf-8-sig')
