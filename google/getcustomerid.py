import json
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# [START list_accessible_customers]
def main(client):
    customer_service = client.get_service("CustomerService")

    accessible_customers = customer_service.list_accessible_customers()
    result_total = len(accessible_customers.resource_names)
    print(f"Total results: {result_total}")

    resource_names = accessible_customers.resource_names
    for resource_name in resource_names:
        print(f'Customer resource name: "{resource_name}"')
    # [END list_accessible_customers]
    
with open("client_secret.txt",'r') as f:
    f = json.loads(f.read())
client = GoogleAdsClient.load_from_dict(f)

main(client=client)