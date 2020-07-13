
import requests
import lxml.html
import time
import re
url="https://you.ctrip.com/travels/changbaishan268/t3-p{}.html"
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
}
f=open("xc_changbaishan.txt","a",encoding="utf-8")
count=1
for i in range(1,225):
    trips_url=url.format(i)
    resp=requests.get(trips_url,headers=headers)
    trips_text=resp.text
    selector=lxml.html.fromstring(trips_text)
    articles=selector.xpath('//a[@class="journal-item cf"]/@href')
    article_titles=selector.xpath('//dt[@class="ellipsis"]/text()')
    for article_url,article_title in zip(articles,article_titles):

        f.write("第%d篇:%s\n"%(count,article_title))
        article_url="https://you.ctrip.com"+article_url

        article_resp=requests.get(article_url,headers=headers)
        article_text=article_resp.text
        article_selector=lxml.html.fromstring(article_text)

        mode_1=article_selector.xpath('//div[@class="ctd_content"]')
        mode_2=article_selector.xpath('//div[@class="ctd_content wtd_content"]')
        if mode_1:
            article_content=mode_1[0].xpath('string(.)')
            article_content=re.sub('[\s+\n]','',article_content)
        else:
            article_content=""
            for part in mode_2:
                div_text=part.xpath('string(.)')
                article_content=article_content+re.sub('[\s+]','',div_text)

        f.write(article_content)
        f.write("\n"+"-"*100+"\n")
        count+=1
        time.sleep(1)

    time.sleep(3)

f.close()
