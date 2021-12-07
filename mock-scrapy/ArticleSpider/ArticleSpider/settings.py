# Scrapy settings for ArticleSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ArticleSpider'

SPIDER_MODULES = ['ArticleSpider.spiders']
NEWSPIDER_MODULE = 'ArticleSpider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 8
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Accept-Language': 'zh-CN,zh;q=0.9',
  'Cookie': '_ga=GA1.2.638297868.1633745158; __gads=ID=739d2c8f50f3817a:T=1636449196:S=ALNI_MZI0o-kA3E909wGrT2LTv7eMRCMtw; .Cnblogs.AspNetCore.Cookies=CfDJ8FO3GXnjClZGrNGr2Ic8Z1ouGfZjQQt5s98YQmnay2MRbQEtyu0E6JNLobv8P3f0LL85LZNBulDCUQw5K8QD4lJ47jhYwMVtlo4NK_jyAaAEL056QEpUJ7wdh00Ruv_V2s2BUmC8LP5SbR1wYvvcchmi6NvYLjm4NruzVRNIDQnoZvalryouZv0kcPZW0kqOl5bRRJx0wgSNHMa-O1hBNml_ZPOgcV4mzcF1KwQ2CR4RVnsyn7F61S3D_jt3SVC5VeMxR9iJxJztWUg7Z39zTN_TFJDiclllHBGhCnAP7U4mo6aqPG65JHOeBCA-_awbHIUGx2CFqASCMsemhFh_Jt8phOKMmFRo9zTAmtXqyeFn_GgadG-QfKUeARN17KAMbpSDvbBEH2dpOm_2YIsl7V6jxLMG2-xOA16QEUjquDfZE8Vx0MA8hX_WdlVdmfxyQW6ykREzteS5trH132Hm46U7r3-kCVJI1Th4X5kIj4m-q9iS-iOw3D8lDQvoH1LQ8v_vs50861sPQANjFU68nvab4fRJlYGoM0KUttjYz8jHa-Yrkdws0L6Vvw6eDEoFr-hL5RAx74Hjh1ImvL1sKQs; .CNBlogsCookie=0B810BAC80EA985972C4F504B87E4E890FEDB2676FC473E3689794200013626D1712563B0F11374A0A725CFEF9A0A8480A72AE14ADD17E4A11D1D6D8C5BA2932B9B3BB6E3F52284EFC6F13141775257B3758ED7E; Hm_lvt_866c9be12d4a814454792b1fd0fed295=1638602670,1638690859,1638696031,1638801470; Hm_lpvt_866c9be12d4a814454792b1fd0fed295=1638801470; affinity=1638801473.318.548.742598; __utma=66375729.638297868.1633745158.1638609426.1638801473.7; __utmc=66375729; __utmz=66375729.1638801473.7.4.utmcsr=cnblogs.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1; __utmb=66375729.1.10.1638801473'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'ArticleSpider.middlewares.ArticlespiderSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'ArticleSpider.middlewares.ArticlespiderDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'scrapy.pipelines.images.ImagesPipeline': 1,
    "ArticleSpider.pipelines.ArticleImagePipeline": 1,
    "ArticleSpider.pipelines.JsonWithEncodingPipeline": 2,
    "ArticleSpider.pipelines.JsonExporterPipeline": 3,
    "ArticleSpider.pipelines.MysqlTwistedPipeline": 4,
    'ArticleSpider.pipelines.ArticlespiderPipeline': 300,
}

# 指定下载图片的字段，如果在item中指定的字段是image_urls的话，可以不用指定
IMAGES_URLS_FIELD = "front_image_url"

# 指定图片的存储路径
import os
import sys
path = os.path.dirname(os.path.abspath(__file__))
IMAGES_STORE = 'images'  # 也可以，默认是在项目目录下寻找images文件夹
# IMAGE_STORE = os.path.join(path, "images")

# MySQL数据库配置
MYSQL_HOST = "192.168.73.130"
MYSQL_PORT = 3306
MYSQL_DBNAME = "article_spider"
MYSQL_USER = "spider"
MYSQL_PASSWORD = "123456"



# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
