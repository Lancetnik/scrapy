from datetime import datetime, timedelta

import psycopg2

from website.settings import *


def call_db(function):
    def decor(*args, **kwargs):
        conn = psycopg2.connect(dbname=DB_NAME, 
                                user=DB_USER, 
                                password=DB_PASSWORD, 
                                host=DB_HOST, 
                                port=DB_PORT)
        cur = conn.cursor()
        
        rez = function(cur, *args, **kwargs)
        
        conn.commit()
        cur.close()
        conn.close()

        return rez
    return decor


class HabrPost:
    def __init__(
            self, link: str, 
            title="", likes=[], bookmarks=[],
            views=[], comments=[], datetime=[],
            posted=datetime(2020, 1, 1)
        ):
        self.link = link
        self.title = title
        self.likes = likes
        self.bookmarks = bookmarks
        self.views = views
        self.comments = comments
        self.datetime = datetime
        self.posted = posted

    def to_dict(self):
        return {
            'link': self.link,
            'title': self.title,
            'likes': self.likes,
            'bookmarks': self.bookmarks,
            'views': self.views,
            'comments': self.comments, 
            'datetime': self.datetime,
            'posted': self.posted
        }

    @staticmethod
    def posts_maker(data: list):
        for post in data:
            yield HabrPost(
                post[0], post[1], post[2],
                post[3], post[4], post[5],
                post[6], post[7]
            ).to_dict()

    @staticmethod
    @call_db
    def all(cur):
        cur.execute("select * from habr")
        result = list(HabrPost.posts_maker(cur.fetchall()))
        return result

    @staticmethod
    @call_db
    def sql(cur, command: str):
        cur.execute(command)
        result = cur.fetchall()
        return result