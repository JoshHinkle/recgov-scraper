import http.client, urllib
import json
import os

conn = http.client.HTTPSConnection("www.recreation.gov")

# pushover_api_token = os.environ.get('PUSHOVER_API_TOKEN')
# pushover_user_key = os.environ.get('PUSHOVER_USER_KEY')

payload = ""

conn.request("GET", "/api/permitinyo/445859/availability?start_date=2023-07-01&end_date=2023-07-31&commercial_acct=false", payload)

res = conn.getresponse()
data = res.read()
data_json = json.loads(data.decode("utf-8"))["payload"]

for date, divisions in data_json.items():
    for division_code, division in divisions.items():
        if division_code in ["44585918", "44585922"] and division["remaining"] > 0 and not division["is_walkup"]:
            if division_code == "44585918":
                location = "Happy Isles"
            elif division_code == "44585922":
                location = "Lyell Canyon"
            print(f"{location} has {division['remaining']} remaining permits on {date}")


conn = http.client.HTTPSConnection("api.pushover.net:443")
conn.request("POST", "/1/messages.json",
  urllib.parse.urlencode({
    "token": 'arxukwp64qvejdaym26uh4h826t4x5',
    "user": 'ugt559h5xqehszhp84thb2inw8q6fo',
    "message": "hello world",
  }), { "Content-type": "application/x-www-form-urlencoded" })
conn.getresponse()
