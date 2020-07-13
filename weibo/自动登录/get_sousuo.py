"""
抓取用户发表的微博
"""
import requests
from login import login
import lxml.html

def get_weibo(keyword,n):
    pass

if __name__=='__main__':
    session=requests.Session()
    keyword='王者荣耀'
    n=2 #爬取的页数
    #实现登录
    username='15757116151'
    password=''
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }
    proxies={}
    login(username,password,headers=headers,proxies=proxies) #应该写成类或者直接在之前的函数里把headers和proxies写死
    #抓取数据
    get_weibo(keyword,n)
