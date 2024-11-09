import csv

def csv_writer(product_info):
    filename = "products.csv"

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(product_info)
    print(f"اطلاعات در {filename} ذخیره شد.")
