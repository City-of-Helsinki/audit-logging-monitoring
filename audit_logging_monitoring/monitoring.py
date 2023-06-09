
import datetime
from django.http import JsonResponse

from audit_logging_monitoring.documents import AuditLogDocument
from django.conf import settings
import requests
import json
import pytz


def main(request):
    
    return JsonResponse({'response':"ElasticCloud audit log service OK"})


def get_entries(date_now, date_yesterday):
    s = AuditLogDocument.search().query('range', **{'@timestamp': {'gte': date_yesterday, 'lte': date_now}}).sort('-@timestamp')
    return s

def add_entry(date_now):
    url = "https://" + str(settings.ELASTICSEARCH_HOST) + "/" + str(settings.ELASTICSEARCH_APP_AUDIT_DATA_STREAM) + "/_doc/?pretty"
    data = {"@timestamp": date_now, "message": "Entry added"}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(url, data=json.dumps(data), headers=headers, auth=(str(settings.ELASTICSEARCH_USERNAME), str(settings.ELASTICSEARCH_PASSWORD)))
    return response

def monitor(request):
    date_now = datetime.datetime.now((pytz.timezone('Europe/Helsinki'))).strftime("%Y-%m-%dT%H:%M:%SZ")
    date_yesterday = (datetime.datetime.now((pytz.timezone('Europe/Helsinki'))) - datetime.timedelta(1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    found = False
    

    try:

        r = add_entry(date_now)
        print(r.text)
        if r.status_code != 201:
            raise Exception(r.text)

    except Exception as err:
        print("Exception occured when saving new entry to elasticsearch:", err)
        return JsonResponse(status=500, data={'response':"Error saving new entry to ElasticSearch"})
    

    try:
        s = get_entries(date_now, date_yesterday)
        
    except Exception as err: 
        print("Error getting entry from elasticsearch:", err)
        return JsonResponse(status=500, data={'response':"Error getting entry from ElasticSearch"})

    for hit in s:

        if not found:
            last_entry = hit

        found = True

        print(
            "Category name : {}, Created at - {}".format(hit.message, hit['@timestamp'])
        )

    if found == False:
        print("Empty")
        return JsonResponse(status=500, data={'response':"No entry has been found"})

    return JsonResponse({'response':"ElasticCloud audit log service OK, last entry " + last_entry['@timestamp']})