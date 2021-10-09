import requests

# 请求数据的url
member_url = "https://www.yaozh.com/member"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}

# session类，可以自动保存cookie
session = requests.session()

# 1. 代码登录
login_url = "https://www.yaozh.com/login"
login_form_data = {
    "type": "0",
    "username": "rui_medicine",
    "pwd": "Medicine_RUI@123",
    "country": "86_zh-CN",
    "formhash": "7DDCB5349C",
    "backurl": "https%3A%2F%2Fwww.yaozh.com%2F"
}
try:
    login_res = session.post(login_url, data=login_form_data, headers=headers)
except requests.RequestException as e:
    print(e)
if login_res.status_code == 200:
    print("登陆成功。", login_res.json())

# 2. 登录成功后，带着有效的cookie访问目标页面
data_response = session.get(member_url, headers=headers)
print(data_response.status_code)

with open("5_cookie.html", 'wb') as f:
    f.write(data_response.content)
