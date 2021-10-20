import requests
import re
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

"""爬取抖音搜索的视频内容"""

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "Cookie": "ttwid=1%7Cos7om3ADYMveWRqslx_wN1yIEAK8LfBwDmF5v1C9t9Q%7C1634300032%7C58fc5f1b70c9f2f1f0a588f2113a80fd9574980a6403579c594c5e77c4dd4633; __guid=197290409.-66197414298014080000.1634300031803.5217; _tea_utm_cache_6383=undefined; douyin.com; MONITOR_WEB_ID=cf2f5f4c-7765-4649-8054-39967a97c5d5; passport_csrf_token_default=7848e7066d9e879cbda8561cb8501d02; passport_csrf_token=7848e7066d9e879cbda8561cb8501d02; s_v_web_id=verify_kusc1km9_3GtCTZ7z_okal_4p0z_ARwv_iTw2Bmg0chTj; _tea_utm_cache_1300=undefined; odin_tt=6c2f95e2aca1209d9512d15b712fc453fa08692a20067100019966acf6cca17b0def3973ddaf933e02b09a754d19f8d2dc36ad1b569592ef1fe0dff1377c2777; ttcid=5192ae7c0f8b40cbb0c206e76adef26f39; __ac_nonce=06169734e0014d26e702b; __ac_signature=_02B4Z6wo00f01GqzNswAAIDBvXUbtbaJDmRqkzJAAHvNg4FOt3aUY9rtX2kzMfxapT7UsYhUJzCg2sJTli6y1Uk7ggRiOUSceZbNJQ8tUlCC7UC76bOYymKRx-50ulAaVVXfIg5JLFLY.Eyib3; msToken=PAzie2gQyBgycs4w6x14BDm6ttIJKnqiLewgdc3FeRe_-wtUUpY1e8HNXzwXgc3d83vsDSHVgINUHNMwlmDAKKoeqACYqPNxof8EUjYfLgf3UNA99QNmGME2; msToken=cPcvxYtZXJ8TeMlhvo-kD32Fafhqant3D5wimB6bTFAlynJ4th6h381pAv10zVja6GHqBNxvfG9Al_YTCI6sTuBEpWRhQ_74vmomlIRhJqLm7dk2vCIQRW6l; tt_scid=jLWOm4cZVRrZOF1QS6Ez9Ul4ShLo6v8EcxdQ-4mqh2JzqdVKfvpSiLJe2pHxszcc9ee6; monitor_count=14"
}


def search(key):
    video_page_list = []
    # 需要下载安装chrome驱动
    driver = webdriver.Chrome(r"D:\code\爬虫\python-web-crawler\dya7\douyin\chromedriver.exe")
    driver.get("https://www.douyin.com/search/%E8%8E%89%E8%8E%89%E5%B4%BD")
    # 网页打开后会出现验证码
    time.sleep(3)
    roll_down(driver)
    print("_" * 100)
    lis = driver.find_elements(By.XPATH, '//a[@class="caa4fd3df2607e91340989a2e41628d8-scss a074d7a61356015feb31633ad4c45f49-scss b388acfeaeef33f0122af9c4f71a93c9-scss"]')
    for li in lis:
        video_page_list.append(li.get_attribute("href"))
    driver.quit()
    return video_page_list



def roll_down(driver):
    """使用JavaScript执行页面下滑操作"""
    for x in range(1, 30, 4):  # 在不断下滑的过程中，页面高度也会变化
        time.sleep(1)
        j = x / 9
        # document.documentElement.scrollTop #指定滚动条的位置
        # document.documentElement.scrollHeight #获取浏览器页面的最大高度
        js = "document.documentElement.scrollTop = document.documentElement.scrollHeight * %f" % j
        driver.execute_script(js)



def get_video_url(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    title = soup.find(name='title').get_text().strip().split("-")[0]
    # 去除标题中的特殊字符
    title = re.sub('[^\w]', "", title)
    title.replace("\\/:*?\"><|", "")

    json_bytes = soup.select('#RENDER_DATA')[0].get_text()
    json_str = requests.utils.unquote(json_bytes)  # 解码url编码格式的数据
    video_info = json.loads(json_str)
    video_url = "https:" + video_info["C_19"]["aweme"]["detail"]["video"]["playAddr"][0]["src"]
    return (title, video_url)


def download_video(title, video_url):
    response = requests.get(video_url, headers=headers)
    video = response.content
    save_video(title, video)
    print("保存成功：", title)


def save_video(title, video):
    with open("videos\\{}.mp4".format(title), 'wb') as f:
        f.write(video)


if __name__ == "__main__":
    video_page_urls = search("莉莉崽")
    for page_url in video_page_urls:
        title, video_url = get_video_url(page_url)
        download_video(title, video_url)
