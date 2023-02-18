import http.client
import json

conn = http.client.HTTPSConnection("www.recreation.gov")

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