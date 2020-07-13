"""
实现关注用户
在某个用户微博上点击关注，实现关注用户
测试1，关注 股痴-重阳
Request URL: https://weibo.com/aj/f/followed?ajwvr=6&__rnd=1576036042182
Request Method: POST
Form Data:
uid: 5920679670
objectid:
f: 1
extra:
refer_sort:
refer_flag: 1005050001_
location: page_100505_home
oid: 5920679670
wforce: 1
nogroup: 1
fnick: 股痴-重阳
refer_lflag: 0000015010_
refer_from: profile_headerv6
template: 7
special_focus: 1
isrecommend: 1
is_special: 0
redirect_url: %2Fp%2F1005053206312660%2Fmyfollow%3Fgid%3D3550682776806000%23place  解码后/p/1005053206312660/myfollow?gid=3550682776806000#place
_t: 0

测试2 关注 爱省钱的欧尼酱
Request URL: https://weibo.com/aj/f/followed?ajwvr=6&__rnd=1576036278965
Request Method: POST
Form Data:
uid: 6141034687            对比上个关注测试，uid变化，猜测是对应用户id
objectid:
f: 1
extra:
refer_sort:
refer_flag: 1005050001_
location: page_100505_home
oid: 6141034687           oid变化 oid也就是uid
wforce: 1
nogroup: 1
fnick: 爱省钱的欧尼酱          fnick变化，对应用户名
refer_lflag: 0000015010_
refer_from: profile_headerv6
template: 7
special_focus: 1
isrecommend: 1
is_special: 0
redirect_url: %2Fp%2F1005053206312660%2Fmyfollow%3Fgid%3D3550682776806000%23place   解码后为'/p/1005053206312660/myfollow?gid=3550682776806000#place'
_t: 0                                                  看命名猜测是一个重定向url,加上域名之后果然是个人的一个关注情况页面

所以现在主要是对应用户的uid 和oid（dengyu uid）的获取，用户名由自己输入
发现在被关注的用户微博的源代码中可以获取到uid,必须事先要传递用户微博首页的url
而不是只有一个用户名就能实现关注，微博好像没有提供搜索用户名的接口
"""
import requests
from login import login












if __name__=='__main__':
    session=requests.Session()
    username='15757116151'
    password=''
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }
    proxies={}
    login(username,password,headers=headers,proxies=proxies)
