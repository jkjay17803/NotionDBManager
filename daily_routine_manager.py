from dotenv import load_dotenv
import os

import requests

load_dotenv()

NOTION_TOKEN = os.getenv('NOTION_API_KEY')
DATABASE_ID = "255463560c4d804f85dec9eb4396f74b"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

# 1. '미완' 항목 제외하기
url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

query = {
    "filter": {
        "property": "Condition",
        "status": {
            "does_not_equal": "미완"
        }
    }
}
res = requests.post(url, headers=headers, json=query)

if res.status_code != 200:
    print("[!] Error:", res.status_code, res.json())
    exit()

pages = res.json().get("results", [])

# 2. 미완으로 변경
for page in pages:
    page_id = page["id"]
    update_url = f"https://api.notion.com/v1/pages/{page_id}"

    data = {
        "properties": {
            "Condition": {
                "status": {
                    "name": "미완"
                }
            }
        }
    }

    response = requests.patch(update_url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"[+] Updated {page_id} → '미완'")
    else:
        print(f"[!] Failed {page_id}: {response.status_code}, {response.json()}")

print("[+] Update Finished")
exit(0)