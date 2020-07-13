import requests
import lxml.html
domain="https://so.gushiwen.org"
headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
}
text=requests.get("https://so.gushiwen.org/guwen/",headers=headers).text
selector=lxml.html.fromstring(text)
bookname_list=selector.xpath('//div[@class="main3"]/div[@class="right"]/div/div[@class="cont"]/a/text()')
url_list=selector.xpath('//div[@class="main3"]/div[@class="right"]/div/div[@class="cont"]/a/@href')

for url,name in zip(url_list,bookname_list):
    newurl=domain+url
    selector_new=lxml.html.fromstring(requests.get(newurl,headers=headers).text)
    title_list=selector_new.xpath('//div[@class="main3"]/div[@class="left"]/div[@class="sons"]/div/ul/span/a/text()')
    link_list=selector_new.xpath('//div[@class="main3"]/div[@class="left"]/div[@class="sons"]/div/ul/span/a/@href')
    filename=name+'.txt'
    count = 1
    for url,newname in zip(link_list,title_list):
        url_2=domain+url
        select=lxml.html.fromstring(requests.get(url_2,headers=headers).text)
        content=select.xpath('//div[@class="main3"]/div[@class="left"]/div[@class="sons"]/div[@class="cont"]/div[@class="contson"]')[0].xpath('string(.)')
        with open('lunyu/%s'%(filename),'a',encoding='utf-8') as f:
            f.write('第%d章 %s'%(count,newname))
            f.write(content)
        count+=1
