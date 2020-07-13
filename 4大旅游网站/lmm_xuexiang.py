#http://www.lvmama.com/trip/search?kw=%E9%9B%AA%E4%B9%A1 雪乡游记的URL 对比长白山，也就是kw变成了雪乡
#但是也会遇到一个问题 远程主机强制关闭了一个现有的连接，尝试着再把time.sleep的值改大一点 之后成功爬取
import requests
import lxml.html
import time
import re

keyword="雪乡"#查询的地点
pages=16#页面上看到的页数
filename="lmm_xuexiang.txt"#记录的文件名

url="http://www.lvmama.com/trip/search/ajaxGetTrip" #请求的地址和长白山是一样的
num=1
data={
    "page":num,
    "status":"",
    "keyword":keyword
}
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
}
f=open(filename,"a",encoding="utf-8")
count=1 #记录篇数
for i in range(1,pages):
    num=i
    resp=requests.post(url,data=data,headers=headers)
    text=resp.text
    selector=lxml.html.fromstring(text)
    trips_url=selector.xpath('//div[@class="title"]/a/@href')
    for article_url in trips_url:
        article_resp=requests.get(article_url,headers=headers)
        article_text=article_resp.text
        article_selector=lxml.html.fromstring(article_text)
        article_title=article_selector.xpath('//p[@class="etf-text"]/@title')[0]
        article_content=article_selector.xpath('//div[@class="ebm-post ebm-article"]')[0].xpath('string(.)')
        article_content=re.sub("[\s+]","",article_content)
        f.write("第%d篇:%s\n"%(count,article_title))
        f.write(article_content)
        f.write("\n"+"-"*100+"\n")
        count=count+1
        time.sleep(10)
        # break
    # break
f.close()
