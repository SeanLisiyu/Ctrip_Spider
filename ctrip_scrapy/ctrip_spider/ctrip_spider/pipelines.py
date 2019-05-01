# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

class CtripSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class TripImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        image_path = []
        for ok,value in results:
            image_path.append(value["path"])
        item["image_path"] = image_path
        return item


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        # Twisted API
        dbparams = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset="utf8",
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)
        return cls(dbpool)

    def do_insert(self, cursor, item):
        # 自定义 执行插入
        img_url = ",".join(item["img_urls"])
        img_path = ",".join(item["image_path"]) # item["image_path"] # "full/xxx"
        insert_sql = """
                    insert into ctrip_spider(url, num ,title, price, img_urls, trip_type, image_path , destination, vendor, guarantee)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        cursor.execute(insert_sql, (
        item["url"], item["num"], item["title"], item["price"], img_url, item["trip_type"],
        img_path, item["destination"], item["vendor"], item["guarantee"]))

    def handle_error(self, failure, item, spider):
        #处理异步处理的异常
        print(failure)

    def process_item(self, item, spider):
        # 使用twised 将插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) # 处理异常