import requests
import json
import lxml.html
import re
import time
import execjs

total_article=1
for page in range(1,27):
    data={
        "mddid": 10707,
        "pageid": "mdd_index",
        "sort": 1,
        "cost": 0,
        "days": 0,
        "month": 0,
        "tagid": 0,
        "page": page,
        "_ts": 1581324314149,
        "_sn": "0008ca16e8"
    }
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    }
    url="http://www.mafengwo.cn/gonglve/ajax.php?act=get_travellist"
    response=requests.post(url,headers=headers,data=data)
    html=json.loads(response.text)["list"]
    selector=lxml.html.fromstring(html)
    articles=selector.xpath('//div[@class="tn-list"]/div')
    f=open("duolun_mafeng.txt","a",encoding="utf-8")
    for article in articles:
        ab_link=article.xpath('.//a[@class="title-link"]/@href')[0]
        travel_id=ab_link.split("/")[-1].split(".")[0]
        article_title=article.xpath('.//a[@class="title-link"]/text()')[0]
        article_url="http://www.mafengwo.cn"+ab_link
        print(article_url)
        f.write(str(total_article)+"\n")
        total_article=total_article+1
        while True:
            try:
                session=requests.session()
                response_a=session.get(article_url,headers=headers)
                cookie_id=";".join(["=".join(item) for item in response_a.cookies.items()])
                a_text=response_a.text
                text_521=''.join(re.findall('<script>(.*?)</script>', a_text))
                func_return = text_521.replace('eval', 'return')
                content = execjs.compile(func_return)
                evaled_func=content.call('x')
                x=evaled_func.split('=')[0].split(' ')[1]
                mode_func=evaled_func.replace("document.cookie=","return")
                s="{var "+x+"=document.createElement('div');"+x+".innerHTML='<a href=\'/\'>_2b</a>';"+x+"="+x+".firstChild.href"
                n="{var "+x+"='http://www.mafengwo.cn/'"
                mode_func=mode_func.replace(s,n)
                mode_func=mode_func.replace("if((function(){try{return !!window.addEventListener;}catch(e){return false;}})()){document.addEventListener('DOMContentLoaded',"+x+",false)}else{document.attachEvent('onreadystatechange',"+x+")}","")
                mode_func=mode_func.replace(r"setTimeout('location.href=location.pathname+location.search.replace(/[\?|&]captcha-challenge/,\'\')',1500);","")
                mode_func=mode_func.replace("return return('String.fromCharCode('+"+x+"+')')","return(String.fromCharCode("+x+"))")
                content=execjs.compile(mode_func)
                __jsl_clearance=content.call(x)
                __jsl_clearance=re.sub("\x00","",__jsl_clearance)
                new_headers={
                    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
                    "cookie":cookie_id+";"+__jsl_clearance.split(";")[0]
                }
                resp=session.get(article_url,headers=new_headers)
                if resp.status_code==200:
                    break
            except:
                print("返回的JS不能运行重新获取")
        article_html=resp.text
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
            expand_text=json.loads(session.get(expand_url,headers=new_headers).text)
            expand_html=expand_text["data"]["html"]
            new_flag=expand_text["data"]["has_more"]
            expand_selector=lxml.html.fromstring(expand_html)
            article_expand='.'.join([p.xpath('string(.)') for p in expand_selector.xpath('//p[@class="_j_note_content _j_seqitem"]')])
            if new_flag :
                article_expand=article_expand+"游记正文未完后续还有"
        article_selector=lxml.html.fromstring(article_html)
        ps=article_selector.xpath('//p[@class="_j_note_content _j_seqitem"]')
        if ps:
            article_content='.'.join([p.xpath('string(.)') for p in article_selector.xpath('//p[@class="_j_note_content _j_seqitem"]')])
        else:
            article_content='.'.join([p.xpath('string(.)') for p in article_selector.xpath('//p[@class="_j_note_content"]')])
        article_content=re.sub("[\s]+","",article_content)+ re.sub("[\s]+","",article_expand)
        f.write("游记正文:"+article_title+"\n")
        f.write(article_content)
        f.write("\n"+"评论:"+"\n")
        num=1
        while True:
            c_url='http://pagelet.mafengwo.cn/note/pagelet/bottomReplyApi?params={{"iid":{},"page":{}}}'.format(travel_id,num)
            c_data=json.loads(session.get(c_url,headers=new_headers).text)
            c_html=c_data["data"]["html"]
            if c_html.find("_j_reply_content")==-1:
                f.write("无评论或评论就这么多了"+"\n")
                break
            c_selector=lxml.html.fromstring(c_html)
            users=c_selector.xpath('//div[@class="mfw-cmt _j_reply_item"]')
            for user in users:
                username=user.xpath('div[@class="mcmt-info"]/div[@class="mcmt-user"]/a[1]/text()')[0]
                comment=user.xpath('div[@class="mcmt-con-wrap clearfix"]//p[@class="_j_reply_content"]/text()')
                if comment:
                    comment=user.xpath('div[@class="mcmt-con-wrap clearfix"]//p[@class="_j_reply_content"]/text()')[0]
                else:
                    comment=''
                f.write(username+":"+re.sub("[\s]+","",comment)+"\n")
            num=num+1
        f.write("--"*70+"\n")
        time.sleep(5)
f.close()
