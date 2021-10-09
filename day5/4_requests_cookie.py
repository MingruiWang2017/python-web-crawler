import requests

# 请求数据的url
member_url = "https://www.yaozh.com/member"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}

cookies = "_ga=GA1.2.612799267.1633420793; yaozh_userId=1148931; UtzD_f52b_saltkey=r1ownN8D; UtzD_f52b_lastvisit=1633417486; yaozh_uidhas=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217c4f7d305913a-020fbf6cddb434-b7a1b38-3686400-17c4f7d305a9bb%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%7D%2C%22%24device_id%22%3A%2217c4f7d305913a-020fbf6cddb434-b7a1b38-3686400-17c4f7d305a9bb%22%7D; UtzD_f52b_ulastactivity=1633398086%7C0; Hm_lvt_65968db3ac154c3089d7f9a4cbb98c94=1633420793,1633525782; acw_tc=2f624a3e16336633686481041e060ef6c6723a82eeb846196532af46d9a403; PHPSESSID=binnv54n997sglsdjph5all640; _gid=GA1.2.1059097269.1633663369; _gat=1; yaozh_logintime=1633663374; yaozh_user=1148931%09rui_medicine; yaozh_jobstatus=kptta67UcJieW6zKnFSe2JyYnoaSaJltnpeWg26qb21rg66flM6bh5%2BscZJqbIXX18rD0cabzpjO0sqDbqpvcWuDpZKm1ZXZzaacg3OlnZa5baB5D39C699Ce99B5A3385359Ab65E4Sm4aVl2qYapeanJhpWXCra5VzU6fKo8qGdKqbaWWdh5OXl5eXbZhonJmcl2ZZcLU%3Dd000046e062c1d654d4b7cfd485604f8; db_w_auth=929964%09rui_medicine; UtzD_f52b_lastact=1633663375%09uc.php%09; UtzD_f52b_auth=3ab5IsmCH7Cwtv9IKm4Bb9vWE5nY8BzpEBqSXQlfipRbYhr2xGKAX9W7ovh678Mz76P47Mm2TdEJasxbWWM5dqZhEw8; yaozh_mylogin=1633663377"


def convert_cookie_str_2_dict(cookies_str: str):
    """将字符串类型的cookies转换为字典"""
    # cookies_dict = {}
    # cookies_list = cookies_str.split("; ")
    # for cookie in cookies_list:
    #     key = cookie.split("=")[0]
    #     value = cookie.split("=")[1]
    #     cookies_dict[key] = value
    # return cookies_dict
    return {cookie.split("=")[0]: cookie.split("=")[1] for cookie in cookies_str.split("; ")}


# requests需要的cookies是字典或者CookieJar
cookie_dict = convert_cookie_str_2_dict(cookies)
print(cookie_dict)

response = requests.get(member_url, headers=headers, cookies=cookie_dict)
print(response.status_code)

data = response.content
with open("4_cookie.html", 'wb') as f:
    f.write(data)