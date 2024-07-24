from typing import Dict
import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd

def extract_article_details(url: str) -> Dict[str, str]:
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Unable to retrieve article"}

    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1').get_text() if soup.find('h1') else "No title"
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    content = "\n".join([p.get_text() for p in soup.find_all('p')])
    source = url.split('/')[2]

    details = {
        "구분1": "해외사업자",  # 추후에 더 세부적인 분류를 위해 수정 가능
        "구분2": "노키아",      # 추후에 더 세부적인 분류를 위해 수정 가능
        "게시일": date,
        "내용": content,
        "source": source,
        "링크": url
    }
    return details

def save_to_excel(data: Dict[str, str], filename: str):
    df = pd.DataFrame([data])
    df.to_excel(filename, index=False)

# 예시 URL
url = "https://www.mobileworldlive.com/telefonica/telefonica-taps-nokia-for-sa-5g-api-boost/"
details = extract_article_details(url)

# 결과를 엑셀 파일로 저장
filename = "article_details.xlsx"
save_to_excel(details, filename)
print(f"Details saved to {filename}")

# 저장된 엑셀 파일을 확인하기 위해 출력
print(pd.read_excel(filename))
