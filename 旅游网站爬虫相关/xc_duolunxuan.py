import requests
import lxml.html
import time
import json
import csv
import re
url="https://you.ctrip.com/searchsite/travels/?query=%E5%A4%9A%E4%BC%A6%E5%8E%BF&isAnswered=&isRecommended=&publishDate=&PageNo=1"
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
}
response=requests.get(url,headers=headers)
selector=lxml.html.fromstring(response.text)
total_pages=int(selector.xpath('//div[@class="desNavigation cf"]/p/span/a[3]/text()')[0])
f=open("duolun_comments.txt","a",encoding="utf-8")

for num in range(1,total_pages+1):
    url="https://you.ctrip.com/searchsite/travels/?query=%E5%A4%9A%E4%BC%A6%E5%8E%BF&isAnswered=&isRecommended=&publishDate=&PageNo={}".format(num)
    response=requests.get(url,headers=headers)
    selector=lxml.html.fromstring(response.text)
    articles=selector.xpath('//ul[@class="youji-ul cf"]/li[@class="cf"]')
    for article in articles:
        link=article.xpath('a[@class="pic"]/@href')[0]
        travel_id=link.split('/')[-1].split('.')[0]
        article_url="https://you.ctrip.com"+link
        article_selector=lxml.html.fromstring(requests.get(article_url,headers=headers).text)
        article_main=article_selector.xpath('//div[@class="ctd_main_body"]')
        if article_main:
            article_content=re.sub('[\n\s]+','',article_main[0].xpath('string(.)'))
        else:
            article_content="不存在游记正文"

        f.write("游记正文:"+article_content)
        f.write("\n")
        f.write("评论:"+"\n")
        number=1
        while True:
            comment_url="https://you.ctrip.com/TravelSite/Home/TravelReplyListHtml?TravelId={}&IsReplyRefresh=0&ReplyPageNo={}&ReplyPageSize=10&_={}".format(int(travel_id),number,int(time.time()))
            comment_html=json.loads(requests.get(comment_url,headers=headers).text)["Html"]
            time.sleep(1)
            if not comment_html:
                f.write('--'*70+"\n")
                break
            comment_selector=lxml.html.fromstring(comment_html.replace("\r\n",""))
            comments=comment_selector.xpath('//p[@class="ctd_comments_text"]')
            users=comment_selector.xpath('//a[@class="ctd_comments_username"]')
            for i in range(len(users)):
                if not users[i].xpath('text()'):
                    f.write("用户："+''+":"+comments[i].xpath('string(.)').strip()+"\n")
                else:
                    f.write("用户："+users[i].xpath('text()')[0]+":"+comments[i].xpath('string(.)').strip()+"\n")
            number=number+1
    time.sleep(2)
