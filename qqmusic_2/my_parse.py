"""
开发者工具里的Network选项返回的文件都是支持ctrl-f搜索的  直接在文件列表那里ctrl+f打开搜索界面
"""

url='https://u.y.qq.com/cgi-bin/musicu.fcg?callback=getUCGI9144530902493533&g_tk=5381&jsonpCallback=getUCGI9144530902493533&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data=%7B%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A10000%7D%2C%22singerList%22%3A%7B%22module%22%3A%22Music.SingerListServer%22%2C%22method%22%3A%22get_singer_list%22%2C%22param%22%3A%7B%22area%22%3A-100%2C%22sex%22%3A-100%2C%22genre%22%3A-100%2C%22index%22%3A-100%2C%22sin%22%3A0%2C%22cur_page%22%3A1%7D%7D%7D'
url2='https://u.y.qq.com/cgi-bin/musicu.fcg?callback=getUCGI6791086958585475&g_tk=5381&jsonpCallback=getUCGI6791086958585475&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data=%7B%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A10000%7D%2C%22singerList%22%3A%7B%22module%22%3A%22Music.SingerListServer%22%2C%22method%22%3A%22get_singer_list%22%2C%22param%22%3A%7B%22area%22%3A-100%2C%22sex%22%3A-100%2C%22genre%22%3A-100%2C%22index%22%3A-100%2C%22sin%22%3A0%2C%22cur_page%22%3A1%7D%7D%7D'
url3='https://u.y.qq.com/cgi-bin/musicu.fcg?callback=getUCGI04830043560306807&g_tk=5381&jsonpCallback=getUCGI04830043560306807&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data=%7B%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A10000%7D%2C%22singerList%22%3A%7B%22module%22%3A%22Music.SingerListServer%22%2C%22method%22%3A%22get_singer_list%22%2C%22param%22%3A%7B%22area%22%3A2%2C%22sex%22%3A-100%2C%22genre%22%3A-100%2C%22index%22%3A-100%2C%22sin%22%3A0%2C%22cur_page%22%3A1%7D%7D%7D'
url4='https://u.y.qq.com/cgi-bin/musicu.fcg?callback=getUCGI5884086763004113&g_tk=5381&jsonpCallback=getUCGI5884086763004113&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data=%7B%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A10000%7D%2C%22singerList%22%3A%7B%22module%22%3A%22Music.SingerListServer%22%2C%22method%22%3A%22get_singer_list%22%2C%22param%22%3A%7B%22area%22%3A2%2C%22sex%22%3A0%2C%22genre%22%3A-100%2C%22index%22%3A-100%2C%22sin%22%3A0%2C%22cur_page%22%3A1%7D%7D%7D'

url5='https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg?g_tk=5381&jsonpCallback=MusicJsonCallbacksinger_track&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&singermid=0025NhlN2yWrP4&order=listen&begin=0&num=30&songstatus=1'

url6='https://u.y.qq.com/cgi-bin/musicu.fcg?&g_tk=5381&jsonpCallback=getUCGI5884086763004113&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data=%7B%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A10000%7D%2C%22singerList%22%3A%7B%22module%22%3A%22Music.SingerListServer%22%2C%22method%22%3A%22get_singer_list%22%2C%22param%22%3A%7B%22area%22%3A2%2C%22sex%22%3A0%2C%22genre%22%3A-100%2C%22index%22%3A-100%2C%22sin%22%3A0%2C%22cur_page%22%3A1%7D%7D%7D'
url7='https://u.y.qq.com/cgi-bin/musicu.fcg?&g_tk=1227116187&jsonpCallback=getUCGI3327021923646065&loginUin=532223911&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data=%7B%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A10000%7D%2C%22singerList%22%3A%7B%22module%22%3A%22Music.SingerListServer%22%2C%22method%22%3A%22get_singer_list%22%2C%22param%22%3A%7B%22area%22%3A2%2C%22sex%22%3A0%2C%22genre%22%3A-100%2C%22index%22%3A-100%2C%22sin%22%3A80%2C%22cur_page%22%3A2%7D%7D%7D'

{"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"2306237181","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiG
etVkey","param":{"guid":"2306237181","songmid":["0023GYvV2sPKYp"],"songtype":[0],"uin":"532223911","loginflag":1,"platform":"20"}},"comm":{"uin":532223911,"format":"json","ct":20,"
cv":0}}
"001FL0V21f8blE"
{"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"2306237181","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiG
etVkey","param":{"guid":"2306237181","songmid":["001FL0V21f8blE"],"songtype":[0],"uin":"532223911","loginflag":1,"platform":"20"}},"comm":{"uin":532223911,"format":"json","ct":20,"
cv":0}}