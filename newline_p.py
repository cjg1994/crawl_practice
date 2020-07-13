"""
open函数的newline参数,普通文件好像没影响,写入文件再从文件里看写的数据好像没区别
再把数据读出来试试有无区别，没测试出来.........对此参数还不了解
"""
# s="aaa\nbbb\nccc\n"
# f=open('new.txt','w',newline='')
# f.write(s)
# f.close()
import csv
fp=open('new.csv','w',newline='')
writer=csv.writer(fp)
writer.writerow(('id','name','grade'))#一行数据要放在一个整体里
writer.writerow(('1','lucky','87'))
writer.writerow(('2','peter','92'))
writer.writerow(('3','lili','85'))
fp.close()

fr=open('new.csv','r',newline='')
s=fr.read()
print(s)
fr.close()
