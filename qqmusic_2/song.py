"""
爬取一个歌手的歌曲
1.点击一首歌播放，开发者工具中找到歌曲信息对应的文件，访问这个url发现没有数据，原来是使用的Post方法，找到发送的Form Data 使用post访问url

2.歌曲文件得去Network的Media选项下面找，得到url，可以直接访问得到字节流，打开一个wb模式的文件再写入

3.为什么要使用session,session.get  session.post来访问url

4.比如周杰伦的一首歌 说好不哭 是免费的的 播放后在Media选项下得到文件url,有多个文件的话找那个文件名不同的，单独访问发现也是能播放的
url='http://122.226.161.13/amobile.music.tc.qq.com/C400001qvvgF38HVc4.m4a?guid=2306237181&vkey=82E3019C3ABF339A3BE8C620C2EE8FAC5898B21AA3EF4FD8365D746BF2DCCFCF0BAB0DE903EEA3CF23527A4EACACCD5E1C3612BA994D2DF5&uin=6055&fromtag=66'
许嵩的一首歌的url:
url='http://122.226.161.22/amobile.music.tc.qq.com/C4000043aj132xwlEf.m4a?guid=2306237181&vkey=4C5D6ABF3C845D597C3268EBB6EB746468C422228147807BC4BEDAAE99A7A4C6DE3C62D589345FBCED693DCA6983F57054F0C08DF4B53147&uin=6055&fromtag=66'
许嵩第二首歌的url:
url='http://122.226.161.24/amobile.music.tc.qq.com/C400002g9P1v0pNEqN.m4a?guid=2306237181&vkey=451379465770FBDCBEDE63A68035B53BC22B287BF47CEE182438808F05AC24500959F31B57FDD8AAA1E86CDBF0593D11DD1E3F3FCEAF2952&uin=6055&fromtag=66'

还不知道如何下载歌曲
歌曲文件的文件名由一个js文件中的l参数产生，加上域名就能访问到这首歌曲
接着探究这个js文件的url,如果能找到规律，就能从中获得每一首歌曲的文件名
https://u.y.qq.com/cgi-bin/musicu.fcg?callback=getplaysongvkey9450514623840787&g_tk=1227116187&jsonpCallback=getplaysongvkey9450514623840787&loginUin=532223911&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data=%7B%22req%22%3A%7B%22module%22%3A%22CDN.SrfCdnDispatchServer%22%2C%22method%22%3A%22GetCdnDispatch%22%2C%22param%22%3A%7B%22guid%22%3A%222306237181%22%2C%22calltype%22%3A0%2C%22userip%22%3A%22%22%7D%7D%2C%22req_0%22%3A%7B%22module%22%3A%22vkey.GetVkeyServer%22%2C%22method%22%3A%22CgiGetVkey%22%2C%22param%22%3A%7B%22guid%22%3A%222306237181%22%2C%22songmid%22%3A%5B%220023GYvV2sPKYp%22%5D%2C%22songtype%22%3A%5B0%5D%2C%22uin%22%3A%22532223911%22%2C%22loginflag%22%3A1%2C%22platform%22%3A%2220%22%7D%7D%2C%22comm%22%3A%7B%22uin%22%3A532223911%2C%22format%22%3A%22json%22%2C%22ct%22%3A20%2C%22cv%22%3A0%7D%7D
发现上面这个url除了data参数是必须的，其他参数都可以删除进行访问，data参数很像之前访问歌手分类的url,需要urllib.parse.unquote方法解码
'{"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"2306237181","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiG
etVkey","param":{"guid":"2306237181","songmid":["0023GYvV2sPKYp"],"songtype":[0],"uin":"532223911","loginflag":1,"platform":"20"}},"comm":{"uin":532223911,"format":"json","ct":20,"
cv":0}}'
将解码出来的数据直接作为data去访问发现也是成功的，因为一般的网站都会实现url的自动转码
修改其中的songmid参数进行访问看看是否能获取其他歌曲对应的文件 发现只要改成其他的songmid就可以访问 guid其实是从cookies中获取，因为是固定不变的，所以这里就不动态去cookies中获取
尝试付费歌曲是否也能这样获取，比如周杰伦的告白气球，去周杰伦所有歌曲信息对应的文件中找到告白气球的songmid
发现如上操作之后获取歌曲url对应的js文件，然而JS文件里的purl参数和vkey参数是空的，并不像其他免费歌曲一样


5.找到一个歌手所有歌曲对应的资源文件，譬如许嵩的全部歌曲的第一页url 主要是singermid参数定位了歌手曲目的资源文件
url='https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg?g_tk=1227116187&jsonpCallback=MusicJsonCallbacksinger_track&loginUin=532223911&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&singermid=000CK5xN3yZDJt&order=listen&begin=0&num=30&songstatus=1'
经过删除部分参数测试 url='https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg?singermid=000CK5xN3yZDJt&order=listen&begin=0&num=30'
找到第二页歌曲的url 发现是https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg?singermid=000CK5xN3yZDJt&order=listen&begin=0&num=30
说明每一页url变化的是begin和num参数 总歌曲数可以从访问url后的total参数得到

此时还有一个问题就是每首歌对应的url该如何构造
"""
formdata={"comm":{"uin":"532223911","ct":"24","cv":"0","gzip":"0","mcc":"460","mnc":"1"},
"data_id":{"module":"track_info.UniformRuleCtrlServer",
            "method":"GetTrackInfo",
            "param":{"ids":[237773700],
                    "types":[0]}
                    }
            }
cookies='pgv_pvi=6608590848; RK=/TTQKyRRFb; ptcz=0d1b9733c04ceb758568ee2ac6f5050c1bd9b0955cabb7315a7155a8f5b815a3; ts_uid=7415789888; pgv_pvid=2306237181; pgv_si=s9232970752; pgv_info=ssid=s7665624828; qqmusic_fromtag=66; _qpsvr_localtk=0.48659199035466694; uin=o0532223911; skey=@QgPhtQLRy; ptisp=ctc; luin=o0532223911; lskey=00010000557bcdb0a9640f223be85e604268475395453f6416e482abbc8f809ccbcb313526530e6f18e6c787; p_uin=o0532223911; pt4_token=OeWUlQBlIiiQXGudqg2xxiyiTTeF15LddrHKJIbVp0s_; p_skey=f4Eex06tHJl6BQZ-bKrf6pr7x9854PabE6xcBaeuSMg_; p_luin=o0532223911; p_lskey=000400000fed589deb5fef4191ad5ea742c6e9c3cb6d9d076c91c1055652b4cffdbc2ce11c3d7e006c8067ee; ts_refer=www.qqmusic.com/qqmusic/frame.html; ts_last=y.qq.com/n/qqmusic/singer/0025NhlN2yWrP4.html'
