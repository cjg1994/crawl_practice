"""
搜索当前目录的文件中是否包含我的密码信息，然后进行删除，因为提交代码时要防止泄露
"""

import os
dir = os.path.abspath('.')
#获取当前目录以及子目录下的所有文件路径
file_list = []

def get_file_list(dir):
    for file in os.listdir(dir):
        file_or_dir_path = os.path.join(dir,file)
        if os.path.isfile(file_or_dir_path): #如果是一个文件路径
            file_list.append(file_or_dir_path)
        else:
            #如果是目录,采用递归，其实不是很想用递归，但是没有想到好的方法如何获取全部的文件路径
            get_file_list(file_or_dir_path)
    return file_list
if __name__=='__main__':
    total_file_path = get_file_list(dir)
    # print(total_file_path) #能获取所有文件的路径了
    passwd=''  #填入要搜索的密码
    for file in total_file_path:
        if file.split('.')[-1] == "png":
            continue
        if file.split('.')[-1] == "jpg":
            continue
        elif file.split('.')[-1] == "pyc":
            continue
        else:
            try:
                with open(file,encoding='utf-8') as f:
                    content = f.read()
                    if content.find(passwd) != -1:
                        print(file)
            except:
                print("读取失败:",file)  #发现目录中有图片文件，读取时应该是rb模式，所以会出错，应该忽略掉图片文件
                break  #一旦读取失败就跳出循环，并修改代码解决对应文件为何读取失败,因为包含其他格式的文件 比如.zip .pyc
