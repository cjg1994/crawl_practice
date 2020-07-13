#马蜂窝中搜索多伦县，游记+评论
#http://www.mafengwo.cn/travel-scenic-spot/mafengwo/10707.html 中的多伦游记，26页，每页10篇
#游记点击其他页发现url并未改变，说明是ajax加载的
#改变page参数就可以得到游记的每一页 最后一个参数虽然不知道是干嘛的，但是发现只更改page就可以得到数据
# mddid: 10707
# pageid: mdd_index
# sort: 1
# cost: 0
# days: 0
# month: 0
# tagid: 0
# page: 2
# _ts: 1580782547394
# _sn: 0008ca16e8
#
# mddid: 10707
# pageid: mdd_index
# sort: 1
# cost: 0
# days: 0
# month: 0
# tagid: 0
# page: 3
# _ts: 1580782671896
# _sn: 90e8aa9588
#请求返回的JS代码好像具有随机性，同一个页面有时候返回521 有时候返回200 难道要写一个判断，如果是521或者报错，就返回来重新请求
import requests
import json
import lxml.html
import re
import time
import execjs #执行JS代码
# from selenium import webdriver
# #
# driver=webdriver.PhantomJS(r'C:\PhantomJS\phantomjs-2.1.1-windows\bin\phantomjs.exe',service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
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
    # print(html)
    #提取出10篇文章的链接
    selector=lxml.html.fromstring(html)
    articles=selector.xpath('//div[@class="tn-list"]/div')
    # print(len(articles)) #10
    f=open("duolun_mafeng.txt","a",encoding="utf-8")
    for article in articles:
        ab_link=article.xpath('.//a[@class="title-link"]/@href')[0]
        travel_id=ab_link.split("/")[-1].split(".")[0]
        # print(travel_id)
        article_title=article.xpath('.//a[@class="title-link"]/text()')[0]
        article_url="http://www.mafengwo.cn"+ab_link
        # article_url="http://www.mafengwo.cn/i/16472754.html"
        # article_url="http://www.mafengwo.cn/i/15391128.html"
        print(article_url)
        f.write(str(total_article)+"\n")
        total_article=total_article+1
        while True:
        # try:
            try:
                session=requests.session()
                response_a=session.get(article_url,headers=headers)
                # time.sleep(2)
                cookie_id=";".join(["=".join(item) for item in response_a.cookies.items()])#当时把response_a写成了response所以一直还是521
                # print(cookie_id)
                a_text=response_a.text  #在线格式化JS代码 Python执行JS代码首选安装PyExecJS模块
                # print(a_text)
                text_521=''.join(re.findall('<script>(.*?)</script>', a_text))
                func_return = text_521.replace('eval', 'return')
                content = execjs.compile(func_return)
                # f.write(content.call('f'))
                # print(content.call('f')) #返回的还是一段JS代码 这说明之前这几步是解密JS代码得到JS代码
                evaled_func=content.call('x')
                # f.write(evaled_func+"\n")
                x=evaled_func.split('=')[0].split(' ')[1] #函数的变量名
                mode_func=evaled_func.replace("document.cookie=","return")
                # f.write(mode_func+"\n")
                # f.write("----------------------------------------------------------")
                #尝试把evaled_func用selenium进行运行
                # print(evaled_func)
                s="{var "+x+"=document.createElement('div');"+x+".innerHTML='<a href=\'/\'>_2b</a>';"+x+"="+x+".firstChild.href"
                n="{var "+x+"='http://www.mafengwo.cn/'"
                mode_func=mode_func.replace(s,n)
                mode_func=mode_func.replace("if((function(){try{return !!window.addEventListener;}catch(e){return false;}})()){document.addEventListener('DOMContentLoaded',"+x+",false)}else{document.attachEvent('onreadystatechange',"+x+")}","")
                mode_func=mode_func.replace(r"setTimeout('location.href=location.pathname+location.search.replace(/[\?|&]captcha-challenge/,\'\')',1500);","")
                mode_func=mode_func.replace("return return('String.fromCharCode('+"+x+"+')')","return(String.fromCharCode("+x+"))")#解密出来的JS有些会出现return return这种错误写法
                # mode_func=mode_func+"return"+" "+x+"()" #这里调用函数，并且要加一个return 返回结果到python中 别忘了return之后还要衔接一个空格
                # f.write(mode_func+"\n")
                # f.write("---------------------------------------------------------------")
                content=execjs.compile(mode_func)
                __jsl_clearance=content.call(x)
                # print(res) #有些成功了 但是有些解密出来的JS代码又是另外一种，而且这种JS有点奇怪
                # __jsl_clearance=driver.execute_script(mode_func)  #终于可以执行并且获取到返回值了
                __jsl_clearance=re.sub("\x00","",__jsl_clearance) #解密出来的数据中有\x00 print出来是空格的 但是用空格替换好像没有效果
                # print(type(__jsl_clearance))
                # print(__jsl_clearance)
                new_headers={
                    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
                    "cookie":cookie_id+";"+__jsl_clearance.split(";")[0]
                }
                resp=session.get(article_url,headers=new_headers) #测试发现cookie里只要有__jsluid_h __jsl_clearance即可
                # print(resp)
                if resp.status_code==200:
                    break
            except:
                print("返回的JS不能运行重新获取")
        # print("end")
        # break
        article_html=resp.text
    #     # time.sleep(5)
    #     # print(len(article_html))
        new_iid=re.findall(r'"new_iid":"(.*?)",',article_html) #有些文章结构中没有new_iid
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
    #     #     time.sleep(2)
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
        article_content=re.sub("[\s]+","",article_content)+ re.sub("[\s]+","",article_expand)#游记正文
    #     #有些文章过长还需要ajax加载，加载的页面url可以通过原页面里的数据构造出来，那么就需要判断每一篇文章的这个页面是否还有数据，如果有的话就要提取出来加入正文数据，可以写一个循环，直至数据为空
        f.write("游记正文:"+article_title+"\n")
        f.write(article_content)
        f.write("\n"+"评论:"+"\n")
    #     # # print(resp)#终于成功了
    #     # # print(mode_func)
    #     # # print(driver.execute_script(mode_func)
    #     # #如何执行mode_func这段JS代码呢 浏览器中执行这段代码有返回值，但是python中调用driver.execute_script()执行时无返回值，需要在 函数调用之前加个return
    #     # #接着获取评论
        num=1
        while True:
    #         #捕捉不到评论还有一个原因是原来url中的双引号不能改成单引号 必须保证一模一样
    #         #格式化字符串中本身包含的花括号格式化输出时需要再加上一个花括号 {-->{{  }-->}}
    #{"iid":"653908","page":"1"} 与{"iid":653908,"page":1}好像都可以访问，但是如果是键的双引号变成了单引号就不行。{"iid":653908,"page":1}可行，{'iid':653908,'page':1}不可行
            c_url='http://pagelet.mafengwo.cn/note/pagelet/bottomReplyApi?params={{"iid":{},"page":{}}}'.format(travel_id,num)#字符串的格式化这一步出错了
    #         # print(c_url)
            c_data=json.loads(session.get(c_url,headers=new_headers).text)
    #         # time.sleep(2)
    #         # print(c_data)
            c_html=c_data["data"]["html"]
            if c_html.find("_j_reply_content")==-1: #如果页面没评论了就退出循环
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
                    comment='' #有些评论是表情或者图片没有文字
                f.write(username+":"+re.sub("[\s]+","",comment)+"\n")  #如果没有评论就不会写入，而不是出错了
            num=num+1
        f.write("--"*70+"\n")
        time.sleep(5)
    #     # break
    #     # mode_func=evaled_func.replace("document.cookie=",'return').replace("if((function(){try{return !!window.addEventListener;}catch(e){return false;}})()){document.addEventListener('DOMContentLoaded',"+x+",false)}else{document.attachEvent('onreadystatechange',"+x+")}","").\
    #     #                         replace(r"setTimeout('location.href=location.pathname+location.search.replace(/[\?|&]captcha-challenge/,\'\')',1500);","").replace(r"window.headless+","")
    #     # print(mode_func) 发现返回的mode_func都是变化的，简单的字符串替换满足不了，有时依旧会报错
    #     #  #执行mode_func这段JS代码就可以得到结果 上面mode_func的修改是执行时报错进行删除尝试的
    #     # # mode_func=evaled_func.replace("document.cookie=",'return')
    #     # content_2=execjs.compile(mode_func)
    #     # cookies=content_2.call(x)
    #     # print(cookies)
    #     # headers={
    #     #     "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    #     #     "cookie":cookie_id+";"+cookies.split(";")[0]
    #     # }
    #     # print(headers)
    #     # # article_s=lxml.html.fromstring(text)
    #     # p_s=article_s.xpath('//p[@class="_j_note_content _j_seqitem"]')
    #     # print(p_s)
    #     # for p in p_s:
    #     #     p.xpath('string(.)')
f.close()
