import urllib.request

# 直接获取个人中心页面
# 登陆之后手动复制PC页面抓取的 Cookies
# 放在request的headers中

# 1. 请求url
url = "https://www.yaozh.com/member/"
# rui_medicine
# Medicine_RUI@123

# 2.添加请求头
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "Cookie": "PHPSESSID=ajlb7hncl3hm9crha4s9rotn50; __guid=124546700.76720536397698380000.1633397878207.0037; _ga=GA1.2.1661715685.1633397878; _gid=GA1.2.1490108961.1633397878; Hm_lvt_65968db3ac154c3089d7f9a4cbb98c94=1633397879; yaozh_logintime=1633398086; yaozh_user=1148931%09rui_medicine; yaozh_userId=1148931; yaozh_jobstatus=kptta67UcJieW6zKnFSe2JyYnoaSaJltnpeWg26qb21rg66flM6bh5%2BscZJqbIXX18rD0cabzpjO0sqDbqpvcWuDpZKm1ZXZzaacg3OlnZa03839c57a05364DC5Af70FeFEE253297Sm4aVl2qYaJ6clZlpWXCra5VzU6fKo8qGdKqbaWWdh5OXl5eUcJ1lnZ2alWVZcLU%3D449a25d68dca5df62bff8341987fd4c0; yaozh_uidhas=1; yaozh_mylogin=1633398093; monitor_count=10; Hm_lpvt_65968db3ac154c3089d7f9a4cbb98c94=1633398165"
}
# 3.构建请求对象
req = urllib.request.Request(url, headers=header)
#  4. 发送请求
res = urllib.request.urlopen(req)

data = res.read()

with open("2_yaozh_with_cookie.html", 'wb') as f:
    f.write(data)
