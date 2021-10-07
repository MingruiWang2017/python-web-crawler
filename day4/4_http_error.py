import urllib.request
import urllib.error

"""
url错误，无法解析
raise URLError(err)
urllib.error.URLError: <urlopen error [Errno 11001] getaddrinfo failed>
"""
url = "https://www.asdfva.com"
try:
    response = urllib.request.urlopen(url)
except urllib.error.URLError as e:
    print(e)


"""
url正确，但是不存在对应页面等HTTP错误
raise HTTPError(req.full_url, code, msg, hdrs, fp)
urllib.error.HTTPError: HTTP Error 404: Not Found
"""
url = "https://blog.csdn.net/zjsxxzh/article/details/110"
try:
    response = urllib.request.urlopen(url)
except urllib.error.HTTPError as e:
    print(e.code)
    print(e)