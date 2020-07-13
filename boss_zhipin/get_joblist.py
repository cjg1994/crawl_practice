"""
对应的职位列表
"""
import lxml.html
def get_job_list(url,keyword,city,headers):
    html=requests.get(url,headers=headers).text
    selector=lxml.html.fromstring(html)
    selector
