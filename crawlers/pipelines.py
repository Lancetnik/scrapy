import json

from itemadapter import ItemAdapter
from loguru import logger
import psycopg2
from psycopg2 import sql

from .settings import *


class PostgresPipeline():
    def open_spider(self, spider):
        logger.add(f'crawlers/logs/{spider.name}/debug.log', format="{time} {message}",
            level="DEBUG", rotation="10 MB", compression='zip')
        self.connection = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_NAME, port = DB_PORT)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    @logger.catch
    def process_item(self, item, spider):
        self.cur.execute(
            sql.SQL("select * from {} where link = (%s)")
                .format(sql.Identifier(spider.name)),
                (item['link'], )
        )
        link = self.cur.fetchall()
        if not link:
            # self.cur.execute(
            #     sql.SQL("insert into {} values(%s, %s, %s, %s, %s, %s, %s, %s)")
            #     .format(sql.Identifier(spider.name)),
            #     (
            #         item['link'], item['title'], [item['likes']], 
            #         [item['bookmarks']], [item['views']], [item['comments']],
            #         [item['datetime']], item['posted']
            #     )
            # )
            addr = item["link"].split('/')[-2]
            with open(f'crawlers/posts/{spider.name}/{addr}.txt', 'w', encoding='utf-8') as outfile:
                outfile.write(item["text"])
        else:
            self.cur.execute(
                sql.SQL(
                    "update habr set\
                     likes = likes || (%(likes)s), bookmarks = bookmarks || (%(bookmarks)s), \
                     views = views || (%(views)s), comments = comments || (%(comments)s), \
                     datetime = datetime || (%(datetime)s) \
                     where link = (%(link)s) and\
                     datetime[array_upper(datetime, 1)] <> (%(datetime)s)")
                .format(sql.Identifier(spider.name)),
                {
                    'link': item['link'],
                    'title': item['title'],
                    'likes': item['likes'],
                    'bookmarks': item['bookmarks'],
                    'views': item['views'],
                    'comments': item['comments'],
                    'datetime': item['datetime']
                }
            )
        self.connection.commit()
        return item