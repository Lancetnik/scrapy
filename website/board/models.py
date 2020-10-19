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

    def __repr__(self):
        return f"{self.id} : {self.title}"

    class Meta:
        managed = False
        db_table = 'habr'