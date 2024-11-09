from bs4 import BeautifulSoup
import requests
import re
import json


def extract_and_convert(text):
    match = re.search(r'(\d{1,3}(?:,\d{3})*)', text)
    if match:
        number_str = match.group(1).replace(',', '')
        converted_number = int(number_str) * 10
        return converted_number
    return None


headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "en-US,en;q=0.5",
    }

url = "https://asalbanooshop.com/product/mac-weightless-loose-powder/"

# english title
product_slug = ""
product_slug = url.split('/')[-2]

page = requests.get(url, headers=headers)
# print(page.text)
if page.status_code == 200:
    html = page.content
    soup = BeautifulSoup(html, "html.parser")

    #price
    price = ""
    price = soup.find('p' , class_="price")
    if price:
        price = price.text
        price = extract_and_convert(price)

    status = ""
    status = soup.find('p', class_="stock out-of-stock")
    if status:
        status = "out-of-stock"
        st = True
    else:
        st = False
        status = "stock"

    # Feature for non perfume
    feature = []
    dict_feature = {}
    div = soup.find('div' , class_="woocommerce-product-details__short-description")
    if div:
        ps = div.find_all('p')
        if ps:
            ps = [item.text[2:] for item in ps[1:]]
            feature = ps
        else:
            ol = div.find('ol')
            if ol :
                ol = ol.find_all('li')
                for li in ol:
                    feature.append(li.text)

                

        if st == False:
            ul = div.find('ul')
            if ul:
                ul = ul.find_all('li')
                if ul:
                    for li in ul:
                        key = li.find('strong').text
                        value = li.find(string=True, recursive=False).strip()
                        dict_feature[key.replace(u'\xa0',' ')] = value.replace(u'\xa0',' ')

            

    # feature for perfume
    per_feature = ""
    div = soup.find('div', class_="woocommerce-product-details__short-description")
    if div:
        table = div.find("table")
        if table:
            table_contents = {}
            for row in table.find_all('tr'):
                columns = row.find_all(['th', 'td'])
                if len(columns) >= 2:  # اطمینان از وجود حداقل دو ستون
                    key = columns[0].get_text(strip=True)
                    value = columns[1].get_text(strip=True)
                    table_contents[key] = value

            per_feature = table_contents


    #brand
    #<div class="pwb-single-product-brands pwb-clearfix"><span class="pwb-text-before-brands-links">برند:</span><a href="/brand/forever52/" title="نمایش برندها">فور اور 52</a></div>
    div = soup.find('div', class_="pwb-single-product-brands pwb-clearfix")
    if div:
        keybr = div.find('span').text
        vabr = div.find('a').text
    temp = [feature,price,vabr,dict_feature,per_feature]
    with open("product.json", mode='a', encoding='utf-8') as json_file:
        json.dump(temp, json_file, ensure_ascii=False, indent=4)


print(price)
print(feature)
print(keybr , vabr)
print(dict_feature)


