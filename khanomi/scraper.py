import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def product_id_from_url(url):
    return url.split('-')[-1]  

def id_exists_in_csv(product_id, filename='products.csv'):
    if not os.path.exists(filename):
        return False
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if product_id in row:  
                return True
    return False

def scrape_product_links(url):
    links = []
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    # chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "relative")))

    page_content = driver.page_source
    soup = BeautifulSoup(page_content, 'html.parser')
    driver.quit()

    a_tags = soup.find_all('a', class_="relative flex h-full w-full flex-col gap-2 p-2")
    for a in a_tags:
        href = a.get('href')
        if href:
            links.append(href)

    return links

def scrape_product_info(url, category):
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "relative")))

    page_content = driver.page_source
    soup = BeautifulSoup(page_content, 'html.parser')
    driver.quit()

    # TITLE
    titlep = soup.find("h1", class_="text-body-16 font-medium text-text-black")
    if titlep:
        titlep = titlep.text
    titlee = soup.find('span', class_="hidden text-body-14 font-medium text-text-mediumGray lg:flex")
    if titlee:
        titlee = titlee.text
        
    # PRICE
    price_out = ""
    price_in = ""

    main_div = soup.find("div", class_="flex w-fit flex-col items-center gap-1 lg:gap-1.5")
    if main_div:
        price = main_div.find('span', class_="px-2 text-center text-body-14 text-text-mediumGray line-through")
        if price:
            price_out = price.text
            price_in = main_div.find('span', class_="text-body-14 font-medium text-text-black lg:text-body-16").text
        else:
            price_out = main_div.find('span', class_="text-body-14 font-medium text-text-black lg:text-body-16").text
            price_in = price_out  

    # DES
    des = soup.find('div', class_="relative flex w-full flex-col gap-2 lg:gap-3")
    if des:
        des = des.find('p').text

    product_id = product_id_from_url(url)
    filename = "products.csv"
    if titlep and titlee and price_in and price_out and des:
        if not id_exists_in_csv(product_id, filename):
            with open(filename, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([titlep, titlee, price_in, price_out, des, category, url])
            print(f"اطلاعات در {filename} ذخیره شد.")
        else:
            print(f"شناسه محصول {product_id} قبلاً در {filename} وجود دارد. در حال نادیده گرفتن.")

def create_category_links(base_url, pages):
    return {key: [f"{value}?page_number={i}" for i in range(1, pages + 1)] 
            for key, value in base_url.items()}

def scraper():
    base_cats_links = {
        "skincare": "https://www.khanoumi.com/categories/skincare",
        "hair": "https://www.khanoumi.com/categories/hair",
        "lips-makeup": "https://www.khanoumi.com/categories/makeup/lips-makeup",
        "eye-makeup": "https://www.khanoumi.com/categories/makeup/eye-makeup",
        "face-care": "https://www.khanoumi.com/categories/skincare/face-care",
        "men" : "https://www.khanoumi.com/categories/makeup/men",
        "electrical-personal-care":"https://www.khanoumi.com/categories/electrical-personal-care"
    }
    
    cats_links = create_category_links(base_cats_links, 2)
    
    product_links = {}
    for key, value in cats_links.items():
        for url in value:
            product_links[key] = scrape_product_links(url)

    for key, value in product_links.items():
        for link in value:
            scrape_product_info(f"https://www.khanoumi.com{link}", key)

scraper()