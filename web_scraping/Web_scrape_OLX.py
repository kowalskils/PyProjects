#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

url = 'https://www.olx.pt/ads/q-dell-xps-gtx-1050/?search%5Bdescription%5D=1'
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}

r = requests.get(url, headers=headers)

# make sure that the page exists and responds ok
if r.status_code == 200:
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('h1')
    if title is not None:
        title_text = title.text.strip()

# Find the objects
products = soup.find_all('h3', {'class': 'lheight22 margintop5'})
prices = soup.find_all('p', {'class': 'price'})
locations = soup.find_all('p', {'class': 'lheight16'})


# Create multiple empty vars
product, price, location = [None] * 3

# Create multiple empty list
lst_prices, lst_products, lst_locations = [[] for i in range(3)]

# Assign values to the list
for location in locations:
    try:
        lst_locations.append(location.find('span').text.strip())
    except Exception:
        pass


for product in products:
    lst_products.append(product.find('strong').text)


for price in prices:
    lst_prices.append(price.find('strong').text)

# Print formatted values
for a, b, c in list(zip(lst_products, lst_prices, lst_locations)):
    print(f'Product Name:{a}\nPrice: {b}\nLocations: {c}\n\n')
