"""
爬取音乐，付费音乐可以直接爬取下载
"param":{"area":-100,"sex":-100,"genre":-100,"index":change_num,"sin":total,"cur_page":1}
修改sin而不修改curpage依旧可以获得对应类别下的另一页歌手名
1.需要遍历每个类别
2.每个类别还需要遍历每一页，不断增加sin的值，用if来判断返回的数据的singerlist是否为空列表的话，会爬取到很多页面没显示的歌手
3.如果要爬取页面总数对应的歌手名，那就需要获取每个类别对应有多少页，而这也是通过异步加载的，所以又需要去找对应的资源文件
4.每个类别的每一页最后一个参数total都是相同的，说明是显示的总的歌手数，除以80就能得到页数
"""

#分析得到歌手url主要变化的是下面的param部分
'{"comm":{"ct":24,"cv":10000},"singerList":{"module":"Music.SingerListServer","method":"get_singer_list","param":{"area":2,"sex":0,"genre":-100,"index":1,"sin":0,"cur_page":1}}}'
#假设要获取全站的歌手列表，可以根据 首字母拼音和一个字符#分类 下的全部歌手名
#只需要循环遍历26个字母和一个#号对应的url
#修改{"comm":{"ct":24,"cv":10000},"singerList":{"module":"Music.SingerListServer","method":"get_singer_list","param":{"area":2,"sex":0,"genre":-100,"index":1,"sin":0,"cur_page":1}}}
url='https://u.y.qq.com/cgi-bin/musicu.fcg?&data={}'
data={"comm":{"ct":24,"cv":10000},"singerList":{"module":"Music.SingerListServer","method":"get_singer_list","param":{"area":-100,"sex":-100,"genre":-100,"index":change_num,"sin":total,"cur_page":1}}}
#data中对第几页起决定作用的是sin的值
