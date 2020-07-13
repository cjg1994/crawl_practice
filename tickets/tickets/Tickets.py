"""
读取用户购票信息,登录12306,查询车票信息,获取购买车票的详细信息,选择乘客和席别,核对预定的车票,发送邮件,保持登录状态
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import excepted_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select
from tickets.SitesCode import SitesCode
import yagmail
import time

class Tickets:
    def __init__(self):
        self.driver=webdriver.Chrome()
        self.tickets_info=[]
        self.read_tickets_from_file()
        self.sites=SitesCode()

    #读取购票信息
    def read_tickets_from_file(self):
        with open("buy_tickets.txt","r",encoding="utf-8") as f:
            for line in f:
                self.tickets_info.append(line.strip())
    #登录12306
    def login(self):
        self.driver.get("https://kyfw.12306.cn/otn/resources/login.html")
        try:
            #手动输入,如果登录成功会跳转,通过EC.url_to_be捕捉url的变化判断是否成功
            wait=WebDriverWait(self.driver,100)
            wait.until(EC.url_to_be("https://kyfw.12306.cn/otn/view/index.html"))
        except TimeoutException:
            return False
        return True

    #查询车票信息
    def query_tickets(self,flag=0):
        #flag=0说明是第一次查询,需要在目的地,出发地输入预购的车票信息
        if flag=0:
            #这是购买车票的页面,而不是主页面
            self.driver.get("https://kyfw.12306.cn/otn/leftTicket/init")
            try:
                #抓取输入框,EC.presence_of_element_located的参数是一个元祖形式,代表一个页面元素
                from_station_input=WebDriverWait(self.driver,100).until(EC.presence_of_element_located((By.ID,"fromStationText")))
                #清楚输入框中的文字
                from_station_input.clear()
                #向输入框中输入目的地,有必要输入吗,反正都是在隐藏输入框中输入对应编号
                from_station_input.send_keys(self.tickets_info[0])
                site_code=self.sites.name_2_code(self.tickets_info[0])

                #JS:设置隐藏的输入框的值为出发地的编码,构造字符串的时候注意value="值"这两个双引号不要忘了
                js="document.getElementById('fromStation').value=\""+site_code+"\";"
                #执行JS
                self.driver.execute_script(js)

                #设置目的地,设置方法与出发地相似
                time.sleep(1)
                #显示等待,知道目的地输入框加载
                to_station_input=WebDriverWait(self.driver,100).until(EC.presence_of_element_located((By.ID,"toStationText")))
                to_station_input.clear()
                to_station_input.send_keys(self.tickets_info[1])
                site_code=self.sites.name_2_code(self.tickets_info[1])
                #JS:设置隐藏的输入框的值为目的地的编码,构造字符串的时候注意value="值"这两个双引号不要忘了
                js="document.getElementById('toStation').value=\""+site_code+"\";"
                #执行JS
                self.driver.execute_script(js)

                #设置出发日期
                time.sleep(1)
                #选择了日期之后网页上看到value值并没有变化,这是怎么回事,这里还是设置value值
                WebDriverWait(self.driver,100).until(EC.presence_of_element_located((By.ID,"train_date")))
                js="document.getElementById('train_date').value=\""+slef.tickets_info[2]+"\";"
                self.driver.execute_script(js)
            except TimeoutException:
                return False
        try:
            #单击查询按钮
            WebDriverWait(self.driver,100).until(EC.presence_of_element_located((By.ID,"query_ticket")))
            #self.driver也有抓取元素的函数find_element_by_id等
            searchButton=self.driver.find_element_by_id("query_ticket")
            searchButton.click()
            #显示等待每一列车的信息加载,这里会等待所有tr加载吗,还是只加载一个tr就往下执行了
            #应该是全部tr加载,可设置time.sleep(3)保证加载或者直接抓取tbody
            WebDriverWait(self.driver,100).until(EC.presence_of_element_located((By.XPATH,"//tbody[@id='queryLeftTable']/tr")))
        except:
            return False
        return True
    def get_ticket(self):
        #获取所有车票信息列表
        #获取所有不包含datatran属性的tr标签
        tr_list=self.driver.find_elements_by_xpath('//tbody[@id="queryLeftTable"]/tr[not(@datatran)]')
        for tr in tr_list:
            #self.driver支持find_element_by_XXX语法
            train_number=tr.find_element_by_class_name("number").text
            if train_number==self.tickets_info[3]:
                if self.tickets_info[4] in ["商务座"，"特等座"]:
                    #这个地方抓取元素要注意一下,等结束之后来改一下这里试试是否可行,再写一个循环遍历
                    #创建一个数组存商务座 特等座这些名称
                    #测试一下self.driver是否支持self.driver.xpath()这种写法
                    left_ticket=tr.find_element_by_xpath(".//td[2]").text
                elif self.tickets_info[4] in ["一等座"]:
                    left_ticket=tr.find_element_by_xpath(".//td[3]").text
                elif self.tickets_info[4] in ["二等座"]:
                    left_ticket=tr.find_element_by_xpath(".//td[4]").text
                elif self.tickets_info[4] in ["高级软卧"]:
                    left_ticket=tr.find_element_by_xpath(".//td[5]").text
                elif self.tickets_info[4] in ["软卧","一等卧"]:
                    left_ticket=tr.find_element_by_xpath(".//td[6]").text
                elif self.tickets_info[4] in ["动卧"]:
                    left_ticket=tr.find_element_by_xpath(".//td[7]").text
                elif self.tickets_info[4] in ["硬卧","二等卧"]:
                    left_ticket=tr.find_element_by_xpath(".//td[8]").text
                elif self.tickets_info[4] in ["软座"]:
                    left_ticket=tr.find_element_by_xpath(".//td[9]").text
                elif self.tickets_info[4] in ["硬座"]:
                    left_ticket=tr.find_element_by_xpath(".//td[10]").text
                elif self.tickets_info[4] in ["无座"]:
                    left_ticket=tr.find_element_by_xpath(".//td[11]").text
                elif self.tickets_info[4] in ["其他"]:
                    left_ticket=tr.find_element_by_xpath(".//td[12]").text
                else:
                    return -1 #席别不存在
                if left_ticket=="--":
                    return -1   #这列车没有这种席别
                #有票的情况
                if left_ticket=="有" or left_ticket.isgigit():
                    orderButton=tr.find_element_by_class_name("btn72")
                    if orderButton.is_enable(): #有票而且预定按钮可以单击
                        orderButton.click()
                        return 1
                    else:#有票但还没开售.不能预定
                        time.sleep(3)
                        return -2
                else:#无票
                    time.sleep(3)
                    return -2
        return -3 #最外层语句块的返回,说明车次不存在
    def children_dialog(self):
        try:
            #显示等待,直到提示对话框的确认按钮被加载
            WebDriverWait(self.driver,3).until(EC.presence_of_element_located((By.ID,"dialog_xsertcj_ok")))
            #获取确认按钮
            #为什么还需要获取该元素,上面那行代码不就是返回确认按钮这个元素吗?
            okButton=self.driver.find_element_by_id("dialog_xsertcj_ok")
            okButton.click()
        except:
            pass
    def order_ticket(self):
        try:
            #显示等待 直到跳转到乘客确认车票的页面
            WebDriverWait(self.driver,100).until(EC.url_to_be("https://kyfw.12306.cn/otn/confirmPassenger/initDc"))
            #显示等待,直到所有的常用乘客信息被加载,这一步是常用信息常客加载
            WebDriverWait(self.driver,100).until(EC.presence_of_element_located((By.XPATH,"//ul[@class='normal_passenger_id']/li")))
        except TimeoutException:
            return False
        passanger_labels=self.driver.find_elements_by_xpath('//ul[@id="normal_passenger_id"]/li/label')
        order_passangers=self.tickets_info[5].split(",")
        amount=0
        #如果购票的名字在常用乘客信息里面,
        for label in passanger_labels:
            if label.text in order_passangers:
                label.click()
                amount+=1
                #如果这个名字是儿童的话,会弹出儿童票温馨提示框
                self.children_dialog()
        #这是每个下拉列表option的value,要通过这个value值来确定选择哪个
        SEAT_TYPE={
            "商务座":"9",
            "特等座":"P",
            "一等座":"M",
            "二等座":"O",
            "高级软卧":"6",
            "软卧":"4",
            "硬卧":"3",
            "软座":"2",
            "硬座座":"1",
            "无座":"1"
        }
        #选择席别,是根据乘客数来确定复选框的id的,所以上面要统计一下乘客数量
        for i in range(1,amount+1):
            id="seatType_%d"%i
            value=SEAT_TYPE[self.tickets_info[4]]
            #操作下拉列表,选择符合的项
            Select(self.driver.find_element_by_id(id)).select_value_by(value)
        submitButton=self.driver.find_element_by_id("submitOrder_id")
        submitButton.click()
        return True
    
