"""调试爬虫代码"""

import os
import sys

from scrapy.cmdline import execute

# 将当前路径加入path的搜索路径中
pwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(pwd)

# 调用爬虫

execute(['scrapy', 'crawl', 'cnblog_news'])
