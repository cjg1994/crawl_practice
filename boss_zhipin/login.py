"""
抓取对应工作的url时返回的响应是一串url代码，猜测应该是产生了一个url让我们继续访问才能抓取到。但是并没有找到.location等表示跳转到
哪个url的代码(可能是自己看不懂JS代码)，后来查找资料发现是请求头中需要加入cookie这一参数，说明网站是做了cookie验证，
其实返回的JS代码里有正在登录几个字样，说明可能是验证登录的，带上cookie之后就成功了。
但是每次一刷新页面,或者是过2分钟，这个cookie就会失效，有需要重新取复制cookie,即使登录以后也是这样.
最后的解决办法是每次抓一条职位信息就休眠5秒，尽量模拟人的行为。不过这样爬虫效率降低太多了
后来又遇到一个问题 一个cookie只能爬取三页，三页之后必须更换cookie,这里可以做一个判断如果获取的数据为空，说明要换cookie，但是cookie怎么获取呢
但是到底是一个ip只能爬取三页还是cookie的问题呢，还未经测试；不过感觉应该是cookie的原因，不可能爬三页就把ip疯了吧
"""
import requests
import lxml.html
import urllib.parse
import chardet
import time
import csv
import re
from city_code import get_city_code  #导入的函数，其中用到的变量是那个模块里的变量，类似这里的headers,如果这个函数
# headers={                             #定义过程中使用了headers,该文件中调用函数时不会使用login.py里定义的headers,必须作为参数传递
#     "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
#
# }
# session=requests.Session()
text=get_city_code() #text是每个地点对应编号
# print(len(text))
keyword="助理"
city="杭州"
url='https://www.zhipin.com/job_detail/?query={}&city={}&industry=&position='.format(keyword,text["杭州"])
referer='https://www.zhipin.com/c{1}/?query={0}&ka=sel-city-{1}'.format(urllib.parse.quote(keyword),text["杭州"])
headers={                             #定义过程中使用了headers,该文件中调用函数时不会使用login.py里定义的headers,必须作为参数传递
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "referer":referer,
    "cookie":'lastCity=101210100; sid=sem_pz_bdpc_dasou_title; _uab_collina=157605134336242007231442; __c=1576051344; __g=sem_pz_bdpc_dasou_title; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1576051344; __l=l=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title&r=https%3A%2F%2Fsp0.baidu.com%2F9q9JcDHa2gU2pMbgoY3K%2Fadrc.php%3Ft%3D06KL00c00fDIFkY0m7qh0KZEgsAPCEKI000005bLyNC00000Tt3JYg.THdBULP1doZA8QMu1x60UWdBmy-bIfK15yc4PAnsuWndnj0sPycYujb0IHYvf17APRcdP16kP1czPRfdPW61fH6knj0kn1czPW0kfsK95gTqFhdWpyfqn1nznj0LnHmknausThqbpyfqnHm0uHdCIZwsT1CEQLILIz4lpA-spy38mvqVQ1q1pyfqTvNVgLKlgvFbTAPxuA71ULNxIA-YUAR0mLFW5Hc1P1ms%26tpl%3Dtpl_11534_21150_17267%26l%3D1515796473%26attach%3Dlocation%253D%2526linkName%253D%2525E6%2525A0%252587%2525E5%252587%252586%2525E5%2525A4%2525B4%2525E9%252583%2525A8-%2525E6%2525A0%252587%2525E9%2525A2%252598-%2525E4%2525B8%2525BB%2525E6%2525A0%252587%2525E9%2525A2%252598%2526linkText%253DBOSS%2525E7%25259B%2525B4%2525E8%252581%252598%2525E2%252580%252594%2525E2%252580%252594%2525E6%252589%2525BE%2525E5%2525B7%2525A5%2525E4%2525BD%25259C%2525EF%2525BC%25258C%2525E6%252588%252591%2525E8%2525A6%252581%2525E8%2525B7%25259F%2525E8%252580%252581%2525E6%25259D%2525BF%2525E8%2525B0%252588%2525EF%2525BC%252581%2526xp%253Did(%252522m3320071610_canvas%252522)%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FH2%25255B1%25255D%25252FA%25255B1%25255D%2526linkType%253D%2526checksum%253D137%26ie%3Dutf-8%26f%3D3%26tn%3Dbaidu%26wd%3Dboss%25E7%259B%25B4%25E8%2581%2598%25E5%25AE%2598%25E7%25BD%2591%26rqlang%3Dcn%26inputT%3D6086050%26prefixsug%3Dboss%26rsp%3D0&g=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title&friend_source=0&friend_source=0; __a=28894238.1576051344..1576051344.83.1.83.83; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1576076491; __zp_stoken__=7fdbC6WLFQaCXPfXOmgBVkUjUUedtSDXbwtDyxGpZxguJ1hQXJyW6up4jsyXn%2BbMdd%2FlcEQKaldwEqiWvLkd0UKyMF9hDfimokA8x4Twu%2BcKd5urOpoIftJygY4IUnrWueB0'
}
#headers里面出现"助理"中文两字，非ascii字符，所以下面get的时候报编码错误，说明助理两字需要转码
# print(headers)
# print(url)
# session=requests.Session()
def get_job_info(url,headers):
    html=requests.get(url,headers=headers)
    charset=chardet.detect(html.content)
    # print(charset)
    html.encoding=charset["encoding"]   #
    # print(html.text)#发现是乱码需要先进性转换
    html=html.text
    selector=lxml.html.fromstring(html)
    joblist=selector.xpath('//div[@class="job-list"]/ul/li')
    # print(html.find("产品"))
    # print(len(joblist))
    # urllist=[]
    infolist=[]
    for job in joblist:
        jobinfo={}
        uri=job.xpath('div/div[@class="info-primary"]/h3/a/@href')[0]
        joburl="https://www.zhipin.com/"+uri
        # urllist.append(joburl)
        jobname=job.xpath('div/div[@class="info-primary"]/h3/a/div/text()')[0]
        salary=job.xpath('div/div[@class="info-primary"]/h3/a/span/text()')[0]
        address=job.xpath('div/div[@class="info-primary"]/p/text()')[0]
        jingyan=job.xpath('div/div[@class="info-primary"]/p/text()')[1]
        xueli=job.xpath('div/div[@class="info-primary"]/p/text()')[2]
        time.sleep(3)   #每抓一条职位就休眠3秒，  不然发现cookie很快失效
        # for link in urllist:
        data=requests.get(joburl,headers=headers).text
        s=lxml.html.fromstring(data)
        description=s.xpath('//div[@class="detail-content"]/div')[0].xpath('string(.)')
        jobinfo["jobname"]=jobname
        jobinfo["salary"]=salary
        jobinfo["address"]=address
        jobinfo["jingyan"]=jingyan
        jobinfo["xueli"]=xueli
        jobinfo["description"]=re.sub('[\n\s]+','',description)
        infolist.append(jobinfo)
        time.sleep(3)
        # break
    return infolist
