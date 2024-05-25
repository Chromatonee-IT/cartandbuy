import requests
from store.models import *

# fetch_data = requests.get('https://fakestoreapi.com/products/1')

# data = fetch_data.json()
# print(data)

payload = []
def data_fetch(n):
    for i in range(1,n):
        fetch_data = requests.get(f'https://dummyjson.com/products/{i}')
        data = fetch_data.json()
        
        id = data["id"]
        product_name = data["title"]
        product_description = data["description"]
        product_category = data["category"]
        product_price = int(data["price"])
        product_image = data["images"]
        rating = data["rating"]
        stock = data["stock"]
        brand = data["brand"]

        payload.append({
            "id": id,
            "name": product_name,
            "title": product_name,
            "description": product_description,
            "category": product_category,
            "price-old": product_price + 500,
            "price-new": product_price,
            "itm_isactive": True,
            "image": product_image,
            "rating": rating,
            "stock": stock,
            "brand": brand
        })
    return payload