from bs4 import BeautifulSoup
import requests
import re
import math

links = {}

def find_pages(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "en-US,en;q=0.5",
    }
    page = requests.get(url, headers=headers)
    rounded_up = 0
    # print(page.text)
    if page.status_code == 200:
        html = page.content
        soup = BeautifulSoup(html, "html.parser")
        
        text1 = soup.find('p' ,class_="woocommerce-result-count").text
        pattern = r"(\d+) نتیجه"
        match = re.search(pattern, text1)
        if match:
            result = match.group(1)
        rounded_up = math.ceil(int(result) / 15)

    return rounded_up

        


def product_urls(base_cats_links):
    print("sending cats link to get product links...")
    for category, base_url in base_cats_links.items():
        i = find_pages(base_url)
        links[category] = []
        for page in range(1, i):  
            page_url = f"{base_url}page/{page}/"
            scrape_urls(page_url,category)
    return links

def scrape_urls(url,category):
    print("scrape cats links...")
    
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Accept-Language": "en-US,en;q=0.5",
        }
    page = requests.get(url, headers=headers)
    # print(page.text)
    if page.status_code == 200:
        html = page.content
        soup = BeautifulSoup(html, "html.parser")
   
        a_tags = soup.find_all('a', class_="product-image-link")
        for a in a_tags:
            href = a.get('href')
            if href:
                links[category].append(f"https://asalbanooshop.com{href}")
    else:
        print(page.status_code)


    return links


