import requests
from bs4 import BeautifulSoup
import time

# 配置
keyword = "git"
max_page = 5
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

for page in range(max_page):
    url = f"https://www.baidu.com/s?wd={keyword}&pn={page*10}"
    print(f"\n===== 第 {page+1} 页 =====")
    
    try:
        res = requests.get(url, headers=headers, timeout=15)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "lxml")

        items = soup.find_all("div", class_="result")
        for item in items:
            try:
                title = item.find("h3").get_text(strip=True)
                link = item.find("a")["href"]
                print(f"标题：{title}")
                print(f"链接：{link}\n")
            except:
                continue

        time.sleep(2)

    except Exception as e:
        print("出错：", e)