"""
搜索关键字“助理”
所有相关岗位爬取，并分析职位描述或者职位详情部分有没有 “爬虫” 字样
搜索页面的地址栏url
https://www.zhipin.com/job_detail/?query=&city=101210100&industry=&position=
这是每个城市对应编号的文件url  把这个对应关系的数据下载下来先
https://www.zhipin.com/wapi/zpCommon/data/city.json
输入助理并点击杭州地址栏url变为：  编码部分对应 助理 两字  ka猜测是 'sel-city-'+ 城市对应编号
https://www.zhipin.com/c101210100/?query=%E5%8A%A9%E7%90%86&ka=sel-city-101210100
选了杭州以后，还可以选择滨江区，浦沿街道，这里只考虑爬取整体城市，而不分里面的区域

"""
