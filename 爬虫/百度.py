from urllib.request import urlopen
url="http://www.baidu.com"
result=urlopen(url)
with open("mybaidu.html", mode="w", encoding="utf-8") as f:
    f.write(result.read().decode("utf-8"))
print("over!")