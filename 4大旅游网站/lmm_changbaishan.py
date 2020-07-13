#游记查询主页面的URL http://www.lvmama.com/trip/
#查询长白山相关游记的URL http://www.lvmama.com/trip/search/?kw=%E9%95%BF%E7%99%BD%E5%B1%B1  这里编码的中文是 长白山
#游记一共有19页 点击第二页URL并未改变，应该是通过AJAX异步加载的
#找到真正请求的资源
#请求的URL http://www.lvmama.com/trip/search/ajaxGetTrip  POST方法
#请求的参数
# page:3
# status:
# keyword:长白山
#爬取所有文章时出现了3个错误
#ConnectionResetError: [WinError 10054] 远程主机强迫关闭了一个现有的连接。
#urllib3.exceptions.ProtocolError: ('Connection aborted.', ConnectionResetError(10054, '远程主机强迫关闭了一个现有的连接。', None, 10054, None))
#requests.exceptions.ConnectionError: ('Connection aborted.', ConnectionResetError(10054, '远程主机强迫关闭了一个现有的连接。', None, 10054, None))
#爬取了77篇就停止了，应该有接近140篇 怀疑是访问过于频繁被远程主机强制断开连接
#果然如此 将time.sleep(2)改成5就没报错了
import requests
import lxml.html
import time
import re
url="http://www.lvmama.com/trip/search/ajaxGetTrip"
num=1
data={
    "page":num,
    "status":"",
    "keyword":"长白山"
}
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
}
f=open("lmm_changbaishan.txt","a",encoding="utf-8")
count=1 #记录篇数
for i in range(1,20):
    num=i
    resp=requests.post(url,data=data,headers=headers)
    # print(resp) 200测试成功
    text=resp.text
    selector=lxml.html.fromstring(text)
    trips_url=selector.xpath('//div[@class="title"]/a/@href')
    # print(trips_url) 成功获取到一页7个url
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
        time.sleep(5)

    #第一页的7篇游记爬取成功，取消循环可以爬取所有页游记，还未测试
    # break
f.close()
