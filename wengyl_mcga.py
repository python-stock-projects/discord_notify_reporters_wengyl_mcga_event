'''
整合discord 工商時報-翁毓嵐的群組，以關鍵字「同步買超」or「攻高」查找最新的google新聞，
並且將新聞發送到discord群組中。

'''

import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_google_news():
    # 搜尋關鍵字「同步買超 OR 攻高」
    url = f'https://news.google.com/search?q=%22%E5%90%8C%E6%AD%A5%E8%B2%B7%E8%B6%85%22%20OR%20%22%E6%94%BB%E9%AB%98%22%20%20when%3A4h&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup)
    # return soup

    news_list = []
    for item in soup.find_all("article", class_="IFHyqb"): # 更新的 Google 新聞項目 class
        title_tag = item.find("a", class_="JtKRv")
        title = title_tag.text if title_tag else "No title" # 標題
        link = title_tag["href"] if title_tag else "No link" # 連結
        if link.startswith("."):
            link = "https://news.google.com" + link[1:]
        source_tag = item.find("div", class_="vr1PYe")
        source = source_tag.text if source_tag else "No source" # 來源
        date_tag = item.find("time", class_="hvbAAd")
        date = date_tag.text if date_tag else "No date" # 日期


        news_list.append({
            "title": title,
            "link": link,
            "source": source,
            "date": date
        })
    
    return news_list

def check_news():

    new_news = get_google_news()

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   
    if new_news:
        # 處理新公告，例如發送通知
        print(f"有新的news - {current_time}")
  
    else:
        print(f"沒有新的news - {current_time}")

    return new_news

if __name__ == "__main__":
    check_news()