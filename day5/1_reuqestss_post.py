import requests

# 发送post请求
url = ""
data = {

}
response = requests.post(url, data=data)

# 内网需要认证
auth = (user, pwd) # 元组
response = requests.get(url, auth=auth)