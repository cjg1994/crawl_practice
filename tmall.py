"""
天猫某个商店的爬虫带上cookie就能获取到数据，不带cookie就不行,但是cookie是有时效性的吧，也就是说爬取的时候必须先手动登录把cookie复制出来
如何做到全自动呢,能不能在登录界面用post发送账号密码实现登录先，再访问商品的url
"""

import requests

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    "Cookie":"cna=BnH3FgjyJWYCAXrrkaTOiAeO; tk_trace=1; t=5882496083fb722dc6520fcbb44a7b7f; _tb_token_=e756e65ebeb5e; cookie2=181117769b2fe0ab9e8cf2f7772bcc02; _m_h5_tk=dec83281062acd9c382dd7fab9f05473_1591791007411; _m_h5_tk_enc=c192a8ebc2bba2f757488b07049c3800; pnm_cku822=; dnk=tb7116151_88; tracknick=tb7116151_88; lid=tb7116151_88; lgc=tb7116151_88; login=true; uc1=cookie21=WqG3DMC9FxUx&cookie15=URm48syIIVrSKA%3D%3D&existShop=false&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&pas=0&cookie14=UoTV7X3ZP%2B%2Fi8g%3D%3D; uc3=vt3=F8dBxGDcSpfA1cY7EuQ%3D&nk2=F5RCZIyOBKOh7ktB&id2=UoCJizU3Iha7bg%3D%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D; _l_g_=Ug%3D%3D; uc4=nk4=0%40FY4JikEDlpuGuP9nvdd4kT6i5IpxLjk%3D&id4=0%40UOg1w4pL06XX%2BX%2FlFC1k5sWg%2B34D; unb=1103814772; cookie1=AVTjHEl%2FycRoyJWqNE73LlXx8AoZl9BFwzv6iimoEhY%3D; cookie17=UoCJizU3Iha7bg%3D%3D; _nk_=tb7116151_88; sgcookie=EE9qGrzfSWPDJ8A4cP4G%2F; sg=82e; csg=e90df3f5; cq=ccp%3D0; l=eBaGz6RcQ0L5lCJABOfZhurza77OSIRxXuPzaNbMiOCP9s1p5L3PWZxYH0Y9C3GVh6cBR3yulDhzBeYBqIAg0B9FtZ91w_Hmn; isg=BKOjlLuq-WrR9rXaFKNXoSrcMudNmDfaWwpw-9UA_4J5FMM2XWjHKoFCDuQa54_S"

}
# headers={
#     "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
# }
url="https://semir.tmall.com/i/asynSearch.htm?_ksTS=1591783594894_117&callback=jsonp118&mid=w-18687831015-0&wid=18687831015&path=/search.htm&search=y&spm=a1z10.3-b-s.w5003-22094443291.6.3e726d6aLvB5f0&keyword=%C4%D0%B3%C4%C9%C0&orderType=hotsell_desc&scene=taobao_shop"
resp=requests.get(url,headers=headers)
print(len(resp.text))
