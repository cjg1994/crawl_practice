"""
1.首先是登录微博 输入错误的密码登录 使用开发者工具找到验证的url是
https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=MTU3NTcxMTYxNTE%3D&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)&_=1575809337617
Query String Parameters:  这一栏表示上面这个url的请求参数
entry: weibo
callback: sinaSSOController.preloginCallBack
su: MTU3NTcxMTYxNTE=                           用户名
rsakt: mod
checkpin: 1
client: ssologin.js(v1.4.19)
_: 1575809337617                               今年对应的时间戳

"""
import requests
import chardet
import base64
import time
#cookie模拟登录失败主要是因为headers里的参数键值是cookie,一开始写成了cookies
headers={
    "User-Agent":'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    # 'cookie':'SINAGLOBAL=115.206.44.194_1534568666.775943; SGUID=1534644174669_32659603; U_TRS1=00000044.630e3964.5c00a1f4.012c4f9d; SUB=_2AkMqsH4tf8NxqwJRmP0XyG_ma49-zgDEieKc7I_2JRMyHRl-yD83qnM5tRB6ATBQwW-mQvNwjghaLx3g5FXHIHyBCrTh; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WF1KHZRriqJzAK4LLPVi7bw; login=6ec7f45fe2ef20765c00bb7efc116593; Apache=115.206.42.209_1575809309.107483'
    'cookie':'SINAGLOBAL=6829146187233.395.1575809308028; un=15757116151; UOR=,,login.sina.com.cn; wvr=6; wb_timefeed_3206312660=1; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF_JK1cQQwTP2FejV7bk8Jj5JpX5KMhUgL.FoeEehq0eKzcSo52dJLoIEBLxK-L12qLB-2LxKBLBonLB.2LxKBLBonL1-eLxKqL1KqLBo.t; Ugrow-G0=1ac418838b431e81ff2d99457147068c; ALF=1607755628; SSOLoginState=1576219630; SCF=AkfuVKxWXXKixfkvD-9GZ26cUD2hKR7XzBqotPTQvQFsWS-WlKvgzWVUpboqqymqxfKVt7X_buB6_9kUUPclAtg.; SUB=_2A25w90O-DeRhGeVM61QS8SzKzTyIHXVThTJ2rDV8PUNbmtBeLW_ekW9NTMWSAz1N-W2jADJ6skIvuyjL1hmJu1Qy; SUHB=079jV6Dc87Puyu; YF-V5-G0=8c4aa275e8793f05bfb8641c780e617b; YF-Page-G0=7f483edf167a381b771295af62b14a27|1576219634|1576219634; wb_view_log_3206312660=1360*7681; _s_tentry=login.sina.com.cn; Apache=4093596682343.33.1576219631416; ULV=1576219631460:4:4:4:4093596682343.33.1576219631416:1576035970131; webim_unReadCount=%7B%22time%22%3A1576231715362%2C%22dm_pub_total%22%3A1%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A40%2C%22msgbox%22%3A0%7D',
    'Referer':'https://weibo.com/u/3206312660/home?wvr=5'
}
session=requests.Session()
res=session.get('https://weibo.com/3206312660/profile?topnav=1&wvr=6',headers=headers)
# res=requests.get('https://weibo.com/3206312660/profile?topnav=1&wvr=6',headers=headers)
charset=chardet.detect(res.content)
# print(charset)
res.encoding=charset['encoding']
# print(res.text.find('东方'))
# headers_bak={
#     "User-Agent":'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
#     # 'cookie':'SINAGLOBAL=115.206.44.194_1534568666.775943; SGUID=1534644174669_32659603; U_TRS1=00000044.630e3964.5c00a1f4.012c4f9d; SUB=_2AkMqsH4tf8NxqwJRmP0XyG_ma49-zgDEieKc7I_2JRMyHRl-yD83qnM5tRB6ATBQwW-mQvNwjghaLx3g5FXHIHyBCrTh; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WF1KHZRriqJzAK4LLPVi7bw; login=6ec7f45fe2ef20765c00bb7efc116593; Apache=115.206.42.209_1575809309.107483'
#     }
files={"b64_data":base64.b64encode(open('test.png','rb').read())}
url='https://picupload.weibo.com/interface/pic_upload.php?cb=https%3A%2F%2Fweibo.com%2Faj%2Fstatic%2Fupimgback.html%3F_wv%3D5%26callback%3DSTK_ijax_{}&mime=image%2Fjpeg&data=base64&url=weibo.com%2Fu%2F3206312660&markpos=1&logo=1&nick=%40%E5%8F%AA%E4%B8%BA%E4%B8%9C%E6%96%B9&marks=0&app=miniblog&s=rdxt&pri=null&file_source=1'.format((int(time.time()*1000000)))
# response=session.post(url,headers=headers_bak,files=files,allow_redirects=False)#allow_redirects=False
response=session.post(url,headers=headers,files=files,allow_redirects=False)#allow_redirects=False
location=response.headers["Location"]#经测试这里返回的url并没有pid 不像在Fiddler中看到的那样
#奇了怪了，隔了两天 换了一下cookies  获取的时候又可以获取到pid了 继续进行微博的自动发送
#发现主要原因是每一个请求的headers的参数值必须都要带上cookie这一项，而不是说虽然上面那个请求表示登录成功，下面这个请求请求头就不用cookies了
#就好像把上面的headers=headers_bak就会失败
pid=location.split('pid=')[1]
# print(pid)
#构造发送图文微博的参数
text="这是第N+1次测试"
form_data={
"location": "v6_content_home",
"text": text,
"appkey":"",
"style_type": "1",
"pic_id": pid,
"tid":"" ,
"pdetail":"" ,
"mid":"" ,
"isReEdit": "false",
"gif_ids":"" ,
"rank": "0",            #rank 0说明公开  1 说明仅自己可见， 其他值情况尝试一下就知道了
"rankid":"" ,
"module": "stissue",
"pub_source": "main_",
"updata_img_num": "1",
"pub_type": "dialog",
"isPri": "null",
"_t": "0"
}
# headers={
#     "User-Agent":'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
#     # 'cookie':'SINAGLOBAL=115.206.44.194_1534568666.775943; SGUID=1534644174669_32659603; U_TRS1=00000044.630e3964.5c00a1f4.012c4f9d; SUB=_2AkMqsH4tf8NxqwJRmP0XyG_ma49-zgDEieKc7I_2JRMyHRl-yD83qnM5tRB6ATBQwW-mQvNwjghaLx3g5FXHIHyBCrTh; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WF1KHZRriqJzAK4LLPVi7bw; login=6ec7f45fe2ef20765c00bb7efc116593; Apache=115.206.42.209_1575809309.107483'
#     'cookie':'SINAGLOBAL=6829146187233.395.1575809308028; un=15757116151; UOR=,,login.sina.com.cn; wvr=6; wb_timefeed_3206312660=1; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF_JK1cQQwTP2FejV7bk8Jj5JpX5KMhUgL.FoeEehq0eKzcSo52dJLoIEBLxK-L12qLB-2LxKBLBonLB.2LxKBLBonL1-eLxKqL1KqLBo.t; Ugrow-G0=1ac418838b431e81ff2d99457147068c; ALF=1607755628; SSOLoginState=1576219630; SCF=AkfuVKxWXXKixfkvD-9GZ26cUD2hKR7XzBqotPTQvQFsWS-WlKvgzWVUpboqqymqxfKVt7X_buB6_9kUUPclAtg.; SUB=_2A25w90O-DeRhGeVM61QS8SzKzTyIHXVThTJ2rDV8PUNbmtBeLW_ekW9NTMWSAz1N-W2jADJ6skIvuyjL1hmJu1Qy; SUHB=079jV6Dc87Puyu; YF-V5-G0=8c4aa275e8793f05bfb8641c780e617b; YF-Page-G0=7f483edf167a381b771295af62b14a27|1576219634|1576219634; wb_view_log_3206312660=1360*7681; _s_tentry=login.sina.com.cn; Apache=4093596682343.33.1576219631416; ULV=1576219631460:4:4:4:4093596682343.33.1576219631416:1576035970131; webim_unReadCount=%7B%22time%22%3A1576231715362%2C%22dm_pub_total%22%3A1%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A40%2C%22msgbox%22%3A0%7D',
#     'Referer':'https://weibo.com/u/3206312660/home?wvr=5'
# } 这里也失败过一次，考虑到发布微博必定是点了发布按钮，而发布按钮只在个人主页，所以猜测做了Referer验证，试了一下果然如此 成功。
url_send='https://weibo.com/aj/mblog/add?ajwvr=6&__rnd={}'.format(str(int(time.time()*1000)))
res_send=session.post(url_send,headers=headers,data=form_data)
# res_send.encoding=chardet.detect(res_send.content)["encoding"]
# print(res_send.status_code)
# print(res_send.text)
