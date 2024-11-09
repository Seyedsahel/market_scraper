from bs4 import BeautifulSoup
import requests
from csv_writer import *
from json_writer import *
from requests.exceptions import ConnectTimeout, Timeout, RequestException
import os
import csv
import re

product_info=[]

def product_info(products):
    for category, urls in products.items():
        print("sending products link to get product info...")
        info_scraper(category,urls)

def info_scraper(category,urls):
    
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Accept-Language": "en-US,en;q=0.5",
        }
    for url in urls:
        try:
            filename = "products.csv"

            # english title
            product_slug = ""
            product_slug = url.split('/')[-2]

            if not product_exists_in_csv(product_slug, filename):
                print("scraping product info...")
                page = requests.get(url, headers=headers)
                # print(page.text)
                if page.status_code == 200:
                    html = page.content
                    soup = BeautifulSoup(html, "html.parser")


                    # persian title
                    title = ""
                    title = soup.find('h1' , class_="product_title wd-entities-title")
                    if title:
                        title = title.text


                    # status
                    status = ""
                    status = soup.find('p', class_="stock out-of-stock")
                    if status:
                        status = "out-of-stock"
                        st = True
                    else:
                        st = False
                        status = "stock"

                    # des
                    des =""
                    des = soup.find("div", class_="wpb_wrapper")
                    if des:
                        des = des.text

                    #price
                    price = ""
                    price = soup.find('p' , class_="price")
                    if price:
                        price = price.text
                        price = extract_and_convert_price(price)

                    # Feature for non perfume
                    non_perfume_feature = []
                    non_perfume_dict_feature = {}
                    div = soup.find('div' , class_="woocommerce-product-details__short-description")
                    if div:
                        ps = div.find_all('p')
                        if ps:
                            ps = [item.text[2:] for item in ps[1:]]
                            non_perfume_feature = ps
                        else:
                            ol = div.find('ol')
                            if ol :
                                ol = ol.find_all('li')
                                for li in ol:
                                    non_perfume_feature.append(li.text)
                        if st == False:
                            ul = div.find('ul')
                            if ul:
                                ul = ul.find_all('li')
                                if ul:
                                    for li in ul:
                                        key = li.find('strong')
                                        if key:
                                            key = key.text
                                            value = ""
                                            value = li.find(string=True, recursive=False)
                                            if value:
                                                non_perfume_dict_feature[key.replace(u'\xa0',' ')] = value.replace(u'\xa0',' ')

                    # feature for perfume
                    perfume_feature = ""
                    div = soup.find('div', class_="woocommerce-product-details__short-description")
                    if div:
                        table = div.find("table")
                        if table:
                            table_contents = {}
                            for row in table.find_all('tr'):
                                columns = row.find_all(['th', 'td'])
                                if len(columns) >= 2:  
                                    key = columns[0].get_text(strip=True)
                                    value = columns[1].get_text(strip=True)
                                    table_contents[key] = value

                            perfume_feature = table_contents


                    #brand
                    div = soup.find('div', class_="pwb-single-product-brands pwb-clearfix")
                    if div:
                        brand = div.find('a').text
        

                    # cats
                    cats = soup.find('nav' , class_="woocommerce-breadcrumb")
                    categories = []
                    if cats:
                        cats = cats.contents[1:-1]
                        for cat in cats:
                            categories.append(cat.text)
                        categories = ' , '.join(map(str, categories)) # convert to string


                    # img
                    img = ""
                    div = soup.find("div" ,class_="product-image-wrap")
                    if div:
                        img = div.find("a")
                        if img:
                            img = img["href"]
                            img = f"https://asalbanooshop.com{img}"


                    # print(f"{categories}\n,{title}\n,{product_slug}\n,{price}\n,{des}\n,{feature}\n,{status}\n,{feature}\n")

                if perfume_feature:
                    product_info_for_csv = [title,product_slug,price,des,perfume_feature,"",brand,img,status,categories,url]
                    product_info_for_json = {
                    "titleFa" : title,
                    "titleEn" : product_slug,
                    "price" : price,
                    "des" : des,
                    "perfume_feature" : perfume_feature,
                    "brand" : brand,
                    "img" : img,
                    "status" : status,
                    "categories" :categories,
                    }
                else:
                    product_info_for_csv = [title,product_slug,price,des,non_perfume_feature,non_perfume_dict_feature,brand,img,status,categories,url]
                    product_info_for_json = {
                    "titleFa" : title,
                    "titleEn" : product_slug,
                    "price" : price,
                    "des" : des,
                    "non_perfume_feature" : non_perfume_feature,
                    "non_perfume_dict_feature" : non_perfume_dict_feature,
                    "brand" : brand,
                    "img" : img,
                    "status" : status,
                    "categories" :categories,
                    }
                
                    
                
                csv_writer(product_info_for_csv)
                json_writer(product_info_for_json)

            else:
                print(f"شناسه محصول {product_slug} قبلاً در {filename} وجود دارد. در حال نادیده گرفتن.")


        except ConnectTimeout:
            print(f"Connection to {url} timed out. Please check the URL or your internet connection.")
        except Timeout:
            print(f"The request to {url} timed out. Please try again later.")
        except RequestException as e:
            print(f"An error occurred: {e}")



def product_exists_in_csv(product_slug, filename='products.csv'):
    if not os.path.exists(filename):
        return False
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if product_slug in row:
                return True
    return False


def extract_and_convert_price(text):
    match = re.search(r'(\d{1,3}(?:,\d{3})*)', text)
    if match:
        number_str = match.group(1).replace(',', '')
        converted_number = int(number_str) * 10
        return converted_number
    return None
