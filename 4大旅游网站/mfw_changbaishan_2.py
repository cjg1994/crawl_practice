import requests
import json
import lxml.html
import re
import time
import execjs

total_article=1
f=open("test.txt","a",encoding="utf-8")
for num in range(1,7):
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }
    url="http://www.mafengwo.cn/search/q.php?q=%E9%95%BF%E7%99%BD%E5%B1%B1&p={}&t=notes&kt=1".format(num)
    response=requests.get(url,headers=headers)
    text=response.text
    selector=lxml.html.fromstring(text)
    trips_url=selector.xpath('//div[@class="ct-text "]/h3/a/@href')
    trips_titles=selector.xpath('//div[@class="ct-text "]/h3/a/text()')
    for article_url,article_title in zip(trips_url,trips_titles):
        travel_id=article_url.split("/")[-1].split(".")[0]
        f.write("第%d篇:\n"%(total_article))
        total_article=total_article+1
        while True:
            try:
                session=requests.session()
                response_a=session.get(article_url,headers=headers)
                cookie_id=";".join(["=".join(item) for item in response_a.cookies.items()])
                a_text=response_a.text
                text_521=''.join(re.findall('<script>(.*?)</script>', a_text))
                #eval换成return的原因是eval是将里面的字符串当做代码来运行的 得到了什么 就改成return将它返回
                func_return = text_521.replace('eval', 'return')
                content = execjs.compile(func_return)
                evaled_func=content.call('x')
                # f.write(evaled_func)
                # f.write('--'*50)
                x=evaled_func.split('=')[0].split(' ')[1] #这一步获取的是解密之后的JS代码中的函数名，每一次都是不固定的，所以要获取名称
                mode_func=evaled_func.replace("document.cookie=","return")
                s="{var "+x+"=document.createElement('div');"+x+".innerHTML='<a href=\'/\'>_2b</a>';"+x+"="+x+".firstChild.href"
                n="{var "+x+"='http://www.mafengwo.cn/'"
                mode_func=mode_func.replace(s,n)
                mode_func=mode_func.replace("if((function(){try{return !!window.addEventListener;}catch(e){return false;}})()){document.addEventListener('DOMContentLoaded',"+x+",false)}else{document.attachEvent('onreadystatechange',"+x+")}","")
                mode_func=mode_func.replace(r"setTimeout('location.href=location.pathname+location.search.replace(/[\?|&]captcha-challenge/,\'\')',1500);","")
                mode_func=mode_func.replace("return return('String.fromCharCode('+"+x+"+')')","return(String.fromCharCode("+x+"))")
                # f.write('\n')
                # f.write(mode_func)
                content=execjs.compile(mode_func)
                __jsl_clearance=content.call(x)
                __jsl_clearance=re.sub("\x00","",__jsl_clearance)
                new_headers={
                    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
                    "cookie":cookie_id+";"+__jsl_clearance.split(";")[0]
                }
                resp=session.get(article_url,headers=new_headers)
                print(resp)
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
        f.write(article_content)
        f.write("--"*70+"\n")
        time.sleep(5)
        break
    break
f.close()
