import traceback
import dj_database_url  # 该库用于解析数据库连接中的字段
import MySQLdb  # mysqlclient库

from twisted.internet import defer
from twisted.enterprise import adbapi
from scrapy.exceptions import NotConfigured


class MysqlWriter(object):
    """
    A pipeline that writes to MySQL database
    """

    @classmethod
    def from_crawler(cls, crawler):
        """获取scrapycrawler 并访问管道设置"""
        # 从配置中获取MySQL URL
        mysql_url = crawler.settings.get("MYSQL_PIPELINE_URL", None)
        if not mysql_url:
            raise NotConfigured

        # create the class
        return cls(mysql_url)

    def __init__(self, mysql_url):
        """打开mysql 连接池"""
        self.mysql_url = mysql_url

        # report connection error only once
        self.report_connection_error = True

        # 解析 MySQL URL ，尝试初始化连接
        conn_kwargs = MysqlWriter.parse_mysql_url(mysql_url)
        print("conn_kwargs: ", conn_kwargs)
        # 第一个参数表示调用MySQLdb库，之后参数是传给MySQLdb.connect()方法的，参考MySQLdb.connections.Connection
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                            charset='utf8',
                                            use_unicode=True,
                                            connect_timeout=5,
                                            **conn_kwargs)

    def close_spider(self, spider):
        """爬虫关闭时，关闭数据库连接池"""
        self.dbpool.close()

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        """处理item， 将其插入MySQL数据库"""
        logger = spider.logger

        try:
            yield self.dbpool.runInteraction(self.do_replace, item)  # 调用do_replace方法与数据库交互
        except MySQLdb.OperationalError:
            if self.report_connection_error:
                logger.error("Can't connect to MySQL: %s" % self.mysql_url)
                self.report_connection_error = False
        except:
            print(traceback.format_exc())

        # 返回item供后续阶段使用
        defer.returnValue(item)

    @staticmethod
    def do_replace(tx, item):
        """执行 REPLACE INTO 命令，这里没使用 INSERT INTO是为了防止出现主键相同会报错的情况发生"""
        sql = """REPLACE INTO properties (url, title, price, description) VALUES (%s, %s, %s, %s)"""

        args = (
            item['url'][0][:100],
            item['title'][0][:30],
            item['price'][0],
            item['description'][0].replace("\r\n", " ")[:100]
        )
        tx.execute(sql, args)

    @staticmethod
    def parse_mysql_url(mysql_url):
        """
        解析mysql url 并为adbapi.ConnectionPool() 准备参数
        """
        params = dj_database_url.parse(mysql_url)

        conn_kwargs = {}
        conn_kwargs['host'] = params['HOST']
        conn_kwargs['user'] = params['USER']
        conn_kwargs['passwd'] = params['PASSWORD']
        conn_kwargs['db'] = params['NAME']
        conn_kwargs['port'] = params['PORT']

        # remove items with empty values
        conn_kwargs = dict((k, v) for k, v in conn_kwargs.items() if v)


        return conn_kwargs
