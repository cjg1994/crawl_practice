"""
提取百度知道页面时提取不到问题列表  必需带上cookie不然抓取不到准确数据
，最后发现是xpath写错的原因 找到ul //ul  忘记加上 //
"""

import requests
import lxml.html

url='https://zhidao.baidu.com/list?fr=daohang'
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'Cookie':'BIDUPSID=E815020B2450FB2C5A2A883D52C36950; PSTM=1534739412; BAIDUID=6C1F5B57817225D5683A81001322601C:FG=1; shitong_key_id=2; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; H_PS_PSSID=1444_21105_30210_18560_26350; PSINO=5; ZD_ENTRY=baidu; Hm_lvt_6859ce5aaf00fb00387e6434e4fcc925=1576134017,1576304600; Hm_lpvt_6859ce5aaf00fb00387e6434e4fcc925=1576304603; shitong_data=fb93080e6adce017f657e0ac08cbe25e60e50f648057e4ed0cbf0c937382bc9ada75d54602143a25296db1947076de41a52a1b073f5753b85a1922f018747c57870191529937f0878becf1516b06b859a257d596477e9dde37d573ed84c1afcf8596ec0873bdf7742153361067a890dcc72ba37ecf6c2173f1617b36d916a7c4; shitong_sign=4c046287',
    'Referer': 'https://zhidao.baidu.com/list?type=default'
}
res=requests.get(url,headers=headers)
data=res.text
# print(data)
selector=lxml.html.fromstring(data)
s=selector.xpath('//ul[@class="question-list-ul"]/li[@class="question-list-item"]')
for ques in s:
    text=ques.xpath('div[1]/div//a/text()')[0]
    print(text)
