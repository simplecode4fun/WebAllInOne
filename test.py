

import requests
    

# querystring = {"by":"relevancy","limit":limit,"match_id":match_id,"newest":page_no,"order":"desc","scenario":"PAGE_OTHERS","version":"2"}

payload = ""
headers = {
    "cookie": "REC_T_ID=3cd4a8c4-b8a0-11eb-ac80-b49691342bf6",
    "authority": "shopee.co.id",
    "pragma": "no-cache",
    "cache-control": "no-cache",
    "sec-ch-ua": "^\^"
}

url = "https://shopee.co.id/api/v4/search/search_items"

response = requests.request("GET", url, data=payload, headers=headers)
