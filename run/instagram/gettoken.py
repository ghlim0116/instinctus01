import requests
import json

# 아래 주소를 브라우저 주소입력창에 입력
# code를 복사하되 맨 마지막의 '#_'는 제외해야 함
# https://api.instagram.com/oauth/authorize?client_id=3376505482667195&redirect_uri=https://cheremimaka.com/&scope=user_profile,user_media,email,manage_fundraisers,read_insights,publish_video,catalog_management,private_computation_access,pages_manage_cta,pages_manage_instant_articles,pages_show_list,read_page_mailboxes,ads_management,ads_read,business_management,pages_messaging,pages_messaging_phone_number,pages_messaging_subscriptions,instagram_basic,instagram_manage_comments,instagram_manage_insights,instagram_content_publish,publish_to_groups,groups_access_member_info,leads_retrieval,whatsapp_business_management,instagram_manage_messages,attribution_read,page_events,pages_read_engagement,pages_manage_metadata,pages_read_user_content,pages_manage_ads,pages_manage_posts,pages_manage_engagement,whatsapp_business_messaging,instagram_shopping_tag_products,instagram_graph_user_profile&response_type=code

acode = 'AQD0zgyPn2J4gcr5cV5mHZxhYUI-WKruESxdYavxwoAav8llf4jGE_tgkBvEGLcj6OyN0tuR8ZdxqE3Fie4ao10CKisVJF-Cx-HPOvtOZgBcivIS-3IhfLz-MnFIb7vmPfr1cpZ5Xhxwj8rIzMpQfj2aCTCvMKkvgAX0Xo62xmPdRg28dCc-h6VD6Q_vC0TucZ3daAxeTaTHGXqSXBiQR3UzXV7N9BdY8MNWNBXgiBjlqA'
igappid = '3376505482667195'
url = "https://api.instagram.com/oauth/access_token"
files = {
    'client_id': (None, igappid),
    'client_secret': (None, 'd94b1fc00f0e40d9cfc096587161d62a'),
    'grant_type': (None, 'authorization_code'),
    'redirect_uri': (None, 'https://cheremimaka.com/'),
    'code': (None, acode),
}
response = requests.post(url, files=files)
print(response.text)
with open("token.txt",'w') as token:
    atoken = response.json()['access_token']
    url = "https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret=d94b1fc00f0e40d9cfc096587161d62a&access_token={}".format(atoken)
    response2 = requests.get(url)
    rjson = response2.json()
    rjson['user_id'] = response.json()['user_id']
    token.write(str(rjson))
# access_token에 60일짜리 토큰이 저장됨

#{'access_token': 'IGQVJXckxIcXNMRkk2MWJYelhwWHE2ZAnN0T1pEcndOUmtzeFZA0U3lCY2dWaHhCYTJCdWhzUHUwN2JqVFRrVjlCQzVreVB1a3g2ZAUFKWVpGcG9vT2RDWXQ2UEtrNUNjNFpFLVhBZAmhB', 'token_type': 'bearer', 'expires_in': 5100648, 'user_id': 17841406838763700, 'access_token_2h': 'IGQVJVYjRsVWhpMUk3cEdJYXVVcXF2dDE1UzB3S1lxZAnVLTUs1SmVZAVFpleXpEUjVTMTEzY0N0d0xFWnQ4cUY1emNTN1lmc0ZATcGFmUEFWLVRGcF9xaU1DajdJdnY4RVBJX21Pbno5TVd6anVxd21PcDZAQU1pGZAkFQV0xN'}