#搜索雪乡返回的URL https://s.tuniu.com/search_complex/whole-hz-0-%E9%9B%AA%E4%B9%A1/  对比长白山，其实就是whole-hz-0-XXX
#没有用要在主页中先点击游记 在页面中间的那个搜索框中搜索雪乡
#https://trips.tuniu.com/ 页面中间搜索雪乡 https://trips.tuniu.com/search?q=%E9%9B%AA%E4%B9%A1 对比长白山也就是参数q的改变
#24页
#假设传给我一个地名，一个游记总页数，然后就可以进行爬取
import requests
import lxml.html
import json
import time
import re

position="雪乡" #地名，因为网站自己会对url做一个编码，所以自己不用调用urllib.quote进行编码
pages=25  #其实这个参数值可以从请求每一页列表时返回的json数据中data键中的totalCount键对应的值中获取
filename="tn_xuexiang.txt"

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
}
f=open(filename,"a",encoding="utf-8")
count=1
for num in range(1,pages):#每个url返回的是json数据，其实这里不必写32，可以根据返回的数据中的键 "data"的值中的rows键的值是否为空来判断是否还有数据，是否还需继续爬取
    url="https://trips.tuniu.com/travels/index/ajax-list?queryKey={}&page={}&limit=10".format(position,num)
    resp=requests.get(url,headers=headers)
    text=resp.text
    trips=json.loads(text)
    trips_list=trips["data"]["rows"]
    for trip in trips_list:
        article_title=trip["name"]
        article_url="https://www.tuniu.com/trips/"+str(trip["id"])
        article_response=requests.get(article_url,headers=headers)
        article_text=article_response.text
        selector=lxml.html.fromstring(article_text)
        # content_div=selector.xpath('//div[@class="sdk-trips-container"]')[0] #有个页面不存在导致这里抛出 改成
        content_div=selector.xpath('//div[@class="sdk-trips-container"]')
        if content_div:
            content=content_div[0].xpath('string(.)')
            content=re.sub('[\s+]','',content)
            f.write("第%d篇:%s\n"%(count,article_title))
            f.write(content)
            f.write("\n"+"--"*50+"\n")
            count+=1  #第27页的时候有一篇页面不存在。要设置一个判断，如果没有数据就跳过；
        else:
            continue
        # print(article_title)
        # print(content)
        time.sleep(5)
        # break

    # break
