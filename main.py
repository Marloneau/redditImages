import json
import requests
import pandas as pd
import numpy as np

#Reading config/credentials
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


"""res = requests.get("https://oauth.reddit.com/r/shitposting/hot",headers=headers,params={"limit":"100"})
print(res.json()["data"]["children"][0]["data"].keys())"""

data = pd.DataFrame()
params={"limit":100}

pattern_del="(.gif|.png|.jpg)" #Mmaking sure I want those images

subr=["shitposting","ProgrammerHumor"] #List of subreddits I want images from 

for subreddit in subr:
    
    params={"limit":100}
    
    for i in range(2):
        
        res = requests.get("https://oauth.reddit.com/r/" + subreddit + "/hot",headers=headers,params=params)
        
        df=pd.DataFrame()

        for post in res.json()["data"]["children"]:
            df = df.append({
                "title":post["data"]["title"],
                "url":post["data"]["url"],
                "id":post["data"]["id"],
                "kind":post["kind"],
            },ignore_index=True)
        
        last_row = df.iloc[ len(df)-1]

        fullname = last_row["kind"] + "_" + last_row["id"]

        params["after"] = fullname

        filter = df["url"].str.contains(pattern_del)

        df=df[filter]

        data = data.append(df, ignore_index=True)

print(data)





for post in res.json()["data"]["children"]:
    print(post["data"]["url"])


