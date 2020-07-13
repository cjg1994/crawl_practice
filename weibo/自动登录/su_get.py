"""
对账号进行base64加密,密码进行rsa加密
"""
import urllib.parse
import base64
import rsa
import binascii

#账号加密
def get_su(username):
    username_quote=urllib.parse.quote_plus(username) #JS文件中是对账号的编码 urlencode(a) 进行加密，主要是将@等特殊符号转换成url中能够识别的字符
    username_base64=base64.b64encode(username_quote.encode('utf-8')) #这里为什么要encode('utf-8')，因为base64.b64encode()参数是字节类型
    return username_base64.decode('utf-8') #将转换成的字节类型再按照同一个编码转换成字符串

#密码加密，servertime,nonce,pubkey来自预登录请求的数据
#var f = new sinaSSOEncoder.RSAKey;
# f.setPublic(me.rsaPubkey, "10001"); 这里的两个参数都是16进制
#b = f.encrypt([me.servertime, me.nonce].join("\t") + "\n" + b)
#原JS文件中创建公钥的语句
def get_password(password,servertime,nonce,pubkey):
    rsaPublickey=int(pubkey,16) #将16进制的我pubkey转换成十进制
    #创建公钥
    key=rsa.PublicKey(rsaPublickey,65537)#10001转换成十进制，说明python中创建公钥的rsa.PublicKey参数是十进制的。转换为RSA可使用的十进制类型
    #拼接明文
    message=str(servertime)+'\t'+str(nonce)+'\n'+str(password)
    message=message.encode('utf-8') #加密函数的参数是bytes类型
    #加密函数
    passwd=rsa.encrypt(message,key)
    #将加密信息转换为16进制
    #可使用binascii来讲密文格式化输出.
    #利用binascii模块可以将十六进制显示的字节转换成我们在加解密中更常用的显示方式
    passwd=binascii.b2a_hex(passwd)  #后面把这行去掉测试了一下发现也没问题
    return passwd
if __name__=='__main__':
    password='123456'
    servertime='1575874774'
    nonce='6SCK19'
    pubkey='EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'
    print(get_password(password,servertime,nonce,pubkey))
    #这里每次返回的密文还都不一样，百度了一下关于填充数据
