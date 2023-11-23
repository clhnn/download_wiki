time_code = "2009-2010"
searching_uri = "https://zh.wikipedia.org/zh-tw/*"
from comcrawl import IndexClient
import pandas as pd
import os

searching_uri_dir = searching_uri.replace("/", "-").replace(":", "-").replace("*", "-all")
if not os.path.exists("output"):
    os.makedirs("output")
if not os.path.exists(f"output/{time_code}"):
    os.makedirs(f"output/{time_code}")
if not os.path.exists(f"output/{time_code}/{searching_uri_dir}"):
    os.makedirs(f"output/{time_code}/{searching_uri_dir}")

client = IndexClient([time_code], verbose=True)
success = False
while not success:
    try:
        client.search(searching_uri)
        client.results = (pd.DataFrame(client.results)
                        .sort_values(by="timestamp")
                        .drop_duplicates("urlkey", keep="last")
                        .to_dict("records"))
        pd.DataFrame(client.results).to_csv(f"output/{time_code}/{searching_uri_dir}/index.csv", index=False)
        success = True
    except:
        print("Index Server Response Timeout. Retrying...")

success = False
while not success:
    try:
        client.download()
        success = True
    except:
        print("Download Server Error. Retrying...")