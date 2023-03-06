import requests

url = "https://graph.facebook.com/oauth/access_token?client_id={}&client_secret={}&grant_type=client_credentials".format(appid,appsecret)
response = requests.get(url)
print(response.text)
with open("apptoken.txt","w") as atk:
    atk.write(response.text)