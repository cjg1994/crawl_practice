"""
站点处理的类:
1.从文件中获取站点信息
2.判断站点是否存在
3.根据站点名获取站点编号
"""
class SitesCode:
    def __init__(self):
        self.sites={}
        self.get_sites_from() #初始化这个类的时候就执行这个方法填充self.sites
    def get_sites_from(self):
        with open("sites.txt","r",encoding="utf-8") as f:
            for site in f:
                site=site.strip().split(":")
                site_name=site[0]
                site_code=site[1]
                self.sites[site_name]=site_code
    def is_exist(self,site_name):
        if site_name in self.sites:
            return True
        else:
            return False
    def name_2_code(self,site_name):
        return self.sites[site_name]
