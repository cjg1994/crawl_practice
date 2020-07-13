"""需要将每个字符串固定长度输出中间补空白"""
# food='西湖'
# food2='西湖醋鱼'
# food3='西湖醋鱼片儿川'
# food4='西'
# food5='一二三四五六七八'
# s2='|%s'%food2
# s1='|%s'%food
# s3='|%s'%food3
# s4='|%s'%food4
# s5='|%s'%food5
# while len(s2)<=10:
#     s2=s2+' '
# while len(s1)<=12:  #少2个字需要多2个空白
#     s1=s1+' '
# while len(s3)<=7:   #多3个字需要少3个空白
#     s3=s3+' '
# while len(s4)<=13:   #少3个字需要多3个空白
#     s4=s4+' '
# while len(s5)<=6:   #多3个字需要少3个空白
#     s3=s5+' '
# print(s2+'|')
# print(s1+'|')
# print(s3+'|')
# print(s4+'|')
# print(s5+'|')
def test(s):
    n=0
    for char in s:
        if 64<ord(char)<123:
            n+=1
    temp=len(s)
    while len(s)<=10-temp+n*1:
        s=s+' '
    s=s+'|'
    return s
print(test('西'))
print(test('西湖'))
print(test('西湖醋鱼'))#全是中文的时候对齐了
print(test('西a'))
