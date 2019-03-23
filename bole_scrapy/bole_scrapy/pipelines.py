# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
import os
import MySQLdb
import MySQLdb.cursors
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi

root_dir = os.path.dirname(os.path.dirname(__file__))
target_file = os.path.join(root_dir, "article.json")


class BoleScrapyPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonExporterPipeline(object):
    """
    1. 使用scrapy原生的json文件到处类进行json文件的写入
    2. 与JsonWithEncodingPipeline类功能一致
    """

    def __init__(self):
        self.file = open(target_file, 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


class JsonWithEncodingPipeline(object):
    """
    1. 使用codecs库打开一个json文件然后写入item的内容
    2. 可以在settings.py文件中设置运行等级 e.g. 2
    """

    def __init__(self):
        self.file = codecs.open(target_file, "a", encoding="utf-8")

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(content)
        return item

    def close_spider(self, spider):
        self.file.close()


class MysqlTwistedPipline(object):
    """
    使用twisted实现数据库的异步插入
    """

    def __init__(self, db_pool):
        self.db_pool = db_pool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings["MYSQL_HOST"],
            database=settings["MYSQL_DBNAME"],
            db=settings['MYSQL_TABLENAME'],
            user=settings["MYSQL_USER"],
            password=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        db_pool = adbapi.ConnectionPool('MySQLdb', **dbparams)
        return cls(db_pool)

    def do_insert(self, cursor, item):
        insert_sql = "insert into jobbole_article (article_url, article_title, article_date, article_url_object_id) values (%s, %s, %s, %s)"
        cursor.execute(
            insert_sql,
            (
                item.get('article_url'),
                item.get('article_title'),
                item['article_date'],
                item.get('article_url_object_id')
            )
        )

    def handle_error(self, failure):
        # 处理异步插入数据库的异常
        print(failure)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        if not item:
            return {}
        query = self.db_pool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)
        return item


class MysqlPipeline(object):
    """
    :param str host:        host to connect
    :param str user:        user to connect as
    :param str password:    password to use
    :param str passwd:      alias of password, for backward compatibility
    :param str database:    database to use
    :param str db:          alias of database, for backward compatibility
    :param int port:        TCP/IP port to connect to
    :param str unix_socket: location of unix_socket to use
    :param dict conv:       conversion dictionary, see MySQLdb.converters
    """

    def __init__(self):
        self.conn = MySQLdb.connect(host='localhost',
                                    port=3306,
                                    user='root',
                                    password='8823443wsj_WIN',
                                    database='ariticle_spider',
                                    db='jobbole_article',
                                    charset='utf8',
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if not item:
            return item
        insert_sql = "insert into jobbole_article (article_url, article_title, article_date, article_url_object_id) values (%s, %s, %s, %s)"
        # try:
        self.cursor.execute(insert_sql, (
            item.get('article_url', 'www.baidu.com'),
            item.get('article_title', '百度'),
            item['article_date'],
            item.get('article_url_object_id', '1111111166666666')))
        self.conn.commit()
        return item


class ArticleImagesPipeline(ImagesPipeline):
    """
    1. 继承 ImagesPipeline 之后重写 item_completed 方法然后对传进来的item进行处理
    2. 可以在settings.py文件中设置这个pipeline的运行等级 e.g. 1
    """

    def item_completed(self, results, item, info):
        for ok, value in results:
            if ok:
                item['article_image_local_path'] = value['path']
                return item


if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.dirname(__file__))
    print(root_dir)
    print(os.path.join(root_dir, "article.json"))
