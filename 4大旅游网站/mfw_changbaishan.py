#马蜂窝长白山游记 主页搜索框中搜索长白山 返回的URL是 http://www.mafengwo.cn/search/q.php?q=%E9%95%BF%E7%99%BD%E5%B1%B1&seid=75A2EC2F-0995-469C-ACD6-E690956A9ECD 其中的q参数编码是长白山，seid参数不知是什么，删除之后访问也成功
#点击上方导航栏中的游记两字 范湖的URL http://www.mafengwo.cn/search/q.php?q=%E9%95%BF%E7%99%BD%E5%B1%B1&t=notes&seid=75A2EC2F-0995-469C-ACD6-E690956A9ECD&mxid=&mid=&mname=&kt=1
#上面这个url保留q和t参数就可以访问成功，点击第二页 url变为http://www.mafengwo.cn/search/q.php?q=%E9%95%BF%E7%99%BD%E5%B1%B1&p=2&t=notes&kt=1
#说明参数需要保留的是q,p,t 浏览时候发现有时候底下的页面DIV不显示，不知是浏览器原因还是网络原因 每一页有50篇游记
#上次爬取具体游记文章时会返回一串JS代码，不知此次是否一样
import requests
import lxml.html
import time
import re
# import execjs
import json
#下面这个cookie有时效性大概20分钟左右
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    "cookie":"__guid=186442287.4386924987600930300.1580710592208.643; mfw_uuid=5e37bac2-558d-e4b2-e075-2ceb7748b514; UM_distinctid=17009b1907553-0d71a4cb9a94be-454c092b-ff000-17009b190763ea; uva=s%3A92%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1580710602%3Bs%3A10%3A%22last_refer%22%3Bs%3A24%3A%22https%3A%2F%2Fwww.mafengwo.cn%2F%22%3Bs%3A5%3A%22rhost%22%3BN%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1580710602%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=5e37bac2-558d-e4b2-e075-2ceb7748b514; __jsluid_h=1e790a2ed4b4b13cbb3ca2f1fe1d043f; PHPSESSID=fc3pi6627dpq7rou1gilmt9583; oad_n=a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222020-03-12+11%3A25%3A48%22%3B%7D; __mfwc=direct; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1583983548; bottom_ad_status=0; __omc_chl=; __omc_r=; __mfwlv=1583999581; __mfwvn=6; CNZZDATA30065558=cnzz_eid%3D998103768-1580708696-https%253A%252F%252Fwww.mafengwo.cn%252F%26ntime%3D1583999556; __mfwa=1580710594430.29913.7.1583999581713.1584002329640; __jsl_clearance=1584003705.254|0|NxaY4oXirLeEyu3EIyfaHKBrl3M%3D; monitor_count=37; __mfwb=0b11a62b5efd.3.direct; __mfwlt=1584003706; Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1584003707"
}
f=open("mfw_changbaishan.txt","a",encoding="utf-8")
total_article=1
for num in range(1,7):#一共有6页，先直接输入
    url="http://www.mafengwo.cn/search/q.php?q=%E9%95%BF%E7%99%BD%E5%B1%B1&p={}&t=notes&kt=1".format(num)
    resp=requests.get(url,headers=headers)
    # print(resp)#6页列表均能获取，接着获取每一页游记的url列表
    text=resp.text
    selector=lxml.html.fromstring(text)
    trips_url=selector.xpath('//div[@class="ct-text "]/h3/a/@href')
    trips_titles=selector.xpath('//div[@class="ct-text "]/h3/a/text()')

    for article_url,article_title in zip(trips_url,trips_titles):
        # print(article_url)
        travel_id=article_url.split("/")[-1].split(".")[0]
        f.write("第%d篇:%s\n"%(total_article,article_title))
        total_article=total_article+1
        article_response=requests.get(article_url,headers=headers)
        article_html=article_response.text

        new_iid=re.findall(r'"new_iid":"(.*?)",',article_html)
        if new_iid:
            new_iid=new_iid[0]
        else:
            new_iid=""
        iid=travel_id
        data_seq=re.findall(r'data-seq="(.*?)"',article_html)
        if data_seq:
            data_seq=data_seq[-1]
        else:
            data_seq=""
        flag=re.findall(r'"has_more":(.*?),',article_html)
        if flag:
            flag=flag[0]
        else:
            flag=""
        article_expand=""
        if flag=="true":
            expand_url="http://www.mafengwo.cn/note/ajax/detail/getNoteDetailContentChunk?id={}&iid={}&seq={}&back=0".format(iid,new_iid,data_seq)

            expand_text=json.loads(requests.get(expand_url,headers=headers).text)
            expand_html=expand_text["data"]["html"]
            new_flag=expand_text["data"]["has_more"]
            expand_selector=lxml.html.fromstring(expand_html)
            article_expand='.'.join([p.xpath('string(.)') for p in expand_selector.xpath('//p[@class="_j_note_content _j_seqitem"]')])
            if new_flag :
                # pass #有些游记很长很长，还有页面需要获取，感觉这里可以循环获取，具体还没操作
                article_expand=article_expand+"游记很长未完"
        article_selector=lxml.html.fromstring(article_html)
        ps=article_selector.xpath('//p[@class="_j_note_content _j_seqitem"]')
        # print(ps)
        if ps:
            article_content='.'.join([p.xpath('string(.)') for p in article_selector.xpath('//p[@class="_j_note_content _j_seqitem"]')])
        else:
            article_content='.'.join([p.xpath('string(.)') for p in article_selector.xpath('//p[@class="_j_note_content"]')])
        article_content=re.sub("[\s]+","",article_content)+ re.sub("[\s]+","",article_expand)
        f.write(article_content)
        f.write("\n"+"--"*70+"\n")
        time.sleep(2)
        # break
    # break
f.close()
