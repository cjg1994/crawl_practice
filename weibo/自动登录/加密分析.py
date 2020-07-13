"""
, makeRequest = function(a, b, c, d) {
  var e = {                           这里e是一个对象，说明是post发送的数据对象
      entry: me.getEntry(),
      gateway: 1,
      from: me.from,
      savestate: c,
      qrcode_flag: d,
      useticket: me.useTicket ? 1 : 0
  };
  me.failRedirect && (me.loginExtraQuery.frd = 1);
  e = objMerge(e, {
      pagerefer: document.referrer || ""
  });
  e = objMerge(e, me.loginExtraFlag);
  e = objMerge(e, me.loginExtraQuery);
  e.su = sinaSSOEncoder.base64.encode(urlencode(a));
  me.service && (e.service = me.service);
  if (me.loginType & rsa && me.servertime && sinaSSOEncoder && sinaSSOEncoder.RSAKey) {
      e.servertime = me.servertime;
      e.nonce = me.nonce;
      e.pwencode = "rsa2";
      e.rsakv = me.rsakv;
      var f = new sinaSSOEncoder.RSAKey;
      f.setPublic(me.rsaPubkey, "10001");
      b = f.encrypt([me.servertime, me.nonce].join("\t") + "\n" + b) 猜测这里的me.servertime应该是和预登录请求返回的一样,JS文件中确实有这样设置的函数
  } else if (me.loginType & wsse && me.servertime && sinaSSOEncoder && sinaSSOEncoder.hex_sha1) {
      e.servertime = me.servertime;     设置servertime
      e.nonce = me.nonce;               设置nonce   这个值也是变化的，每次生成都是和随机书有关，但是每一次的登录请求都是产生一个值，这个值在预登录请求返回的数据中包含了
      e.pwencode = "wsse";
      b = sinaSSOEncoder.hex_sha1("" + sinaSSOEncoder.hex_sha1(sinaSSOEncoder.hex_sha1(b)) + me.servertime + me.nonce)
  }
  e.sp = b;        这里设置了sp的值 说明是根据每次请求的预登录请求返回的数据再利用rsa算法或者哈希算法加密,可以看到代码中有elif if分支

  var makeNonce = function(a) {
        var b = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
          , c = "";
        for (var d = 0; d < a; d++)
            c += b.charAt(Math.ceil(Math.random() * 1e6) % b.length);
        return c
    }

前两次登录微博返回的都不是个人主页，而是需要抓取url继续访问，自己构造出个人微博的url
有些返回数据在开发者工具上不显示，可以借助抓包软件，或者自己请求一下 看看html.text的值
                    }try{sinaSSOController.crossDomainAction('login',function(){location.replace('https://passport.weibo.com/wbsso/login?ssosavestate=1607480705&url=https%3A%2F%2Fweibo
.com%2Fajaxlogin.php%3Fframelogin%3D1%26callback%3Dparent.sinaSSOController.feedBackUrlCallBack&display=0&ticket=ST-MzIwNjMxMjY2MA==-1575944705-gz-4199522B4BFB220B8E3726F456251108-
1&retcode=0');});}
                catch(e){
  """
