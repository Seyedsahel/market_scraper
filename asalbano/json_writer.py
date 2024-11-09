import csv
import json
from datetime import datetime
import re

def csv_to_json(csv_file_path, json_file_path):
    
    products = []

    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            now = datetime.utcnow()
            # title,titleEn,price,des,feature,img,status,categories,url
            product = {
                "group": [],
                "shares": [],
                "createdBy": "",
                "createdAt": {"$date": now},
                "title": row['title'],
                "shipRatio": 3,
                "titleEn": row['titleEn'],
                "description": row['des'],
                "images": row['img'], 
                "category": [],  
                "slug": row['slug'].replace(" ", "-"),
                "status": "marketable",
                "specifications": [
                    {"keyFa": "ویژگی ها:", "valueFa": row['features']},
                    
                ],
                "productItems": [
                    {
                        "price": (extract_and_convert_price(row['price'])),
                        "discount": 0,
                        "isDefault": False,
                        "tax": 0,
                        "status": "marketable",
                        "variations": [],
                        "_id": {"$oid": row['product_id']},
                        "createdBy": "6663f1229852d521309b7b84",
                        "createdAt": {"$date": now},
                        "sku": row['sku'],
                        "product": row['product_id'],
                        "qty": 0,
                        "perOrderQty": 1
                    }
                ],
                "version": 3,
                "updatedAt": {"$date": "2024-11-05T15:08:34.550Z"},
                "updatedBy": "6663f1229852d521309b7b84",
                "token": "0830OO0I01",
                "__asal":True,
                "published": False,
                "isPublishForTorob": False
            }

            products.append(product)

    
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(products, json_file, ensure_ascii=False, indent=4)

def extract_and_convert_price(text):
    match = re.search(r'(\d{1,3}(?:,\d{3})*)', text)
    if match:
        number_str = match.group(1).replace(',', '')
        converted_number = int(number_str) * 10
        return converted_number
    return None


csv_to_json('products.csv', 'output.json')
