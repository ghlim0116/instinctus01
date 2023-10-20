import json
import requests

def refresh():
    with open("token.txt",'r') as f:
        token = f.read()
    rtoken= json.loads(token)['refresh_token']

    CLIENT_ID = '********************************************'
    CLIENT_SECRET = '********************************'
    url = 'https://oauth2.googleapis.com/token'
    payload = '''grant_type=refresh_token&refresh_token={}&client_id={}&client_secret={}&access_type=offline'''.format(rtoken,CLIENT_ID,CLIENT_SECRET)
    headers = {
        'Host':'oauth2.googleapis.com',
        'Content-Type': "application/x-www-form-urlencoded"
        }
    response = requests.request("POST", url, data=payload, headers=headers).json()
    response['prtoken'] = rtoken
    with open("newtoken.txt",'w') as tw:
        json.dump(response,tw,indent=4)
    newtoken = json.loads(response.text)['access_token']    
    return newtoken
