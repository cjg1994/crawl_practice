#长白山，哈尔滨，...不知道这些景点的页面格式是否相同，如果相同，则传入一个关键字然后获取对应的地点编码，然后去构造url
#长白山游记第一页的URL https://you.ctrip.com/travels/changbaishan268/t3.html
#第二页URL https://you.ctrip.com/travels/changbaishan268/t3-p2.html
#第一页URL最后面改成t3-p1也可以访问

#先直接输入总页数224页，也可以获取页面的元素的值，
#获取这些URL的class="ellipsis"元素的href属性即可获取到每篇游记的正文,并不是标题做了超链接，而是整个DIV就是一个a标签，所以要在a中获取href属性
import requests
import lxml.html
import time
import re
url="https://you.ctrip.com/travels/changbaishan268/t3-p{}.html"
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
}
f=open("xc_changbaishan.txt","a",encoding="utf-8")#可读模式不会创建文件，这里要是可写追加模式
count=1#用来记录篇数
for i in range(1,225):
    trips_url=url.format(i)
    resp=requests.get(trips_url,headers=headers)
    trips_text=resp.text
    selector=lxml.html.fromstring(trips_text)
    articles=selector.xpath('//a[@class="journal-item cf"]/@href')#获取的链接还要与协议、域名做一个拼接
    article_titles=selector.xpath('//dt[@class="ellipsis"]/text()')
    for article_url,article_title in zip(articles,article_titles):
        #这里的article是每个文章的链接
        # print(article)成功，可以获取到链接
        #观察几篇游记的元素格式是否相同，获取游记正文
        f.write("第%d篇:%s\n"%(count,article_title))
        article_url="https://you.ctrip.com"+article_url
        # print(article_url)
        article_resp=requests.get(article_url,headers=headers)
        article_text=article_resp.text
        article_selector=lxml.html.fromstring(article_text)
        #获取class="ctd_content"的元素下的所有文本节点()子节点孙节点)等，看看是否是正文
        #正文似乎在一个个p标签里，不过猜测可能有些会在其他标签中，所以这里直接获取最外层标签下的所有文本
        #貌似有2种结构，一种是class="ctd_content"的DIV下的p标签组成的正文，一种是多个class="ctd_content wtd_content"的DIV组成的正文
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
        # print(article_content)成功获取到，清除一下其中的换行符、空白
        # article_content=re.sub('[\s+\n]','',article_content)
        # 清除所有换行符似乎不太美观，可以选择清除无效空白，但是\s也会匹配到\n的，如果考虑美观的话可以只删除有些文章开头的发表时间那一段的文字，因为那段文字空白太多
        # article_text=re.sub('发表.*?\s+','',article_content)
        #但是文章中可能连着有多个br标签，表示换行，文章中也会连续出现多次换行，可以获取每一个p标签下的所有文本，拼接成正文文章.
        # print(article_content)成功
        f.write(article_content)
        f.write("\n"+"-"*100+"\n")
        count+=1
        time.sleep(1)
        # break
    time.sleep(3)
    #取消循环，爬取2000多篇文章,还没有测试过爬取200多页是否全部成功，但是第一页的10篇文章测试成功爬取
    # break
f.close()
