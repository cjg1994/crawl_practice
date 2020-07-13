#途牛官网搜索长白山 返回的URL是 https://s.tuniu.com/search_complex/whole-hz-0-%E9%95%BF%E7%99%BD%E5%B1%B1/ 编码的是中文 长白山  但是这个页面没有游记相关内容
#官网主页上找到攻略再点击游记 在页面中间游记内容上方的搜索框中搜索长白山 返回的URL https://trips.tuniu.com/search?q=%E9%95%BF%E7%99%BD%E5%B1%B1
#相关游记约303篇 31页 点击第二页 地址栏URL未变 应该是AJAX加载进来的
#第二页 https://trips.tuniu.com/travels/index/ajax-list?queryKey=%E9%95%BF%E7%99%BD%E5%B1%B1&page=2&limit=10&_=1584006223816
#第三页 https://trips.tuniu.com/travels/index/ajax-list?queryKey=%E9%95%BF%E7%99%BD%E5%B1%B1&page=3&limit=10&_=1584006288807
#去掉时间戳_ 改变page参数就能得到每页游记列表
import requests
import lxml.html
import json
import time
import re
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
}
f=open("tn_changbaishan.txt","a",encoding="utf-8")
count=1
for num in range(1,32):#每个url返回的是json数据，其实这里不必写32，可以根据返回的数据中的键 "data"的值中的rows键的值是否为空来判断是否还有数据，是否还需继续爬取
    url="https://trips.tuniu.com/travels/index/ajax-list?queryKey=%E9%95%BF%E7%99%BD%E5%B1%B1&page={}&limit=10".format(num)
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
        time.sleep(2)
        # break
    time.sleep(3)
    # break
