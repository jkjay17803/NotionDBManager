from dotenv import load_dotenv
import os
import json
import requests
from datetime import date, timedelta
import calendar
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_API_KEY")
DATABASE_ID = "25c463560c4d80bf989be04203a6891e"
today = date.today()
year, month = today.year, today.month

# 이번 달 마지막 날
last_day = calendar.monthrange(year, month)[1]

# 금, 토, 일 일(day)만 저장
weekend_days = [
    day
    for day in range(1, last_day + 1)
    if date(year, month, day).weekday() in (4, 5, 6)  # 금=4, 토=5, 일=6
]


url = "https://api.notion.com/v1/pages"  # 페이지 생성 URL로 변경

# 2. 헤더 설정
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",  # 여기에 토큰 입력
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# 3. 데이터베이스 ID
database_id = "25c463560c4d80bf989be04203a6891e"  # 여기에 데이터베이스 ID 입력

# 4. 페이지 데이터
for days in weekend_days:
    data = {
        "parent": { "database_id": database_id },
        "properties": {
            "내용": {
                "title": [
                    {
                        "text": { "content": "카페 알바" }
                    }
                ]
            },
            "날짜": {
                "date": {
                    "start": f"2025-09-{days:02d}T11:00:00",
                    "end": f"2025-09-{days:02d}T14:59:00"
                }
            },
            "우선순위": {
                "select": {
                    "name":"높음"
                }
            },
            "카테고리": {
                "select": {
                    "name":"카페"
                }
            }
        }
    }

    # 5. 요청 보내기
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # 6. 결과 확인
    if response.status_code == 200:
        print("데이터가 성공적으로 추가되었습니다!")
        print(response.json())
    else:
        print("데이터 추가 실패:", response.status_code)
        print(response.text)