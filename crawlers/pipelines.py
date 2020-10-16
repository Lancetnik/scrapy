import json

from itemadapter import ItemAdapter
import psycopg2

from .settings import *


class PostgresPipeline():
    def open_spider(self, spider):
        self.connection = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_NAME, port = DB_PORT)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.cur.execute(
            "select * from habr where link = (%s)",
            (item['link'],)
        )
        link = self.cur.fetchall()
        if not link:
            self.cur.execute(
                "insert into habr values(%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    item['link'], item['title'], [item['likes']],
                    [item['bookmarks']], [item['views']], [item['comments']],
                    [item['datetime']], item['posted']
                )
            )
        else:
            self.cur.execute(
                    "update habr set\
                     likes = likes || (%(likes)s), bookmarks = bookmarks || (%(bookmarks)s), \
                     views = views || (%(views)s), comments = comments || (%(comments)s), \
                     datetime = datetime || (%(datetime)s) \
                     where link = (%(link)s) and\
                     datetime[array_upper(datetime, 1)] <> (%(datetime)s)",
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