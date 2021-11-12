# Scrapy settings for hookasync project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'hookasync'

SPIDER_MODULES = ['hookasync.spiders']
NEWSPIDER_MODULE = 'hookasync.spiders'


EXTENSIONS = {"hookasync.extensions.HookasyncExtension": 100}
DOWNLOADER_MIDDLEWARES = {
    "hookasync.extensions.HookasyncDownloaderMiddleware": 100
}

SPIDER_MIDDLEWARES = {"hookasync.extensions.HookasyncSpiderMiddleware": 100}
ITEM_PIPELINES = {"hookasync.extensions.HookasyncPipeline": 100}

# disable S3
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""