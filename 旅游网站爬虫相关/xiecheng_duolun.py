#搜索多伦县游记的第一页url https://you.ctrip.com/searchsite/travels/?query=%E5%A4%9A%E4%BC%A6%E5%8E%BF&isAnswered=&isRecommended=&publishDate=&PageNo=1
#将PageNo=1改成2就得到第二页的游记了
#抓取每一页10篇游记的url
#访问每一篇游记抓取评论
#第一篇游记的评论https://you.ctrip.com/TravelSite/Home/TravelReplyListHtml?TravelId=3007211&IsReplyRefresh=0&ReplyPageNo=1&ReplyPageSize=10&_=1580725506233
#第二篇游记的评论https://you.ctrip.com/TravelSite/Home/TravelReplyListHtml?TravelId=3199599&IsReplyRefresh=0&ReplyPageNo=1&ReplyPageSize=10&_=1580725651147
#发现是TravelId不同 可以从第一步获取的url里面抽取得到TravelId
#第三篇评论比较多的游记url
#https://you.ctrip.com/TravelSite/Home/TravelReplyListHtml?TravelId=1871556&IsReplyRefresh=0&ReplyPageNo=1&ReplyPageSize=10&_=1580725795973
#点击下一页的评论发现又会请求一个url
#https://you.ctrip.com/TravelSite/Home/TravelReplyListHtml?TravelId=1871556&IsReplyRefresh=0&ReplyPageNo=2&ReplyPageSize=10&_=1580725850793
# 只是ReplayPageNo参数不同
#如果把ReplayPageNo改的比较大，得到的是{"RetCode":1,"Html":"","ErrorMessage":null,"AdditionalData":null} 里面就没有评论数据了
import requests
import lxml.html
import time
import json
import csv
import re
url="https://you.ctrip.com/searchsite/travels/?query=%E5%A4%9A%E4%BC%A6%E5%8E%BF&isAnswered=&isRecommended=&publishDate=&PageNo=1"
#当把PageNo参数增大到一定数值时，页面是有的，但是游记会显示成0
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
}
response=requests.get(url,headers=headers)
selector=lxml.html.fromstring(response.text)
total_pages=int(selector.xpath('//div[@class="desNavigation cf"]/p/span/a[3]/text()')[0])
# url_list=[]
f=open("duolun_comments.txt","a",encoding="utf-8")
# writer=csv.DictWriter(f,fieldnames=["username","comment"])
# writer.writeheader()
for num in range(1,total_pages+1):
    url="https://you.ctrip.com/searchsite/travels/?query=%E5%A4%9A%E4%BC%A6%E5%8E%BF&isAnswered=&isRecommended=&publishDate=&PageNo={}".format(num)
    response=requests.get(url,headers=headers)
    selector=lxml.html.fromstring(response.text)
    articles=selector.xpath('//ul[@class="youji-ul cf"]/li[@class="cf"]')
    # print(len(articles))获取到每篇游记了 接着获取其中的链接
    for article in articles:
        link=article.xpath('a[@class="pic"]/@href')[0]
        travel_id=link.split('/')[-1].split('.')[0]#得到TravelId用于之后评论url的构造
        article_url="https://you.ctrip.com"+link #得到每篇游记的url
        # print(article_url)
        article_selector=lxml.html.fromstring(requests.get(article_url,headers=headers).text)
        article_main=article_selector.xpath('//div[@class="ctd_main_body"]') #但是这里会取出乱七八糟的东西，要取出此标签下的所有p标签 后来发现有些文章也不是写在p标签下的 还是直接取这个标签下所有的文字吧
        if article_main:
            # article_content=article_main[0].xpath('string(.)') #还要考虑有些游记是没有主文章的，只有图片
            # article_content=re.sub('\s+','',''.join(article_main[0].xpath('.//p/text()'))) #这里需要加个. 表示当前节点 不然是错误的
            article_content=re.sub('[\n\s]+','',article_main[0].xpath('string(.)'))
        else:
            article_content="不存在游记正文"
        # print(article_content)
        f.write("游记正文:"+article_content)
        f.write("\n")
        f.write("评论:"+"\n")
        number=1
        while True:
            comment_url="https://you.ctrip.com/TravelSite/Home/TravelReplyListHtml?TravelId={}&IsReplyRefresh=0&ReplyPageNo={}&ReplyPageSize=10&_={}".format(int(travel_id),number,int(time.time()))
            comment_html=json.loads(requests.get(comment_url,headers=headers).text)["Html"]
            time.sleep(1)
            if not comment_html: #循环为什么没被终止 num=1的初始化要在循环之外 修改之后测试成功
                f.write('--'*70+"\n")
                break
            comment_selector=lxml.html.fromstring(comment_html.replace("\r\n",""))
            # print(comment_selector)
            comments=comment_selector.xpath('//p[@class="ctd_comments_text"]') #有些评论p标签下的文本节点比较多，/text()是把该标签下的子节点的文本全都取出(不包含孙节点)
            users=comment_selector.xpath('//a[@class="ctd_comments_username"]') #为什么y有些文章会超出范围
            # print(len(users),len(comments))
            # print(comments)
            # comment_list=[]
            for i in range(len(users)):#因为评论文本节点长度的不确定性，这里的长度使用users
                if not users[i].xpath('text()'):
                    f.write("用户："+''+":"+comments[i].xpath('string(.)').strip()+"\n")
                else:
                    f.write("用户："+users[i].xpath('text()')[0]+":"+comments[i].xpath('string(.)').strip()+"\n") #居然出现有用户空白的用户名 这里就会报错
                # comment_dict={}
                # comment_dict["username"]=users[i]
                # comment_dict["comment"]=re.sub('[\n\s]+','',comments[i])
                # print(comment_dict["comment"],comment_dict["username"])
                # comment_list.append(comment_dict)
            # writer.writerow({"article_content":article_content})
            # writer.writeheader()
            # writer.writerows(comment_list)
            # comment_list=comment_selector.xpath('//p[@class="ctd_comments_text"]/text()')
            # print(comment_list)
            # print(link,travel_id) 成功抓取到
            # url_list.append(link)#每一页10篇游记的url都加进了url_list
            number=number+1
        # break
    time.sleep(2)
    # break
# print(len(url_list))60个url都能获取到
