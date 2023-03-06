import requests
import json

def refreshtoken():
    with open("token.txt",'r') as token:
        token = token.read().replace("'",'"')
    token = json.loads(token)
    atoken = token['access_token']
    ig_user_id = token['user_id']

    url = "https://graph.instagram.com/refresh_access_token"
    params = {
        'grant_type':'ig_refresh_token',
        'access_token':atoken,
        }
    response = requests.get(url,params=params)
    rjson = response.json()
    rjson['user_id'] = ig_user_id
    with open("token.txt",'w') as token:
        token.write(str(rjson))