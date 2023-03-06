from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest
import os
import csv
import json
import math
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse

def run_report(property_id="326395343",date1=""):
    oneday = datetime.timedelta(days=1)
    if date1:
        date1 = parse(date1).date().strftime("%Y-%m-%d")
    else:
        date1 = (datetime.datetime.now().date() - oneday).strftime("%Y-%m-%d")
    date2 = date1
    with open('/home/instinctus/Desktop/run/GA4/DimensionsandMetrics.json','r') as f:
        DimensionsandMetrics = json.loads(f.read())
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/instinctus/Desktop/run/GA4/credentials.json"
    property_id = "326395343"
    client = BetaAnalyticsDataClient()
    
    for DMMT in DimensionsandMetrics['data']:
        responserows = {}
        datalenth = 0
        jsonheads = []
        header = ['date'] + [DM for DM in DMMT['dimensions']] + [DM for DM in DMMT['metrics']]
        for i in range(0,math.ceil(len(DMMT['metrics'])/5)):
            request = RunReportRequest(
                property=f"properties/{property_id}",
                dimensions=[Dimension(name=DM) for DM in DMMT['dimensions']],
                metrics=[Metric(name=MT) for MT in DMMT['metrics'][i*5:(i+1)*5]],
                date_ranges=[DateRange(start_date=date1, end_date=date2)],
            )
            response = client.run_report(request)
            if len(response.rows) > datalenth:
                datalenth = len(response.rows)
            for row in response.rows[:]:
                jsonhead = ''.join([value.value for value in row.dimension_values])
                jsonheads += [jsonhead]
                try:
                    xx = responserows[jsonhead]
                    del xx
                except:
                    responserows[jsonhead] = {}
                responserows[jsonhead]['date'] = date1
                j=1
                for value in row.dimension_values:
                    responserows[jsonhead][header[j]] = value.value
                    j+=1
                k = i*5 + j
                for value in row.metric_values:
                    responserows[jsonhead][header[k]] = value.value
                    k+=1

        json2array = np.zeros(shape=(datalenth,1+len(DMMT['dimensions'])+len(DMMT['metrics'])),dtype=np.dtype)
        jsonheaduniq = []
        for a in jsonheads:
            if a not in jsonheaduniq:
                jsonheaduniq += [a]
        for n in range(0,len(jsonheaduniq)):
            for m in range(0,len(header)):
                try:
                    json2array[n][m] = responserows[jsonheaduniq[n]][header[m]]
                except KeyError:
                    json2array[n][m] = 0
        with open("/home/instinctus/Desktop/run/GA4/" + DMMT['title']+".csv",'w') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(header)
            for row in json2array:
                csv_writer.writerow(row)