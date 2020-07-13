"""
在搜索栏上写上 王者荣耀 url变成
url=https://s.weibo.com/weibo/%25E7%258E%258B%25E8%2580%2585%25E8%258D%25A3%25E8%2580%2580?topnav=1&wvr=6&b=1
第一次调用urllib.parse.unquote(url)返回的数据依然是编码的，不过应该是去掉了其中的%25，再进行解码得到 王者荣耀
说明url的构造就是合并搜索关键词 https://s.weibo.com/weibo/王者荣耀?topnav=1&wvr=6&b=1
说明网站是由后台生成，而不是异步加载形式
必须登录才能查看下一页 下一页的url
https://s.weibo.com/weibo/%E7%8E%8B%E8%80%85%E8%8D%A3%E8%80%80?topnav=1&wvr=6&b=1&page=2
说明第一页的url加上page=1也是能访问的
将关键词改成英雄联盟 猪肉等不相关的关键词 发现topnav wvr b 三个参数始终不变
检察元素 发现下面的用户发表的每条微博都在一个div里 遍历div 抓取微博用户名 微博内容 发表的图片 发表的视频 这四个数据
下面测试元素的抓取
抓取视频时获得的src是：
//f.video.weibocdn.com/003Mcacalx07zf3Vg9HG01041200A2jq0E010.mp4?label=mp4_ld&template=640x360.25.0&trans_finger=40a32e8439c5409a63ccf853562a60ef&Expires=1575955994&ssig=n97MpBhCDS&KID=unistore,video
发现地址栏直接访问就可以得到这个视频
"""
import requests
import lxml.html
import csv
url='https://s.weibo.com/weibo/%E7%8E%8B%E8%80%85%E8%8D%A3%E8%80%80?topnav=1&wvr=6&b=1'
headers={
    "User-Agent":'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
res=requests.get(url,headers=headers)
# print(res.text[:1000]) 中文正常显示不需要更改编码
# print(res.text.find('狄仁杰')) 查找一条微博中的词发现页面源代码中就包括了这些内容，而不是异步加载进来的
# 开始提取页面元素
data=res.text
selector=lxml.html.fromstring(data)
weibo_list=selector.xpath('//div[@class="m-wrap"]/div/div/div[@class="card-wrap"]')
# print(len(weibo_list)) #每页24条微博
users=[]
for weibo in weibo_list:
    info={}
    #先提取用户名 其实需要提取的内容都在class属性为content的div标签下
    name=weibo.xpath('div[@class="card"]/div/div[@class="content"]/div/div/a[@class="name"]/@nick-name')[0]#可以提取到用户名
    # content=weibo.xpath('div[@class="card"]/div/div[@class="content"]/p[@class="txt"]/text()')[0]
    #返回的文本节点数组里包括了空白换行 有效内容等 需要清理
    content=weibo.xpath('div[@class="card"]/div/div[@class="content"]/p[@class="txt"]/text()')
    #连接然后去除空白
    content=''.join(content).strip()
    #提取视频 提取视频遇到问题 视频并不是每条微博都会发的
    try:
        viedo_src=weibo.xpath('div[@class="card"]/div/div[@class="content"]/div[@class="media media-video-a"]/div[@class="thumbnail"]//video/@src')[0]
    except IndexError:
        video_src=''
    #同理 提取图片元素 图片src组成的一个列表，因为可能有多张图片
    #这条提取规则有问题 因为如果用户发表的是视频，可能会捕获到相关的图片，并不是用户发表的图片
    # img_src_list=weibo.xpath('div[@class="card"]/div/div[@class="content"]/div[@node-type="feed_list_media_prev"]//img/@src')
    #因为发表的图片都是在一个ul里的，所以更精确定位
    try:
        img_src_list=weibo.xpath('div[@class="card"]/div/div[@class="content"]/div[@node-type="feed_list_media_prev"]/div/ul//img/@src')
    except IndexError:
        img_src_list=[]
    #提取完毕 写入文件 怎么保存诗句呢 先不下载图片和视频 保存src先
    info["name"]=name
    info["content"]=content
    info["video_src"]=video_src
    info["img_src_list"]=img_src_list
    users.append(info)
    # print(name,img_src_list)

#写入csv文件
with open('weibo_content.csv','a',encoding="utf-8") as f:
    writer=csv.DictWriter(f,fieldnames=["name","content","video_src","img_src_list"])
    writer.writeheader()
    writer.writerows(users)
#运行，能实现第一页24条微博的爬取了
