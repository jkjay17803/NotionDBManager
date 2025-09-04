import datetime

from dotenv import load_dotenv
import os
import json
import requests
from datetime import date, timedelta,timezone
import calendar
from dataclasses import dataclass

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_API_KEY")
DATABASE_ID = "25c463560c4d80bf989be04203a6891e"

title = str(input("Enter the title: "))
d = input("Enter the days\nMon:0 Tue:1 Wed:2 Thu:3 Fri:4 Sat:5 Sun:6\n:")
lst = list(map(int, d.split()))

data = input("Enter the startTime: ")
start = [int(x) for x in data.split(":")]
data = input("Enter the endTime: ")
end = [int(x) for x in data.split(":")]

start[0] -= 9
end[0] -= 9

today = date.today()
m = today.month
year, month = today.year, today.month

# 이번 달 마지막 날
last_day = calendar.monthrange(year, month)[1]

# 금, 토, 일 일(day)만 저장
weekend_days = [
    day
    for day in range(1, last_day + 1)
    if date(year, month, day).weekday() in (lst)  # 금=4, 토=5, 일=6
]

priority = int(input("Enter the priority\nHigh: 0 Medium: 1 Low: 2\n:"))
if priority == 0:
    priority = "높음"
elif priority == 1:
    priority = "중간"
elif priority == 2:
    priority = "낮음"


category = int(input("Enter the category\nPersonal: 0 || Cafe: 1 || Study:2 || University: 3 || Love: 4 || Work: 5\n:"))
if category == 0:
    category = "개인"
elif category == 1:
    category = "카페"
elif category == 2:
    category = "공부"
elif category == 3:
    category = "대학"
elif category == 4:
    category = "연애"
elif category == 5:
    category = "직장"


#확인
print("\n\n=====[ 현재 설정 ]======")
print(f"제목: {title}")
print(f"요일코드: {d}")
print(f"시간: {start[0]+9}:{start[1]} ~ {end[0]+9}:{end[1]}")
print(f"우선도 코드: {priority}")
print(f"카테고리 코드: {category}")
print("\n입니다. 새로운 항목으로 자동 생성할까요? (y/n)")

yn = input(":")
if yn == "n" or yn == "ㅜ":
    print("지금까지의 내용을 모두 잊고 종료합니다.")
    exit(0)

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
                        "text": { "content": f"{title}" }
                    }
                ]
            },
            "날짜": {
                "date": {
                    "start": f"2025-{m}-{days:02d}T{int(start[0]):02d}:{int(start[1]):02d}:00",
                    "end": f"2025-{m}-{days:02d}T{int(end[0]):02d}:{int(end[1]):02d}:00"
                }
            },
            "우선순위": {
                "select": {
                    "name":f"{priority}"
                }
            },
            "카테고리": {
                "select": {
                    "name":f"{category}"
                }
            }
        }
    }

    # 5. 요청 보내기
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # 6. 결과 확인
    if response.status_code == 200:
        print("[+] 데이터가 성공적으로 추가되었습니다!")
    else:
        print("[!] 데이터 추가 실패:", response.status_code)
        print(response.text)