import requests, re
from bs4 import BeautifulSoup

site = requests.get('http://www.agroplazma.com')
site.encoding = site.apparent_encoding
html = BeautifulSoup(site.text, 'html.parser')

text = re.sub(r'\s+', ' ',html.get_text())
print(text)