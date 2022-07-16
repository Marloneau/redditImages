import json
import requests

with open("config.json","r") as f:
    config=json.load(f)

auth = requests.auth.HTTPBasicAuth(config["CLIENT_ID"],config["TOKEN"])

data={
    "grant_type":"password",
    "username": config["USERNAME"],
    "password":config["PASSWORD"]
}

headers = {"User-Agent":"MyBot/0.0.1"}

res = requests.post(
    "https://www.reddit.com/api/v1/access_token",
    auth=auth,
    data=data,
    headers=headers
    )

TOKEN = res.json()["access_token"]

headers = {**headers, **{"Authorization": f"bearer {TOKEN}"}} 

#requests.get("https://oauth.reddit.com/api/avi/me",headers=headers)

res = requests.get("https://oauth.reddit.com/r/shitposting/hot",headers=headers,params={"limit":"3"})
print(res.json()["data"]["children"][0]["data"].keys())


for post in res.json()["data"]["children"]:
    print(post["data"]["url"])


