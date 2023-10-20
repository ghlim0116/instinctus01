import requests

# https://accounts.google.com/o/oauth2/v2/auth?scope=https%3A//www.googleapis.com/auth/drive.metadata.readonly&access_type=offline&include_granted_scopes=true&response_type=code&state=state_parameter_passthrough_value&redirect_uri=https%3A//cheremimaka.com/&client_id=********************************
access_code = '******************************************************'

CLIENT_ID = '*************************************'
CLIENT_SECRET = '************************************************'
SCOPE = "https://www.googleapis.com/auth/analytics.manage.users.readonly https://www.googleapis.com/auth/analytics.provision https://www.googleapis.com/auth/analytics https://www.googleapis.com/auth/doubleclicksearch https://www.googleapis.com/auth/adwords https://www.googleapis.com/auth/analytics.readonly"
REDIRECT_URI = 'https://cheremimaka.com'
url = 'https://oauth2.googleapis.com/token'
payload = '''grant_type=authorization_code&code={}&redirect_uri=https://cheremimaka.com/&client_id={}&client_secret={}'''.format(access_code,CLIENT_ID,CLIENT_SECRET)
headers = {
    'Authorization': "Bearer %s" %(access_code),
    'Content-Type': "application/x-www-form-urlencoded"
    }
response = requests.request("POST", url, data=payload, headers=headers)
print(response.text)
with open("token.txt",'w') as tw:
    tw.write(response.text)
