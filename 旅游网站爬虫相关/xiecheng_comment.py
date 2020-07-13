#抓取携程上关于拉市海的评论
import requests
import lxml.html
import csv
import re
keyword="拉市海"
#携程首页url https://www.ctrip.com/?sid=155952&allianceid=4897&ouid=index
#搜索拉市海后的url https://you.ctrip.com/sight/lashihai32/19738.html#ctm_ref=www_hp_his_lst
#搜索九寨沟的url
#每一页评论请求的url都是一样的https://you.ctrip.com/destinationsite/TTDSecond/SharedView/AsynCommentView
#post请求的参数发生变化
# poiID:80565
# districtId:100007
# districtEName:Lijiang
# pagenow:4  这个参数会随着评论页增加
# order:3.0
# star:0.0
# tourist:0.0
# resourceId:19738
# resourcetype:2
url="https://you.ctrip.com/destinationsite/TTDSecond/SharedView/AsynCommentView"
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    "cookie":"_RSG=1DapWDWwQO7vB5LlmoFUaB; _RGUID=761aea03-60ce-4341-b91e-3f2c2f5452f9; _ga=GA1.2.201341775.1505226063; __guid=246721932.1036759855143674100.1556119532870.2776; _RDG=28195a5fd6940b29642962df9b36b39cde; MKT_CKID=1575473582669.5kr0b.0hq7; _abtest_userid=4d4ca40d-9d54-49d6-847b-feb2f33ad0fb; _RF1=60.181.145.13; Session=SmartLinkCode=U155952&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; MKT_CKID_LMT=1580711128393; _gid=GA1.2.1167747573.1580711128; MKT_Pagesource=PC; ASP.NET_SessionSvc=MTAuMTUuMTI4LjI4fDkwOTB8b3V5YW5nfGRlZmF1bHR8MTU3NjUxMTI1MzEwMA; appFloatCnt=1; Union=OUID=index&AllianceID=4897&SID=155952&SourceID=&createtime=1580712123&Expires=1581316922792; manualclose=1; gad_city=3ad910cf00add35bd27e5896bdb9d0d7; login_uid=AC9DB200A824F4F479E50CC7A15CED3B; login_type=0; _gat=1; monitor_count=15; _bfa=1.1489758883826.37wksg.1.1575473578256.1580711125466.5.20; _bfs=1.16; _jzqco=%7C%7C%7C%7C1580711142781%7C1.1549372167.1575473582676.1580714488703.1580714517446.1580714488703.1580714517446.undefined.0.0.14.14; __zpspc=9.5.1580712122.1580714517.11%232%7Csp0.baidu.com%7C%7C%7C%25E6%2590%25BA%25E7%25A8%258B%7C%23; _bfi=p1%3D100101991%26p2%3D290530%26v1%3D20%26v2%3D19",
    "origin":"https://you.ctrip.com"
}
#首先测试一下抓取第四页的10条评论
data={
    "poiID":80565,
    "districtId":100007,
    "districtEName":"Lijiang",
    "pagenow":4,
    "order":3.0,
    "star":0.0,
    "tourist":0.0,
    "resourceId":19738,
    "resourcetype":2
}
response=requests.post(url,headers=headers,data=data)
# print(response.text)
#抓取出评论主体
text=response.text
#得到html树
selector=lxml.html.fromstring(text)
#返回的数据并不像浏览器上直接看到的那样，返回的直接是10个div 而没有外层的id=sightcommentbox的div
# comments=selector.xpath('//div[@id="sightcommentbox"]/div[@class="comment_single"]')
comments=selector.xpath('//div[@class="comment_single"]')
# print(comments)#成功获取到10个div标签
comments_list=[]
for comment in comments:
    # print(comment.xpath('ul/li[@class="main_con"]/span/text()')[0])成功输出评论文本
    # print(comment.xpath('div[@class="userimg"]/span/a/text()')[0])成功抓取到用户名
    user_name=comment.xpath('div[@class="userimg"]/span/a/text()')[0]
    user_comment=comment.xpath('ul/li[@class="main_con"]/span/text()')[0]
    user_comment=re.sub('[\n\s]+','',user_comment)
    comment_dict={}
    comment_dict["username"]=user_name
    comment_dict["comment"]=user_comment #构造出字典，发现需要去除评论中的空白
    comments_list.append(comment_dict) #将每一条评论写成字典再写入列表
#得到每一页的评论组成的列表了，写入文件
f=open("comments.csv","w")
writer=csv.DictWriter(f,fieldnames=["username","comment"])
writer.writeheader()
writer.writerows(comments_list)
f.close()
#完成了一页评论的抓取，现在将其写成函数
