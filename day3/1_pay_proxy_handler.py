import urllib.request


# 付费代理使用
# 1.使用用户名密码: 通过带验证的处理器来发送
# 2.使用密码管理器传递用户名密码: 速度较快，可以使用IP池


# 第一种方式
def pay_proxy_handler1():
    # 1.代理IP
    pay_proxy = {"http": "username:password@192.168.12.11:8080"}  # ssh登录格式
    # 2.创建handler
    proxy_handler = urllib.request.ProxyHandler(pay_proxy)
    # 3.通过处理器创建opener
    proxy_opener = urllib.request.build_opener(proxy_handler)
    # 4.发送请求
    response = proxy_opener.open("http://www.baidu.com", timeout=5)
    print(response)


# 第二种方式
def pay_proxy_handler2():
    # 1.准备用户信息及IP信息
    user_name = "zhangsan"
    password = "123@qwer"
    pay_proxy = "192.168.1.122:8080"
    # 2.创建密码管理器，添加用户名、密码
    password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    # uri统一资源标识符 uri>url
    # url统一资源定位器
    password_manager.add_password(None, pay_proxy, user_name, password)
    # 3.创建可以验证代理IP的handler
    proxy_auth_handler = urllib.request.ProxyBasicAuthHandler(password_manager)
    # 4.创建opener
    proxy_opener = urllib.request.build_opener(proxy_auth_handler)
    # 5.发送请求
    response = proxy_opener.open("http://www.baidu.com", timeout=5)
    print(response)
    print(response.read().decode())


if __name__ == '__main__':
    # pay_proxy_handler1()
    print("-" * 30)
    pay_proxy_handler2()
