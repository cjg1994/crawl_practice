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
for num in range(1,32):
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
        content_div=selector.xpath('//div[@class="sdk-trips-container"]')
        if content_div:
            content=content_div[0].xpath('string(.)')
            content=re.sub('[\s+]','',content)
            f.write("第%d篇:%s\n"%(count,article_title))
            f.write(content)
            f.write("\n"+"--"*50+"\n")
            count+=1
        else:
            continue

        time.sleep(2)

    time.sleep(3)
