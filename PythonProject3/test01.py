import requests
from bs4 import BeautifulSoup

# 请求网页
url = "https://www.baidu.com"
res = requests.get(url)
res.encoding = "utf-8"

# 解析网页
soup = BeautifulSoup(res.text, "lxml")

# 提取网页标题
print("网页标题：", soup.title.text)

# 提取所有链接
for a in soup.find_all("a"):
    print(a.text, "→", a["href"])