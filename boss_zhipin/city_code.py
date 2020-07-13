"""
城市编号的映射表
"""
import requests
import json
def get_city_code():
    headers={                             #定义过程中使用了headers,该文件中调用函数时不会使用login.py里定义的headers,必须作为参数传递
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",

    }
    url='https://www.zhipin.com/wapi/zpCommon/data/city.json'
    text=requests.get(url,headers=headers).text
    data=json.loads(text)
    city_info={}
    for city in data["zpData"]["cityList"]: #cityList对应的是直辖市或者省份，统一抓取"subLevelModelList"字段
        for c in city["subLevelModelList"]:
            city_info[c["name"]]=c["code"] #因为选择省份以后必须要选择城市，所以这里不将省份编号存入
    return city_info