# print(len(infolist))
    # break
# print(len(urllist))
# 'https://www.zhipin.com/c101210100/?query=%E5%8A%A9%E7%90%86&page=3&ka=page-3'
if __name__=='__main__':
    text=get_city_code() #text是每个地点对应编号
    # print(len(text))
    keyword="助理"
    city="杭州"
    url='https://www.zhipin.com/job_detail/?query={}&city={}&industry=&position='.format(keyword,text["杭州"])
    # referer='https://www.zhipin.com/c{1}/?query={0}&ka=sel-city-{1}'.format(urllib.parse.quote(keyword),text["杭州"])
    headers={                             #定义过程中使用了headers,该文件中调用函数时不会使用login.py里定义的headers,必须作为参数传递
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        # "referer":referer,
        "cookie":'lastCity=101210100; sid=sem_pz_bdpc_dasou_title; _uab_collina=157605134336242007231442; __c=1576051344; __g=sem_pz_bdpc_dasou_title; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1576051344; __l=l=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title&r=https%3A%2F%2Fsp0.baidu.com%2F9q9JcDHa2gU2pMbgoY3K%2Fadrc.php%3Ft%3D06KL00c00fDIFkY0m7qh0KZEgsAPCEKI000005bLyNC00000Tt3JYg.THdBULP1doZA8QMu1x60UWdBmy-bIfK15yc4PAnsuWndnj0sPycYujb0IHYvf17APRcdP16kP1czPRfdPW61fH6knj0kn1czPW0kfsK95gTqFhdWpyfqn1nznj0LnHmknausThqbpyfqnHm0uHdCIZwsT1CEQLILIz4lpA-spy38mvqVQ1q1pyfqTvNVgLKlgvFbTAPxuA71ULNxIA-YUAR0mLFW5Hc1P1ms%26tpl%3Dtpl_11534_21150_17267%26l%3D1515796473%26attach%3Dlocation%253D%2526linkName%253D%2525E6%2525A0%252587%2525E5%252587%252586%2525E5%2525A4%2525B4%2525E9%252583%2525A8-%2525E6%2525A0%252587%2525E9%2525A2%252598-%2525E4%2525B8%2525BB%2525E6%2525A0%252587%2525E9%2525A2%252598%2526linkText%253DBOSS%2525E7%25259B%2525B4%2525E8%252581%252598%2525E2%252580%252594%2525E2%252580%252594%2525E6%252589%2525BE%2525E5%2525B7%2525A5%2525E4%2525BD%25259C%2525EF%2525BC%25258C%2525E6%252588%252591%2525E8%2525A6%252581%2525E8%2525B7%25259F%2525E8%252580%252581%2525E6%25259D%2525BF%2525E8%2525B0%252588%2525EF%2525BC%252581%2526xp%253Did(%252522m3320071610_canvas%252522)%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FH2%25255B1%25255D%25252FA%25255B1%25255D%2526linkType%253D%2526checksum%253D137%26ie%3Dutf-8%26f%3D3%26tn%3Dbaidu%26wd%3Dboss%25E7%259B%25B4%25E8%2581%2598%25E5%25AE%2598%25E7%25BD%2591%26rqlang%3Dcn%26inputT%3D6086050%26prefixsug%3Dboss%26rsp%3D0&g=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title&friend_source=0&friend_source=0; __a=28894238.1576051344..1576051344.83.1.83.83; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1576076491; __zp_stoken__=7fdbC6WLFQaCXPfXOmgBVkUjUUedtSDXbwtDyxGpZxguJ1hQXJyW6up4jsyXn%2BbMdd%2FlcEQKaldwEqiWvLkd0UKyMF9hDfimokA8x4Twu%2BcKd5urOpoIftJygY4IUnrWueB0'
    }
    rows=get_job_info(url,headers)
    # print(rows)
    with open('jobinfo.csv','a',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=["jobname","salary","address","jingyan","xueli","description"])
        writer.writeheader()
        for i in range(1,11):
            url='https://www.zhipin.com/c{1}/?query={0}&page={2}&ka=page-{2}'.format(keyword,text["杭州"],str(i))
            rows=get_job_info(url,headers)
            writer.writerows(rows)
