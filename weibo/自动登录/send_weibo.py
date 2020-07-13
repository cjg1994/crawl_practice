"""
自动发布微博
分析：登录以后可以发微博，不考虑发视频的情况，发表纯文字或者图片加文字
假设发表 爬虫测试 四个字
因为是向服务器提交数据，考虑POST方法，找到请求的url和请求参数
url='https://weibo.com/aj/mblog/add?ajwvr=6&__rnd=1575961335784'    这一串数字猜测是时间戳
method:POST
请求参数：
ajwvr: 6
__rnd: 1575961335784   时间戳
Post方法发送的form_data如下：
location: v6_content_home
text: 爬虫测试   提交的文本
appkey:
style_type: 1
pic_id:
tid:
pdetail:
mid:
isReEdit: false
rank: 0
rankid:
module: stissue
pub_source: main_
pub_type: dialog
isPri: 0
_t: 0
现在再尝试发送纯文本，
url='https://weibo.com/aj/mblog/add?ajwvr=6&__rnd=1575961660979'
请求参数为：  对比发现也就是时间戳和text发生变化
ajwvr: 6
__rnd: 1575961660979
post方法的Form data为：
location: v6_content_home
text: 纯文本测试
appkey:
style_type: 1
pic_id:
tid:
pdetail:
mid:
isReEdit: false
rank: 0
rankid:
module: stissue
pub_source: main_
pub_type: dialog
isPri: 0
_t: 0

接着发送文字加图片，并尝试把公开选为仅自己可见根据请求参数推测一些空值将被填写上，当你添加图片时，相当于发送一个让服务器存储图片的请求，服务器赋予一个唯一id
url='https://weibo.com/aj/mblog/add?ajwvr=6&__rnd=1575961943336'
post的数据为：
location: v6_content_home
text: 这是一张图片
appkey:
style_type: 1
pic_id: bf1c72d4ly1g9rnb0d1a0j211s0dagnz  发表图片也就是这个参数被填写上了值，
tid:
pdetail:
mid:
isReEdit: false
gif_ids:
rank: 1
rankid:
module: stissue
pub_source: main_
updata_img_num: 1
pub_type: dialog
isPri: null
_t: 0

接着再发送加图片，仅自己可见改为公开，发生错误，文字是必填的。
location: v6_content_home
text: 图片的测试二
appkey:
style_type: 1
pic_id: bf1c72d4ly1g9rneg9wagj211s0dagnz
tid:
pdetail:
mid:
isReEdit: false
gif_ids:
rank: 0          说明这个参数0表示公开 1表示尽自己可见
rankid:
module: stissue
pub_source: main_
updata_img_num: 1
pub_type: dialog
isPri: null
_t: 0
现在要找出图片的pic_id，然后构造出Form-data， 发送图片的时候，图片在本地转换为字节流，并用base64加密，再向服务器发送加密过的数据
这就需要找到添加图片这一操作发起的请求
看到一个pic_upload.php文件，说明是处理图片上传的，分析这个文件找出图片id是如何产生的
分析pic_upload.php 请求url很长，方法是POST，FormData是b64_data
url='https://picupload.weibo.com/interface/pic_upload.php?cb=https%3A%2F%2Fweibo.com%2Faj%2Fstatic%2Fupimgback.html%3F_wv%3D5%26callback%3DSTK_ijax_1575961274296471&mime=image%2Fjpeg&data=base64&url=weibo.com%2Fu%2F3206312660&markpos=1&logo=1&nick=%40%E5%8F%AA%E4%B8%BA%E4%B8%9C%E6%96%B9&marks=0&app=miniblog&s=rdxt&pri=null&file_source=1'
utl='https://picupload.weibo.com/interface/pic_upload.php?cb=https://weibo.com/aj/static/upimgback.html?_wv=5&callback=STK_ijax_1575961274296471&mime=image/jpeg&data=base64&url=weibo.c
om/u/3206312660&markpos=1&logo=1&nick=@只为东方&marks=0&app=miniblog&s=rdxt&pri=null&file_source=1'
请求参数为：
cb: https://weibo.com/aj/static/upimgback.html?_wv=5&callback=STK_ijax_1575961274296471
mime: image/jpeg
data: base64
url: weibo.com/u/3206312660
markpos: 1
logo: 1
nick: @只为东方
marks: 0
app: miniblog
s: rdxt
pri: null
file_source: 1
将图片转换为字节流，再用base64加密，然后发送给服务器的url,这个请求的返回数据在开发者工具中显示不出来
利用Fillder抓包工具可以看到Response的数据 Raw选项卡下有个Location参数可以提取出pid
4658 bf1c72d4ly1g9ru7gqgewj202800p742
"""
