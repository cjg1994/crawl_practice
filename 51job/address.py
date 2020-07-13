"""
获取搜索栏中地址对应的编号 用来构造URL
"""
import requests
import re
import lxml.html
import csv
import chardet
# import demjson
url='https://js.51jobcdn.com/in/resource/js/2019/search/common.0ebd455e.js'
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
}
response=requests.get(url,headers=headers)
#不是json数据，采用正则提取有用的信息
text=response.text
address_map=re.findall('window.area=(.*?"珠三角"})',text)[0] #成功提取出一个类似字典的地址映射信息
address=eval(address_map)#考虑将字符串直接执行，得到字典对象
# address=json.loads(address_map) #发现有些键是数字而不是字符串 10001 "10001" 所以不能使用json
# print(address_map[:100])
#为了方便的构造URL，将字典键值交换
address_dict={v:k for k,v in address.items()}
# print(address_dict['北京'])
#demjson模块 用来转换类似数据
# temp = demjson.decode(address_map)
# print(type(temp))
# print(temp[251400])虽然转换成字典了 但是并不是把251400 变成 "251400"

#假设要查杭州的python相关职位
position="杭州"
key="运营"
#构造url,查询的是杭州的运营岗位,发现url中传入中文，访问时会自动转码；如果有些网站不支持自动转码，那就需要使用urllib.parse.quote方法
url='https://search.51job.com/list/{0},000000,0000,00,9,99,{1},2,1.html'.format(address_dict[position],key)
# print(url)
res=requests.get(url,headers=headers)
charset=chardet.detect(res.content)  #这里检测获得的字节流的编码
res.encoding=charset['encoding'] #指定.text属性获取文本的时候的编码
html=res.text#如果直接获取.text 默认是使用一种编码， 导致了后面的编码错误
selector=lxml.html.fromstring(html)
# i=selector.xpath('//div[@class="dw_table"]')
# print(i) #这里是能获取到这个标签的
infos=selector.xpath('//div[@class="dw_table"]/div[@class="el"]')#此处的元素class属性是el,而不是e1  要区别小写L和1
# print(len(infos))
info_list=[]
for info in infos:
    info_dict={}
    name=info.xpath('p/span/a/text()')[0].strip()
    #此处获取的url还可以在这个循环中再requests.get一下，获取工作的详细信息,再一起写入info_dict
    job_url=info.xpath('p/span/a/@href')[0]
    company=info.xpath('span')[0].xpath('a/text()')[0] #xpath定位元素返回的是一个列表 下标从0开始
    add=info.xpath('span')[1].xpath('text()')[0]#第二个span节点的文本
    try:
        salary=info.xpath('span')[2].xpath('text()')[0]
    except:
        salary="缺失值"
    pubtime=info.xpath('span')[3].xpath('text()')[0]
    info_dict['name']=name
    info_dict['job_url']=job_url
    info_dict['company']=company
    info_dict['add']=add
    info_dict['salary']=salary
    info_dict['pubtime']=pubtime
    info_list.append(info_dict)

f=open('job.csv','w')
writer=csv.DictWriter(f,fieldnames=['name','job_url','company','add','salary','pubtime']) #表头参数是fieldnames
writer.writeheader()
# print(info_list)
writer.writerows(info_list) #写入文件的时候也出错，主要是因为编码的问题
#如果要获取多页的职位 发现只是把url最后面的1.html 改成2.html  可以把上面获取地点编码，获取每页职位信息分别写成函数
