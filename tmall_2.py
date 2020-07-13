"""
天猫某个商店的爬虫带上cookie就能获取到数据，不带cookie就不行,但是cookie是有时效性的吧，也就是说爬取的时候必须先手动登录把cookie复制出来
如何做到全自动呢,能不能在登录界面用post发送账号密码实现登录先，再访问商品的url
这是登录时请求的url https://login.taobao.com/newlogin/login.do?appName=taobao&fromSite=0
但是登录时post的数据里面有经过加密的数据,必须破解这些数据才能实现登录,不然只能用selenium模块或者是直接带cookie的方式

"""

import requests

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
}
session=requests.session()


url="https://semir.tmall.com/i/asynSearch.htm?_ksTS=1591783594894_117&callback=jsonp118&mid=w-18687831015-0&wid=18687831015&path=/search.htm&search=y&spm=a1z10.3-b-s.w5003-22094443291.6.3e726d6aLvB5f0&keyword=%C4%D0%B3%C4%C9%C0&orderType=hotsell_desc&scene=taobao_shop"
resp=requests.get(url,headers=headers)
print(resp.text)
