import requests
import json

# 아래 주소를 브라우저 주소입력창에 입력
# code를 복사하되 맨 마지막의 '#_'는 제외해야 함
# https://api.instagram.com/oauth/authorize?client_id=***************&redirect_uri=https://cheremimaka.com/&scope=user_profile,user_media,email,manage_fundraisers,read_insights,publish_video,catalog_management,private_computation_access,pages_manage_cta,pages_manage_instant_articles,pages_show_list,read_page_mailboxes,ads_management,ads_read,business_management,pages_messaging,pages_messaging_phone_number,pages_messaging_subscriptions,instagram_basic,instagram_manage_comments,instagram_manage_insights,instagram_content_publish,publish_to_groups,groups_access_member_info,leads_retrieval,whatsapp_business_management,instagram_manage_messages,attribution_read,page_events,pages_read_engagement,pages_manage_metadata,pages_read_user_content,pages_manage_ads,pages_manage_posts,pages_manage_engagement,whatsapp_business_messaging,instagram_shopping_tag_products,instagram_graph_user_profile&response_type=code

acode = '*****************************************************************************************************************************'
igappid = '********************'
url = "https://api.instagram.com/oauth/access_token"
files = {
    'client_id': (None, igappid),
    'client_secret': (None, '*****************************'),
    'grant_type': (None, 'authorization_code'),
    'redirect_uri': (None, 'https://cheremimaka.com/'),
    'code': (None, acode),
}
response = requests.post(url, files=files)
print(response.text)
with open("token.txt",'w') as token:
    atoken = response.json()['access_token']
    url = "https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret=*****************************&access_token={}".format(atoken)
    response2 = requests.get(url)
    rjson = response2.json()
    rjson['user_id'] = response.json()['user_id']
    token.write(str(rjson))
# access_token에 60일짜리 토큰이 저장됨

#{'access_token': '**********************************************************************************************************************', 'token_type': 'bearer', 'expires_in': 5100648, 'user_id': ***************, 'access_token_2h': '*********************************************************************************************************************************************'}
