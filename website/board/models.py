from django.contrib.postgres.fields import ArrayField
from django.db import models


class Habr(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.TextField()
    title = models.TextField()
    posted = models.DateTimeField(blank=True, null=True)
    tags = ArrayField(models.TextField())
    likes = ArrayField(models.IntegerField())
    bookmarks = ArrayField(models.IntegerField())
    views = ArrayField(models.IntegerField())
    comments = ArrayField(models.IntegerField())
    datetime = ArrayField(models.DateTimeField())

    def to_dict(self):
        with open(f"../crawlers/posts/habr/{self.id}.txt", 'r', encoding="utf8") as file:
            return {
                'id': self.id,
                'link': self.link,
                'title': self.title,
                'posted': str(self.posted),
                'tags': self.tags,
                'likes': self.likes,
                'bookmarks': self.bookmarks,
                'comments': self.comments,
                'datetime': self.datetime,
                'text': file.read()
            }

    def to_preview(self):
        with open(f"../crawlers/posts/habr/{self.id}.txt", 'r', encoding="utf8") as file:
            return {
                'id': self.id,
                'link': self.link,
                'title': self.title,
                'posted': str(self.posted),
                'annotation': file.read()[:300]+'...'
            }

    class Meta:
        managed = False
        db_table = 'habr'