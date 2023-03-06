import requests
import json
import pandas as pd
import numpy as np
import time
import datetime
import csv
from dateutil.parser import parse
from dateutil import relativedelta
import refreshtoken

def orders():
    time1 = datetime.datetime.now()
    apicount = 0

    atoken = refreshtoken.refresh()
    time.sleep(0.5)
    apicount += 1
    
    orders = open("orders.csv", 'w', encoding='utf-8-sig')
    orderitems = open("orderitems.csv", 'w', encoding='utf-8-sig')
    orderbr = open("orderbr.csv", 'w', encoding='utf-8-sig')
    # header
    order_header = [
        "order_id",
        "currency",
        "market_id",
        "member_id",
        "member_email",
        "billing_name",
        "payment_method",
        "order_date",
        "first_order",
        "payment_date",
        "group_no_when_ordering",
        "order_price_amount",
        "shipping_fee",
        "points_spent_amount",
        "credits_spent_amount",
        "coupon_discount_price",
        "coupon_shipping_fee_amount",
        "membership_discount_amount",
        "shipping_fee_discount_amount",
        "set_product_discount_amount",
        "app_discount_amount",
        "point_incentive_amount",
        "total_amount_due",
        "payment_amount",
        # "sales_amount",
        # "tax_amount",
        "market_other_discount_amount",
        "order_place_name",
        "order_place_id",
        "postpay",
        "additional_shipping_fee",
        "international_shipping_insurance",
        "additional_handling_fee",
        "shipping_type",
        "shipping_type_text",
        "shipping_status"
    ]
    orderitem_header = [
        "order_id",
        "member_id",
        "item_no",
        "order_status",
        "order_item_code",
        "variant_code",
        "product_code",
        "custom_product_code",
        "custom_variant_code",
        "option_id",
        "option_value",
        "option_value_default",
        "product_name",
        "product_name_default",
        "product_price",
        "option_price",        
        "additional_discount_price",
        "coupon_discount_price",
        "item_payment_amount",
        "quantity",
        "product_tax_type",
        "tax_rate",
        "supplier_product_name",
        "supplier_id",
        "supplier_name",
        "tracking_no",
        "shipping_code",
        "shipping_company_id",
        "shipping_company_name",
        "shipping_company_code",
        "product_bundle",
        "product_bundle_name",
        "naver_pay_order_id",
        "ordered_date",
        "shipped_date",
        "delivered_date"
    ]
    writeorder = csv.DictWriter(orders, fieldnames= order_header)
    writeorder.writeheader()
    writeorderitem = csv.DictWriter(orderitems, fieldnames= orderitem_header)
    writeorderitem.writeheader()
    writeorderbr = csv.writer(orderbr)
    headerTF = False

    #get order count
    autho = 'bearer %s' %(atoken)
    headers = {
        'Authorization': autho,
        'Content-Type': "application/json",
        'X-Cafe24-Api-Version': "2022-09-01"
        }
    onemonth = relativedelta.relativedelta(months=1)
    oneday = datetime.timedelta(days=1)
    
    start_date = datetime.datetime.now().date().replace(day=1) - 12 * onemonth
    # start_date = datetime.datetime(year = 2019, month = 1, day = 1).date()
    end_date = start_date + onemonth - oneday
    totalorders = 0
    def date_fix(date):
        if date != None:
            fixed_date = parse(date).strftime('%y-%m-%d %H:%M:%S')
        else:
            fixed_date = '00-00-00 00:00:00'
        return fixed_date

    while True:
        url = "https://instinctus1.cafe24api.com/api/v2/admin/orders/count?start_date=%s&end_date=%s" %(start_date,end_date) #&order_status=N10,N20,N30,N40
        response = requests.request("GET", url, headers=headers)
        try:
            orderscount = json.loads(response.text)['count']
        except Exception as e:
            if "A temporary server error has occurred" in response.text:
                raise ImportError('TemporaryServerError')
            else:
                raise e
            
        totalorders += orderscount
        print(str(start_date)[:7],' : ',orderscount)
        time.sleep(0.5)
        apicount += 1

        # get order data
        getdatacount = orderscount // 100 + 1
        for k in range(0,getdatacount):
            offset = k * 100
            url = "https://instinctus1.cafe24api.com/api/v2/admin/orders?start_date=%s&end_date=%s&limit=100&offset=%s&embed=items,buyer,receivers" %(start_date,end_date,offset) #&order_status=N10,N20,N30,N40
            response = requests.request("GET", url, headers=headers)
            time.sleep(0.3)
            apicount += 1
            try:
                r = json.loads(response.text)['orders']
            except Exception as e:
                if "A temporary server error has occurred" in response.text:
                    raise ImportError('TemporaryServerError')
                else:
                    raise e
            # orders.write(response.text)
            for i in r:
                # taxed = 0
                # taxfree = 0
                payment_amount = float(i['actual_order_amount']['payment_amount'])
                order_price_amount = float(i['actual_order_amount']['order_price_amount'])
                for j in i['items']:
                    product_price = float(j['product_price'])
                    option_price = float(j['option_price'])
                    additional_discount_price = float(j['additional_discount_price'])
                    coupon_discount_price = float(j['coupon_discount_price'])
                    if order_price_amount == 0:                        
                        item_payment_amount = 0
                    else:
                        item_payment_amount = round((product_price + option_price + additional_discount_price + coupon_discount_price)/order_price_amount * payment_amount,0)
                        
                    tax_rate = float(j['tax_rate'])
                    # total_price = product_price + option_price
                    # if tax_rate > 0:
                    #     taxed = taxed + total_price
                    # else:
                    #     taxfree = taxfree + total_price
                    ordered_date = date_fix(j['ordered_date'])
                    shipped_date = date_fix(j['shipped_date'])
                    delivered_date = date_fix(j['delivered_date'])
                    writeorderitem.writerow(
                        {
                            "order_id":i['order_id'],
                            "member_id":i['member_id'],
                            "item_no":j['item_no'],
                            "order_status":j['order_status'],
                            "order_item_code":j['order_item_code'],
                            "variant_code":j['variant_code'],
                            "product_code":j['product_code'],
                            "custom_product_code":j['custom_product_code'],
                            "custom_variant_code":j['custom_variant_code'],
                            "option_id":j['option_id'],
                            "option_value":j['option_value'],
                            "option_value_default":j['option_value_default'],
                            "product_name":j['product_name'],
                            "product_name_default":j['product_name_default'],
                            "product_price":product_price,
                            "option_price":option_price,                            
                            "additional_discount_price":additional_discount_price,
                            "coupon_discount_price":coupon_discount_price,
                            "item_payment_amount":item_payment_amount,
                            "quantity":j['quantity'],
                            "product_tax_type":j['product_tax_type'],
                            "tax_rate":tax_rate,
                            "supplier_product_name":j['supplier_product_name'],
                            "supplier_id":j['supplier_id'],
                            "supplier_name":j['supplier_name'],
                            "tracking_no":j['tracking_no'],
                            "shipping_code":j['shipping_code'],
                            "shipping_company_id":j['shipping_company_id'],
                            "shipping_company_name":j['shipping_company_name'],
                            "shipping_company_code":j['shipping_company_code'],
                            "product_bundle":j['product_bundle'],
                            "product_bundle_name":j['product_bundle_name'],
                            "naver_pay_order_id":j['naver_pay_order_id'],
                            "ordered_date": ordered_date,
                            "shipped_date": shipped_date,
                            "delivered_date": delivered_date
                        }
                    )
                brjson = i['receivers'][0]
                brjson['order_id'] = i['order_id']
                for l in i['buyer'].keys():
                    brjson[l] = i['buyer'][l]
                if headerTF == False:
                    writeorderbr.writerow(brjson.keys())
                    headerTF = True
                if brjson['updated_date'] != None:
                    brjson['updated_date'] = parse(brjson['updated_date']).strftime('%Y-%m-%d %H:%M:%S')
                writeorderbr.writerow(brjson.values())

                order_date = date_fix(i['order_date'])
                payment_date = date_fix(i['payment_date'])                
                # try:
                #     sales_amount = payment_amount * (1 - taxed/11/(taxed + taxfree))
                # except ZeroDivisionError:
                #     sales_amount = 0
                # tax_amount = payment_amount - sales_amount
                writeorder.writerow(
                    {
                        'order_id':i['order_id'],
                        'currency':i['currency'],
                        'market_id':i['market_id'],
                        'member_id':i['member_id'],
                        'member_email':i['member_email'],
                        'billing_name':i['billing_name'],
                        'payment_method':';'.join(i['payment_method']),
                        'order_date':order_date,
                        'first_order':i['first_order'],
                        'payment_date':payment_date,
                        'group_no_when_ordering':i['group_no_when_ordering'],
                        "order_price_amount":order_price_amount,
                        "shipping_fee":i['actual_order_amount']['shipping_fee'],
                        "points_spent_amount":i['actual_order_amount']['points_spent_amount'],
                        "credits_spent_amount":i['actual_order_amount']['credits_spent_amount'],
                        "coupon_discount_price":i['actual_order_amount']['coupon_discount_price'],
                        "coupon_shipping_fee_amount":i['actual_order_amount']['coupon_shipping_fee_amount'],
                        "membership_discount_amount":i['actual_order_amount']['membership_discount_amount'],
                        "shipping_fee_discount_amount":i['actual_order_amount']['shipping_fee_discount_amount'],
                        "set_product_discount_amount":i['actual_order_amount']['set_product_discount_amount'],
                        "app_discount_amount":i['actual_order_amount']['app_discount_amount'],
                        "point_incentive_amount":i['actual_order_amount']['point_incentive_amount'],
                        "total_amount_due":i['actual_order_amount']['total_amount_due'],
                        "payment_amount":payment_amount,
                        # "sales_amount":sales_amount,
                        # "tax_amount":tax_amount,
                        "market_other_discount_amount":i['actual_order_amount']['market_other_discount_amount'],
                        "order_place_name":i["order_place_name"],
                        "order_place_id":i["order_place_id"],
                        "postpay":i['postpay'],
                        "additional_shipping_fee":i['additional_shipping_fee'],
                        "international_shipping_insurance":i['international_shipping_insurance'],
                        "additional_handling_fee":i['additional_handling_fee'],
                        "shipping_type":i['shipping_type'],
                        "shipping_type_text":i['shipping_type_text'],
                        "shipping_status":i['shipping_status']
                    }
                )
        start_date = start_date + onemonth
        end_date = start_date + onemonth - oneday
        if datetime.datetime.now().date() < start_date:
            break
    orders.close()
    orderitems.close()
    del orders, orderitems
    print(apicount, 'APIs sent')

    time2 = datetime.datetime.now()
    print(time2 - time1, ' elapsed')
    print('Total orders : ',totalorders)