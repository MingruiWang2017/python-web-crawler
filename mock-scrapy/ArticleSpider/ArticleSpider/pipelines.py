# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import codecs
import MySQLdb

from MySQLdb.cursors import DictCursor
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi


class ArticlespiderPipeline:
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    """自定义json文件导出管道"""

    def __init__(self):
        self.file = codecs.open("articles.json", 'a', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_close(self, spider):
        self.file.close()


class MysqlPipeline(object):
    """数据库同步写入方法"""

    def __init__(self):
        self.conn = MySQLdb.connect(host="192.168.73.130", port=3306,
                                    user="spider", password="123456",
                                    database="article_spider", charset='utf8',
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into article(title, url, url_md5, front_image_url, front_image_path, like_nums, comment_nums, view_nums, tags, content, create_date)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE view_nums=VALUES(view_nums)
        """  # 当主键发生冲突时，只更新view_nums字段
        params = []
        params.append(item.get('title'))
        params.append(item.get('url'))
        params.append(item.get('url_md5'))
        front_image_list = item.get('front_image_url', [])
        params.append(",".join(front_image_list))
        params.append(item.get('front_image_path', ''))
        params.append(item.get('like_nums', 0))
        params.append(item.get('comment_nums', 0))
        params.append(item.get('view_nums', 0))
        params.append(item.get('tags', ''))
        params.append(item.get('content', ''))
        params.append(item.get('create_date', '1970-07-01'))

        self.cursor.execute(insert_sql, tuple(params))
        self.conn.commit()

        return item

    def spider_close(self, spider):
        self.conn.close()


class MysqlTwistedPipeline(object):
    """数据库异步写入方法"""

    @classmethod
    def from_settings(cls, settings):
        """从settings.py配置文件读取配置参数"""
        dbparams = {
            'host': settings.get('MYSQL_HOST'),
            'port': settings.get('MYSQL_PORT'),
            'database': settings.get('MYSQL_DBNAME'),
            'user': settings.get('MYSQL_USER'),
            'password': settings.get('MYSQL_PASSWORD'),
            'charset': 'utf8',
            'use_unicode': True,
            'cursorclass': DictCursor,
        }

        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)
        return cls(dbpool)

    def __init__(self, dbpool: adbapi.ConnectionPool):
        self.dbpool = dbpool

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)  # 声明对数据库使用什么方法和参数进行操作
        query.addErrback(self.handle_error, item, spider)  # 设置写入数据库错误时的回调方法和参数

        return item

    def do_insert(self, cursor: adbapi.Transaction, item):
        """cursor是方法自带的参数"""
        sql = """
            insert into article values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE view_nums=VALUES(view_nums)
        """  # 当主键发生冲突时，只更新view_nums字段

        params = []
        params.append(item.get('title'))
        params.append(item.get('url'))
        params.append(item.get('url_md5'))
        front_image_list = item.get('front_image_url', [])
        params.append(",".join(front_image_list))
        params.append(item.get('front_image_path', ''))
        params.append(item.get('like_nums', 0))
        params.append(item.get('comment_nums', 0))
        params.append(item.get('view_nums', 0))
        params.append(item.get('tags', ''))
        params.append(item.get('content', ''))
        params.append(item.get('create_date', '1970-07-01'))

        cursor.execute(sql, tuple(params))

    def handle_error(self, failure, item, spider):
        """failure是方法自带的参数，即报错原因"""
        print("MySQL operate ERROR: ", failure)
        print("spider: %s, item: %s" % (spider, item))

    def spider_close(self, spider):
        self.dbpool.close()


class JsonExporterPipeline(object):
    """使用JsonItemExporter导出item为json文件"""

    def __init__(self):
        self.file = open('articles_export.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def spider_close(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


# 继承ImagePipeline，添加功能：记录图片的保存路径
class ArticleImagePipeline(ImagesPipeline):

    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            image_file_path = ""
            for ok, value in results:
                image_file_path = value['path']
            item['front_image_path'] = image_file_path

        return item
