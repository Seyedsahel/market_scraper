from bs4 import BeautifulSoup
import requests
from csv_writer import *
from requests.exceptions import ConnectTimeout, Timeout, RequestException
import os
import csv

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

                    #price
                    price = ""
                    price = soup.find('p' , class_="price")
                    if price:
                        price = price.text

                    # des
                    des =""
                    des = soup.find("div", class_="wpb_wrapper")
                    if des:
                        des = des.text

                    # Feature for non perfume
                    feature = ""
                    div = soup.find('div' , class_="woocommerce-product-details__short-description")
                    if div:
                        ol = div.find('ol')
                        if ol :
                            feature += ol.text
                        if st == False:
                            ul = div.find('ul')
                            if ul:
                                feature += ul.text

                    # feature for perfume
                    div = soup.find('div', class_="woocommerce-product-details__short-description")
                    if div:
                        table = div.find("table")
                        if table:
                            table_contents = []
                            for row in table.find_all('tr'):
                                columns = row.find_all(['th', 'td'])
                                row_data = [col.get_text(strip=True) for col in columns]
                                table_contents.append(' : '.join(row_data))

                            feature = '-'.join(table_contents)

                    #brand
                    div = soup.find('div', class_="pwb-single-product-brands pwb-clearfix")
                    if div:
                        keybr = div.find('span').text
                        valbr = div.find('a').text

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


                product_info = [title,product_slug,price,des,feature,img,status,categories,url]
                csv_writer(product_info)

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