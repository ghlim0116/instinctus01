import requests

# 장기 실행 사용자 액세스 토큰 얻기
atoken = 'user_token'
url = "https://graph.facebook.com/oauth/access_token"
params = {
    'grant_type':'fb_exchange_token',
    'client_id':'857805542024270',
    'client_secret':'f8ef7c9e599ec5e97b7a564d9f5eccc8',
    'fb_exchange_token':atoken,
}
response = requests.get(url,params=params)
atoken = response.json()['access_token']
# 권한 없다고 나와서 여기서 안 하고 그래프 API 탐색기에서 함
# 유효기간이 없는 토큰이므로 계속 써도 됨
{
    "access_token":"EAAMMK2qeZAE4BAJO93OEzOSVRZAnNqGZBNjntifR6irdzBb2uBWF2ogA2EhKDAA4KyA4D4XqXsGZCNtzJPH8zS6ijmLkdyyfJsKMiyKugUz05wpthzYf5GsQD3Topq8qMkhlpBt3lVPQeASlqe7KCp4MiZCRfIxFW7R7ZCUkHms5pWC6Pvf7YK4b6fQORPF6ZBh7E8TpuNWyNsRpEUC6mYX",
    "token_type":"bearer",
    "expires_in":5100990
}