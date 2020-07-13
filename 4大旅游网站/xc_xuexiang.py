#长白山，哈尔滨，...不知道这些景点的页面格式是否相同，如果相同，则传入一个关键字然后获取对应的地点编码，然后去构造url
#长白山游记第一页的URL https://you.ctrip.com/travels/changbaishan268/t3.html
#第二页URL https://you.ctrip.com/travels/changbaishan268/t3-p2.html
#第一页URL最后面改成t3-p1也可以访问

#雪乡游记的URL https://you.ctrip.com/travels/xuexiang1445063.html 只是后面的文件名不同
#猜测有一个映射存储了 雪乡-->xuexiang1445063 长白山-->changbaishan268
#雪乡第二页游记请求的URL是 https://you.ctrip.com/travels/xuexiang1445063/t3-p2.html  和长白山格式是相同的
#现在只要获取雪乡和长白山分别对应的id就行了 发现页面中有个旅游攻略导航DIV 一个ul里面的li标签是一个个地点，做了超链接有href属性，这里虽然能获取但是观察之后发现不太好
#应该从输入雪乡点击搜索这里观察去请求了哪些页面，得到雪乡对应的id
#GET请求的url是https://m.ctrip.com/restapi/h5api/globalsearch/search?action=online&source=globalonline&keyword=%E9%9B%AA%E4%B9%A1&t=1584162320224
#其中 keyword="雪乡"  发现把keyword改成长白山也可以获取长白山的数据  返回的json数据的键data对应的值中可以获取到id 拼接上中文拼音就可以得到上面的url了
import requests
import lxml.html
import time
import re
import json
keyword="雪乡"
pages=11 #其实是64页  这里尝试获取一下10页的数据试试是否成功
filename="xc_xuexiang.txt"
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
}
forward_url="https://m.ctrip.com/restapi/h5api/globalsearch/search?action=online&source=globalonline&keyword={}".format(keyword)
forward_resp=requests.get(forward_url,headers=headers)
forward_text=forward_resp.text
forward_json=json.loads(forward_text)
forward_id=forward_json["data"][0]["id"]
#接着要拼接雪乡对应的拼音xuexiang 得到游记   但是更好的方法是上面的foward_json中有个url键对应的是每个地方的主页面，在这个页面中点击游记按钮才会转到游记页面
#所以 雪乡 对应 xuexiang 应该观察点击游记按钮之后的请求中获取
#后来发现雪乡主页面URL是https://you.ctrip.com/place/xuexiang1445063.html  去掉雪乡的拼音也是可以访问成功的
#雪乡游记页面URL是 https://you.ctrip.com/travels/1445063.html
#在于路径中place 和 travels 的区别 所以构造游记页面的url可以是 https://you.ctrip.com/travels/ + id +.html
travels_url="https://you.ctrip.com/travels/{}".format(forward_id)#这里不要在尾部添加.html 就当是一个字符串，是为了构造下面每一页游记列表的URL而存在的
# print(travels_url)
f=open("xc_xuexiang.txt","a",encoding="utf-8")
count=1
for i in range(1,pages):
    trips_url=travels_url+"/t3-p{}.html".format(i)
    # print(trips_url)#成功构造每页游记列表的URL
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
        time.sleep(5)
        # break
    # time.sleep(2)
    # break
f.close()
