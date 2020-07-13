"""
实现登录
"""
import requests
from prelogin import get_login_data
from su_get import get_su,get_password
import chardet
import re
def login(username,password,headers,proxies):
    login_url='https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
    su=get_su(username)

    server_data=get_login_data(username,session,proxies)
    nonce=server_data["nonce"]
    servertime=server_data["servertime"]
    rsakv=server_data["rsakv"]
    pubkey=server_data["pubkey"]
    sp=get_password(password,servertime,nonce,pubkey)
    form_data={
"entry":"weibo",
"gateway": "1",
"from":"" ,
"savestate":"7",
"qrcode_flag": "false",
"useticket": "1",
"pagerefer": "",
"vsnf": "1",
"su": su,
"service": "miniblog",
"servertime": servertime,
"nonce": nonce,
"pwencode": "rsa2",
"rsakv": rsakv,
"sp": sp,
"sr": "1360*768",
"encoding": "UTF-8",
"prelt": "245",
"url": "https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
"returntype": "META"
    }
    login_page=session.post(login_url,data=form_data,headers=headers,proxies=proxies)
    charset=chardet.detect(login_page.content)
    login_page.encoding=charset["encoding"]
    # print(login_page.text)#此时输出编码还有问题，中文不能正常显示，使用chadet调整
    #发现此时页面输出的一个html代码，并不是登录后的页面代码，  location.replace一般是跳转，所以提取其中的url
    new_url=re.findall('location.replace\("(.*?)"\)',login_page.text)[0]
    # print(new_url)
    html=session.get(new_url,headers=headers,proxies=proxies)
    html.encoding="GBK"
    #返回的类似上面的response,再提取其中的url
    url_2=re.findall('location.replace\([\'"](.*?)[\'"]\)',html.text)[0] #正则表达式中的[\'"]之所以加上\ 是因为规则字符串外侧是用单引号括起来的
    # print(url_2)
    new_html=session.get(url_2,headers=headers,proxies=proxies)
    html.encoding="GBK"
    # print(new_html.text)
    #返回的数据中有uniqueid,而个人微博的url构造也就是用这个uniqueid
    uid=re.findall('"uniqueid":"(\d+)"',new_html.text)[0]
    # print(uid)
    #https://weibo.com/u/3206312660/home 构造登录以后 个人微博的url
    url_personal='https://weibo.com/u/{}/home'.format(uid)
    # print(url_personal)
    html_personal=session.get(url_personal,headers=headers,proxies=proxies)
    # html_personal.encoding="GBK"   #经过测试，个人微博的页面的编码是utf-8,而之前几个返回的response编码都是gbk
    html_personal.encoding=chardet.detect(html_personal.content)["encoding"]
    # print(html_personal.encoding)
    # print(html_personal.text)
    #至此，自动登录成功，返回页面源代码
    return html_personal.text
if __name__=='__main__':
    session=requests.Session()
    username='15757116151'
    password=''
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }
    proxies={}
    login(username,password,headers=headers,proxies=proxies)
