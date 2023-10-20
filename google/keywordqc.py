import numpy as np
import time
import datetime
import requests
import csv
import pymysql
import json
import refreshtoken
from dateutil.parser import parse
from dateutil import relativedelta
import argparse
import sys
#from google.ads.googleads.v12.services.services.keyword_plan_idea_service
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


time1 = datetime.datetime.now()

try:
    access_token = refreshtoken.refresh()
except:
    with open('token.txt','r') as tokentxt:
        token = tokentxt.read()
        access_token = json.loads(token)['access_token']
onemonth = relativedelta.relativedelta(months=1)
oneday = datetime.timedelta(days=1)
requested_end_date =  datetime.datetime.now().date()
requested_start_date = requested_end_date - onemonth
CLIENT_ID = '*****************************************'


def main(
    client, customer_id, location_ids, language_id, keyword_texts, page_url
):
    keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")
    keyword_competition_level_enum = (client.enums.KeywordPlanCompetitionLevelEnum)
    language_rn = client.get_service("GoogleAdsService").language_constant_path(language_id)
    location_rns = map_locations_ids_to_resource_names(client, location_ids)
    keyword_plan_network = (client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH_AND_PARTNERS)
    

    # if not (keyword_texts or page_url):
    #     raise ValueError(
    #         "At least one of keywords or page URL is required, "
    #         "but neither was specified."
    #     )

    request = client.get_type("GenerateKeywordIdeasRequest")
    request.customer_id = customer_id
    request.language = language_rn
    request.geo_target_constants = location_rns
    request.keyword_plan_network = keyword_plan_network
    request.include_adult_keywords = True
    request.keyword_seed.keywords.extend(keyword_texts)
    
    # if not keyword_texts and page_url:
    #     request.url_seed.url = page_url
    # elif keyword_texts and not page_url:
    #     request.keyword_seed.keywords.extend(keyword_texts)
    # elif keyword_texts and page_url:
    #     request.keyword_and_url_seed.url = page_url
    #     request.keyword_and_url_seed.keywords.extend(keyword_texts)

    keyword_ideas = keyword_plan_idea_service.generate_keyword_ideas(request=request)

    for idea in keyword_ideas:
        competition_value = idea.keyword_idea_metrics.competition.name
        print(
            f'Keyword idea text "{idea.text}" has '
            f'"{idea.keyword_idea_metrics.avg_monthly_searches}" '
            f'average monthly searches and "{competition_value}" '
            "competition.\n"
        )

def map_locations_ids_to_resource_names(client, location_ids):
    build_resource_name = client.get_service("GeoTargetConstantService").geo_target_constant_path
    return [build_resource_name(location_id) for location_id in location_ids]

conn = pymysql.connect(host = '***.***.***.***',port=********,database='********',charset='utf8mb4',local_infile=1, user='********',password='********')
cur = conn.cursor()
sql = '''SELECT * FROM `keywordqc`.`keywords`'''
cur.execute(sql)
keywords = np.array(cur.fetchall()).T[1]
conn.close()
with open("client_secret.txt",'r') as f:
    f = json.loads(f.read())
client = GoogleAdsClient.load_from_dict(f)
location_ids = ["1009871"] # Seoul, Korea
language_id = "1000"

main(client,'7688663892',location_ids,language_id,keywords,False)

# with open("keywordidea.csv", 'w', encoding='utf-8-sig') as keywordidea:
#     apicount = 1
#     time.sleep(0.5)

time2 = datetime.datetime.now()
#print(apicount, 'APIs sent')
print(time2 - time1, 'elapsed')
