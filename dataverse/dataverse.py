import numpy as np
import json
import time
import datetime
from dateutil.parser import parse
import sys
import requests

"""
Environment unique name
    orgdaec40fd
Environment ID
    Default-d7fab9a4-c85b-44d3-97d2-213c0fa1db08
Organization ID
    df5f6d86-ab43-43f9-bff0-77e5f3cd4d33
Web API endpoint
    https://orgdaec40fd.api.crm5.dynamics.com/api/data/v9.2
Discovery endpoint
    https://globaldisco.crm5.dynamics.com/api/discovery/v2.0/Instances
Accept: application/json  
OData-MaxVersion: 4.0  
OData-Version: 4.0
If-None-Match: null
"""

entity = "systemusers?$select=crdd1_name%$top=3 HTTP/1.1"
url = "https://orgdaec40fd.api.crm5.dynamics.com/api/data/v9.2/%s" %(entity)
headers = {
    "Accept": "application/json",
    "OData-MaxVersion": "4.0",
    "OData-Version": "4.0",
    "If-None-Match": "null",
    "Content-Type": "application/json",
}
# params = {
#     "access_token":token,
#     "fields":""
# }
response = requests.get(url,headers=headers,)
print(response.text)