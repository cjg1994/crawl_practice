"""
预登录
prelogin.php文件 https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=MTU3NTcxMTYxNTE%3D&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)&_=1575809337617
预登录请求访问的文件，会返回之后登陆请求所需的一些参数，例如nonce、rsakv，pubkey，更换上面url中su的值发现这几个参数都是不变的
login.php文件，这个是主要的登录文件，通过post向服务器发送数据，下面是Form data
entry: weibo      用户名和密码二者肯定在以下参数之内
gateway: 1
from:
savestate: 0
qrcode_flag: false
useticket: 1
pagerefer: https://login.sina.com.cn/crossdomain2.php?action=logout&r=https%3A%2F%2Fpassport.weibo.com%2Fwbsso%2Flogout%3Fr%3Dhttps%253A%252F%252Fweibo.com%26returntype%3D1
vsnf: 1
su: MTU3NTcxMTYxNTE=         su一般是用户名
service: miniblog
servertime: 1575874774
nonce: 6SCK19
pwencode: rsa2
rsakv: 1330428213                 sp一般是密码 都是经过加密的
sp: 6a1b0f6f4fb8f05df7aff4a84543f5bcc8cb738e28f61505e4912d731eafbaec368a13e9b67a8adf547626b4555e60556d91f5cb6240c42a9c37519034ffb49e97d1cdefa4c6db99dc00a1798ac7159a5bf4a2d1b0c7da5b9125ca5b8ad680fdb899637cf8b39d6860b0b414e3e2b2b4cb6bb1ec02207741ff3e2412e62a40b4
sr: 1360*768
encoding: UTF-8
prelt: 42
url: https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack
returntype: META
接下来主要就是获得用户名和密码是通过通过什么算法加密的
找到js文件之后，是通过搜索'sp ='找到相关的函数，还可以尝试一下断点调试的方法
分析JS文件发现密码的加密还用上了severtime和nonce两个值，因为这两个值的变化，说明不同时间加密后的sp都是不同的
su是通过base64算法加密，b通过rsa算法加密，接着构造加密后的

"""
import requests
import time
import json
# check_url='https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=MTU3NTcxMTYxNTE%3D&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)&_=1575809337617'
# session=requests.Session()
# headers={
#     "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
# }
# proxies={}
#
# # sever_data=eval(res.content.decode('utf-8').replace('sinaSSOController.preloginCallBack',''))
# server_data=eval(res.text.replace('sinaSSOController.preloginCallBack',''))
# print(sever_data)
def get_login_data(su,session,proxies):
    #通过用户名构造验证的url,发现把su改成用户账号15757116151或者其他号码依然能够访问
    check_url='https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)&_=%s'%(su,str(int(time.time()*1000)))
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }
    res=session.get(check_url,headers=headers,proxies=proxies)
    server_data=eval(res.text.replace('sinaSSOController.preloginCallBack',''))
    return server_data

if __name__=='__main__':
    session=requests.Session()
    proxies={}
    su='15757116151'
    server_data=get_login_data(su,session,proxies)  #更改不同账号 返回的数据只有pcid nonce这两项在变化
    print(server_data)
    # data=json.loads(server_data) 函数里已经ecal了不需要在json反序列化
    pubkey=server_data["pubkey"]
