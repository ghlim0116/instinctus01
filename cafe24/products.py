import requests
import json
import time
import datetime
import csv
from dateutil.parser import parse
from dateutil import relativedelta
import refreshtoken

def product():
    time1 = datetime.datetime.now()

    atoken= refreshtoken.refresh()
    time.sleep(0.5)
    apicount = 1

    # get product count
    headers = {
        'Authorization': 'Bearer %s' %(atoken),
        'Content-Type': "application/json",
        'X-Cafe24-Api-Version': "2022-09-01"
        }
    url = "https://instinctus1.cafe24api.com/api/v2/admin/products/count"
    response = requests.request("GET", url, headers=headers)
    productcount = json.loads(response.text)['count']
    print(productcount, 'products found')
    apicount += 1
    time.sleep(0.5)

    # get product data

    product_header = [
        "shop_no",
        "product_no",
        "product_code",
        "custom_product_code",
        "product_name",
        "eng_product_name",
        "supply_product_name",
        "internal_product_name",
        "model_name",
        "price_excluding_tax",
        "price",
        "retail_price",
        "supply_price",
        "display",
        "selling",
        "summary_description",
        "adult_certification",
        "made_in_code",
        "product_weight",
        "product_material",
        "created_date",
        "updated_date",
        "sold_out",
        "additional_price",
        "shipping_fee_by_product",
        "shipping_fee_type"
    ]    

    with open("products.csv", 'w', encoding='utf-8-sig') as products:
        offset = 0
        write = csv.DictWriter(products, fieldnames= product_header)
        write.writeheader()
        for i in range(0,productcount//100+1):
            url = "https://instinctus1.cafe24api.com/api/v2/admin/products?offset=%s&limit=100" %(offset)
            response = requests.request("GET", url, headers=headers)
            apicount += 1
            time.sleep(0.4)
            for i in range(0,len(json.loads(response.text)['products'])):
                row = json.loads(response.text)['products'][i]
                write.writerow(
                    {
                        "shop_no":row["shop_no"],
                        "product_no":row["product_no"],
                        "product_code":row["product_code"],
                        "custom_product_code":row["custom_product_code"],
                        "product_name":row["product_name"],
                        "eng_product_name":row["eng_product_name"],
                        "supply_product_name":row["supply_product_name"],
                        "internal_product_name":row["internal_product_name"],
                        "model_name":row["model_name"],
                        "price_excluding_tax":row["price_excluding_tax"],
                        "price":row["price"],
                        "retail_price":row["retail_price"],
                        "supply_price":row["supply_price"],
                        "display":row["display"],
                        "selling":row["selling"],
                        "summary_description":row["summary_description"],
                        "adult_certification":row["adult_certification"],
                        "made_in_code":row["made_in_code"],
                        "product_weight":row["product_weight"],
                        "product_material":row["product_material"],
                        "created_date":parse(row["created_date"]).strftime('%y-%m-%d %H:%M:%S'),
                        "updated_date":parse(row["updated_date"]).strftime('%y-%m-%d %H:%M:%S'),
                        "sold_out":row["sold_out"],
                        "additional_price":row["additional_price"],
                        "shipping_fee_by_product":row["shipping_fee_by_product"],
                        "shipping_fee_type":row["shipping_fee_type"]
                    }
                )
            offset += 100

    del products
    time2 = datetime.datetime.now()
    print(apicount, 'APIs sent')
    print(time2 - time1, 'elapsed')