import urllib.request


# auth认证一般用于爬取自己公司的数据，进行数据分析
# 使用管理员权限登录获取所有数据

def auth_internal_net():
    # 1.用户名、密码
    user = "admin"
    pwd = "admin123"
    internal_net = "http://192.168.1.233:8080"

    # 2.创建密码管理器
    pwd_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    pwd_manager.add_password(None, internal_net, user, pwd)

    # 3.创建认证处理器
    auth_handler = urllib.request.HTTPBasicAuthHandler(pwd_manager)

    # 4.创建opener
    auth_opener = urllib.request.build_opener(auth_handler)

    # 5.请求数据
    response = auth_opener.open("http://www.baidu.com", timeout=5)
    print(response)
    print(response.read().decode())


if __name__ == '__main__':
    auth_internal_net()
