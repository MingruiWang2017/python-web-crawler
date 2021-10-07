import requests
import pprint


class RequestSpider(object):
    def __init__(self, url, headers=None):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        }
        if headers:
            self.headers.update(headers)
        self.response = None


    def run(self):
        self.response = requests.get(self.url, headers=self.headers)
        data = self.response.content

        # 1.获取请求头
        request_headers = self.response.request.headers
        pprint.pprint(request_headers)

        # 2.获取响应头
        response_headers = self.response.headers
        pprint.pprint(response_headers)

        # 3.获取状态码
        code = self.response.status_code
        print(code)

        # 返回的cookie内容是一个CookieJar对象
        # 4.请求的Cookie
        request_cookie = self.response.request._cookies
        print(request_cookie)

        # 5.响应的Cookie
        response_cookie = self.response.cookies
        print(response_cookie)


if __name__ == '__main__':
    req = RequestSpider("http://www.baidu.com")
    req.run()
