import json
import requests

def refresh():
    # load saved refresh token
    with open("token.txt",'r') as f:
        token = f.read()
    rtoken= json.loads(token)['refresh_token']

    # get access token with refresh token
    url = "https://instinctus1.cafe24api.com/api/v2/oauth/token"
    payload = 'grant_type=refresh_token&refresh_token=%s' %(rtoken)
    headers = {
        'Authorization': "Bearer UDYxSEZhRnZDVmtuZm9RcjRWNGlDRDpHYXFZU0R1RUlwanBpSk40U2dnT0NB",
        'Content-Type': "application/x-www-form-urlencoded"
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    with open("token.txt", 'w') as fw:
        responsejson = response.json()
        responsejson['prtoken'] = rtoken
        json.dump(responsejson,fw)

    newtoken = json.loads(response.text)['access_token']    
    return newtoken