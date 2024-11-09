from product_urls import *
from product_info import *


def main():

    base_cats_links = {

        'cosmetic': 'https://asalbanooshop.com/product-category/cosmetic/',
    }

    products = product_urls(base_cats_links)
    # print(products)
    product_info(products)
    print("ok")


if __name__ == "__main__":
    main()

#  'cosmetic':'https://asalbanooshop.com/product-category/cosmetic/',
#        'hair-products':'https://asalbanooshop.com/product-category/hair-products',
#        'skin-products':'https://asalbanooshop.com/product-category/skin-products/',
# 'perfume':'https://asalbanooshop.com/product-category/perfume/',