"""
给出出发地和目的地，返回车次列表
https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E8%8B%8F%E5%B7%9E,SZH&ts=%E5%A4%A9%E6%B4%A5,TJP&date=2019-12-13&flag=N,N,Y
https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E5%8C%97%E4%BA%AC,BJP&ts=%E4%B8%8A%E6%B5%B7,SHH&date=2019-12-13&flag=N,N,Y
可以看出 fs参数  出发地,出发地代号  ts参数表示 目的地,目的地代号  中文网站会自动编码，date参数表示出发日期格式为 2019-12-13
url中的每个参数都是必须的，删除任意一个就访问不到数据
那么问题主要就是获取地点和代号的映射  再构造url进行访问，再提取数据就ok了
开发者工具中直接搜索'北京' 就能找到对应资源文件的url
Request URL: https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9126
接着处理这个数据
列车次的数据并不在网页的源代码中，所以定位到准确资源，进行下载，网站做了cookie验证，get请求时请求头必需带上cookie
测试一下res.cookies,再转换成字典，然后get请求的时候cookies参数设为这个字典
测试失败，res.cookies为空，可能是因为缺少相关证书，访问失败获取不到cookies,而如果想要访问成功必须带上verify=False,但res.cookies仍为空，说明是证书的原因
"""
import requests
import re
import chardet
#也可以下载对应网站的证书,verify参数的值改成 证书文件的路径
html=requests.get('https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9126',verify=False)
# print(html.cookies)
data=html.text
# city_list=re.findall('@(.*?)@',data) #规则有问题，会漏掉一些地点，因为第二个@已经被匹配了，所以第二个地点开始就没有@字符，会匹配不到
city_list=re.findall('@(.*?)\d+',data)
# print(len(city_list))
city_dict={}
for city in city_list:
    city_dict[city.split('|')[1]]=city.split('|')[2]
# print(city_dict['上海'])
start='北京'
end='上海'
date='2019-12-13'
url='https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs={},{}&ts={},{}&date={}&flag=N,N,Y'.format(start,city_dict[start],end,city_dict[end],date)
# print(url)
text=requests.get(url,verify=False).text #发现列车次真正信息并不在源代码里，需要去找到对应的资源文件，ctrl+F搜索一个车次得到
# print(text.find('G149'))

url_2='https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(date,city_dict[start],city_dict[end])
print(url_2) #为什么明明能获得url,下面访问却出错,需要带上cookie
headers={
    "User-Agent":'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    # 'Referer':'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E5%8C%97%E4%BA%AC,BJP&ts=%E4%B8%8A%E6%B5%B7,SHH&date=2019-12-13&flag'
    # 'Cookie':'JSESSIONID=BDAC7AEEF958880600EF22915063A970; _jc_save_wfdc_flag=dc; BIGipServerpool_passport=267190794.50215.0000; RAIL_EXPIRATION=1576550079058; RAIL_DEVICEID=X1sIodW4PDyy5-KAdrIPrgb0ydgapvR2DsfkPBdgYOPl639Bapu6NM1hCbFQfaSvwHyjbX28_fdIO33PwmRWMgU-5p9jMERz1AgrIpewUNGHyY5qWAW-8ntnVqSVMPFEB9TBfbox_GaMVbhqWFfAIM7O_wR4ARoY; _jc_save_fromDate=2019-12-13; _jc_save_toDate=2019-12-13; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; route=9036359bb8a8a461c164a04f8f50b252; BIGipServerotn=1257243146.24610.0000'
    'Cookie':'JSESSIONID=60CE806651C6402922A7E9C617DCEF39; _jc_save_wfdc_flag=dc; BIGipServerpool_passport=267190794.50215.0000; RAIL_EXPIRATION=1576550079058; RAIL_DEVICEID=X1sIodW4PDyy5-KAdrIPrgb0ydgapvR2DsfkPBdgYOPl639Bapu6NM1hCbFQfaSvwHyjbX28_fdIO33PwmRWMgU-5p9jMERz1AgrIpewUNGHyY5qWAW-8ntnVqSVMPFEB9TBfbox_GaMVbhqWFfAIM7O_wR4ARoY; _jc_save_fromDate=2019-12-13; _jc_save_toDate=2019-12-13; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; route=9036359bb8a8a461c164a04f8f50b252; BIGipServerpassport=786956554.50215.0000; BIGipServerotn=485491210.38945.0000'
}

res=requests.get(url_2,headers=headers,verify=False)#如果一开始不带上cookie
# print(res.cookies)
# my_cookisdict=requests.utils.dict_from_cookiejar(res.cookies)
charset=chardet.detect(res.content)
res.encoding=charset['encoding']
# print(my_cookisdict)
print(res.text.find('D705'))
# res2=requests.get(url_2,headers=headers,verify=False,cookies=my_cookisdict)
# print(res2.text)
