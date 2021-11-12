# Scrapy settings for properties project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'properties'

SPIDER_MODULES = ['properties.spiders']
NEWSPIDER_MODULE = 'properties.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'properties (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'properties.pipelines.tidyup.TidyUp': 100,
    # 'properties.pipelines.redis.RedisCache': 300,  # 该管道要放在geo之前，先从缓存中查数据
    # 'properties.pipelines.geo.GeoPipeline': 400,  # 转换地理编码要放在保存数据之前
    # 'properties.pipelines.geo2.GeoPipeline': 400,
    'properties.pipelines.computation.UsingBlocking': 500,
    # 'properties.pipelines.mysql.MysqlWriter':700,
    # 'properties.pipelines.es.EsWriter': 800,
}

MYSQL_PIPELINE_URL = "mysql://root:pass@192.168.73.130:3406/properties"

REDIS_PIPELINE_URL = "redis://192.168.73.130:6399"

EXTENSIONS = {'properties.latencies.Latencies': 500}
LATENCIES_INTERVAL = 5

ES_PIPELINE_URL = "http://192.168.73.130:9200/properties/property/"

LEGACY_CONCURENCY = 16

LOG_LEVEL = "INFO"

# disable S3
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
