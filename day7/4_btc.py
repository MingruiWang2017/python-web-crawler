import requests
import json
from bs4 import BeautifulSoup

"""
获取巴比特网站中的区块链项目页，以及各项目页中的文章链接
"""


class BtcSpider(object):
    def __init__(self):
        self.url = "https://www.8btc.com/project"
        self.base_url = "https://www.8btc.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        }
        self.data = {}
        self.projects = []
        self.data["projects"] = self.projects

    # 1.发送请求
    def get_response(self, url, params=None):
        if url:
            response = requests.get(url, params, headers=self.headers)
        else:
            response = requests.get(self.url, params, headers=self.headers)
        return response.content.decode()

    # 2.1 解析数据：获取所有项目
    def get_projects(self, data):
        soup = BeautifulSoup(data, 'lxml')
        projects_title = soup.select('.project-item div.project-item__header a div.project-item__title.link-dark-major')
        projects_url = soup.select('.project-item div.project-item__header a')
        for title, url in zip(projects_title, projects_url):
            project_name = title.get_text().strip()
            project_url = self.base_url + url.get("href")
            self.projects.append({"name": project_name, "url": project_url})

    # 2.2 解析数据：获取各个项目下的文章
    def get_project_articles(self, data):
        soup = BeautifulSoup(data, 'lxml')
        articles_title = soup.select('article div div a h3')
        articles_url = soup.select('article div div a')
        articles = []
        for title, url in zip(articles_title, articles_url):
            article_title = title.get_text().strip()
            article_url = self.base_url + url.get("href")
            articles.append({article_title: article_url})
        return articles

    # 3. 保存数据
    def save_data(self):
        with open("4_projects_articles.json", 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False)

    # 运行程序
    def run(self):
        # 1. 获取项目页，共9页
        print("get page: ", end="")
        for page in range(1, 10):
            print(page, end=" ")
            params = {"field": 1, "page": page}
            projects_data = self.get_response(self.url, params=params)
            self.get_projects(projects_data)
        projects_num = len(self.projects)
        self.data["projects_num"] = projects_num

        # 2. 获取各项目页的第一页文章
        print("\nget article: ", end="")
        for project in self.projects:
            print(project['name'], end=" ")
            artical_data = self.get_response(project["url"])
            articles = self.get_project_articles(artical_data)
            project["articles_num"] = len(articles)
            project["articles"] = articles

        # 3. 保存数据
        print("\nsave data ...")
        self.save_data()


if __name__ == '__main__':
    btc = BtcSpider()
    btc.run()
