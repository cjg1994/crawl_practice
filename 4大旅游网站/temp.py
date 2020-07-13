# __jsl_clearance=1583999345.859|0|eMzjf%2Fi5YaZk1lDfaaTJtS2R0%3D
# __jsluid_h=a57840ef448e3a840d3d5c26cca0136b
new_headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    # "cookie":"__jsluid_h=1e790a2ed4b4b13cbb3ca2f1fe1d043f;__jsl_clearance=1583999580.19|0|qfB7PisseS21aJgK88IqTe0AJAQ%3D"
    "cookie":"__jsluid_h=9d696399de9d549de5c3812bf4856807;__jsl_clearance=1584002140.279|0|z3BQr90s7swfYz66w2%2Fd3sI%3D"
}
import requests
#测试发现同一个cookie，不同的UserAgent返回的响应结果居然是不同的 难道是我交叉使用了Chrome和360浏览器时useragent混用导致了错误?
resp=requests.get("http://www.mafengwo.cn/i/6523133.html",headers=new_headers)
print(resp)
