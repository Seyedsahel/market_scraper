import json
from datetime import datetime

def json_writer(main_product):
    now = datetime.utcnow()

    
    try:
        with open("products.json", mode='r', encoding='utf-8') as json_file:
            products = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        products = []  

    product = {}
    if "non_perfume_feature" in main_product:    
        product = {
            "group": [],
            "shares": [],
            "createdBy": "",
            "createdAt": {"$date": str(now)},
            "title": main_product['titleFa'],
            "shipRatio": 3,
            "titleEn": main_product['titleEn'],
            "description": main_product['des'],
            "images": main_product['img'], 
            "category": [],  
            "slug": main_product["titleEn"],
            "specifications": [
                {"keyFa": "ویژگی :", "valueFa": feature} for feature in main_product["non_perfume_feature"]
            ] + [
                {"keyFa": key, "valueFa": value} for key, value in main_product["non_perfume_dict_feature"].items()
            ],
            "productItems": [
                {
                    "price": (main_product['price']),
                    "discount": 0,
                    "isDefault": False,
                    "tax": 0,
                    "status": "marketable",
                    "variations": [],
                    "_id": "",
                    "createdBy": "6663f1229852d521309b7b84",
                    "createdAt": {"$date": str(now)},
                    "sku": "",
                    "product": "",
                    "qty": 0,
                    "perOrderQty": 1
                }
            ],
            "version": 3,
            "updatedAt": {"$date": str(now)},
            "updatedBy": "6663f1229852d521309b7b84",
            "token": "0830OO0I01",
            "__asal": True,
            "published": False,
            "isPublishForTorob": False
        }

        products.append(product)

    elif "perfume_feature" in main_product:
        product = {
            "group": [],
            "shares": [],
            "createdBy": "",
            "createdAt": {"$date": str(now)},
            "title": main_product['titleFa'],
            "shipRatio": 3,
            "titleEn": main_product['titleEn'],
            "description": main_product['des'],
            "images": main_product['img'], 
            "category": [],  
            "slug": main_product["titleEn"],
            "specifications": [{"keyFa": key, "valueFa": value} for key, value in main_product["perfume_feature"].items()],
            "productItems": [
                {
                    "price": (main_product['price']),
                    "discount": 0,
                    "isDefault": False,
                    "tax": 0,
                    "status": "marketable",
                    "variations": [],
                    "_id": "",
                    "createdBy": "6663f1229852d521309b7b84",
                    "createdAt": {"$date": str(now)},
                    "sku": "",
                    "product": "",
                    "qty": 0,
                    "perOrderQty": 1
                }
            ],
            "version": 3,
            "updatedAt": {"$date": str(now)},
            "updatedBy": "6663f1229852d521309b7b84",
            "token": "0830OO0I01",
            "__asal": True,
            "published": False,
            "isPublishForTorob": False
        }
        products.append(product)

    
    with open("products.json", mode='w', encoding='utf-8') as json_file:
        json.dump(products, json_file, ensure_ascii=False, indent=4)
