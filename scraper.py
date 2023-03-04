import http.client, urllib
import json
import os
import collections
import time, datetime

pushover_api_token = os.environ.get('PUSHOVER_API_TOKEN', "nonesuch")
pushover_user_key = os.environ.get('PUSHOVER_USER_KEY', "nonesuch")

def send_notification(payload):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": pushover_api_token,
        "user": pushover_user_key,
        "message": payload,
    }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

conn = http.client.HTTPSConnection("www.recreation.gov")

old_happy_isles_payload = ""
old_lyell_payload = ""

while True:
    print(f"Trying in 10 seconds (currently {datetime.datetime.now()})")
    time.sleep(10)
    payload = ""
    available = collections.defaultdict(list)

    
    for date in ["2023-07-01", "2023-08-01"]:
        conn.request("GET", f"/api/permitinyo/445859/availability?start_date={date}&commercial_acct=false", payload)
        res = conn.getresponse()
        data = res.read()
        data_json = json.loads(data.decode("utf-8"))["payload"]

        for date, divisions in data_json.items():
            for division_code, division in divisions.items():
                if division_code in ["44585918", "44585922"] and division["remaining"] > 0 and not division["is_walkup"] and division["remaining"] == division["total"]:
                    available[division_code].append((date, division["remaining"]))


    happy_isles_dates = ", ".join([f"{ent[1]} spots on {ent[0]}" for ent in available["44585918"]])
    happy_isles_payload = f"Happy Isles Permits Available: {happy_isles_dates}"
                

    lyell_dates = ", ".join([f"{ent[1]} spots on {ent[0]}" for ent in available["44585922"]])
    lyell_payload = f"Lyell Canyon Permits Available: {lyell_dates}"


    if happy_isles_payload==old_happy_isles_payload:
        if lyell_payload==old_lyell_payload:
            continue

    
    old_lyell_payload = lyell_payload
    old_happy_isles_payload=happy_isles_payload

    for dates, payload in [(available["44585918"], happy_isles_payload), (available["44585922"], lyell_payload)]:
        if dates: 
            print(f"Sending notifications... {payload}")
            send_notification(payload=payload)
    
    
    
    
