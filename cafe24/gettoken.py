import requests

# get authentication code
# https://instinctus1.cafe24api.com/api/v2/oauth/authorize?response_type=code&client_id=P61HFaFvCVknfoQr4V4iCD&state=1&redirect_uri=https://cheremimaka.com&scope=mall.read_application,mall.read_category,mall.read_product,mall.read_collection,mall.read_supply,mall.read_personal,mall.read_order,mall.read_community,mall.read_customer,mall.read_notification,mall.read_store,mall.read_promotion,mall.read_design,mall.read_salesreport,mall.read_privacy,mall.read_shipping,mall.read_analytics&shop_no=1

# get access token
access_code = 'qYqnBOYsKxspeMwBjVfMPG'
url = "https://instinctus1.cafe24api.com/api/v2/oauth/token"
payload = '''grant_type=authorization_code&code=%s&redirect_uri=https://cheremimaka.com''' %(access_code)
headers = {
    'Authorization': "Bearer UDYxSEZhRnZDVmtuZm9RcjRWNGlDRDpHYXFZU0R1RUlwanBpSk40U2dnT0NB",
    'Content-Type': "application/x-www-form-urlencoded"
    }
response = requests.request("POST", url, data=payload, headers=headers)
with open("token.txt",'w') as tw:
    tw.write(response.text)
print(response.text)