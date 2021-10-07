import urllib.request
import urllib.parse
from http import cookiejar

"""
获取个人中心页面

1. 代码登录，登陆成功，返回有效的cookie
2. 自动带着cookie去请求个人中心


cookiejar 可以自动保存cookie
"""

# 1. 代码登录

# 服务器根据发送请求的方式来判断返回页面的内容：
# get请求：返回登录页面；
# post请求： 返回登陆结果。

# 1.1 登录的网址
login_url = "https://www.yaozh.com/login"

# 1.2 登录的参数
"""
其中有一些前段隐藏域参数, 如
需要登录之前，在登录页网址上使用GET获取对应登录参数。
type: 0
username: rui_medicine
pwd: Medicine_RUI@123
country: 86_zh-CN
mobile: 
vcode: 
pincode: 
formhash: 6B41E49B0B
backurl: https%3A%2F%2Fwww.yaozh.com%2F
"""
login_form_data = {
    "type": "0",
    "username": "rui_medicine",
    "pwd": "Medicine_RUI@123",
    "country": "86_zh-CN",
    "formhash": "432C0E4EEB",
    "backurl": "https%3A%2F%2Fwww.yaozh.com%2F"
}
# post请求参数需要转码为bytes
login_form_info = urllib.parse.urlencode(login_form_data).encode('utf-8')
# 1.3 发送POST登录请求
cookie_jar = cookiejar.CookieJar()
# 定义有添加 cookie 功能的 handler
cookie_handler = urllib.request.HTTPCookieProcessor(cookie_jar)
# handler创建opener
cookie_opener = urllib.request.build_opener(cookie_handler)

# 带着data参数发送POST请求
# 添加请求头
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}
login_request = urllib.request.Request(login_url, data=login_form_info, headers=header)
# 如果登录成功，cookiejar将自动保存cookie
response = cookie_opener.open(login_request)

# 2. 代码带着cookie去访问个人中心
center_url = "https://www.yaozh.com/member/"
center_request = urllib.request.Request(center_url, headers=header)
# 使用带有cookie的opener打开个人中心
response = cookie_opener.open(center_request)
data = response.read()

with open("3_yaozh_with_cokie.html", 'wb') as f:
    f.write(data)
