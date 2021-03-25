from django.contrib.postgres.fields import ArrayField
from django.db import models

from django.conf import settings


class PostModel(models.Model):
    link = models.TextField(unique=True)
    title = models.TextField(unique=True)
    posted = models.DateTimeField()
    source = models.TextField()
    tags = ArrayField(
            models.CharField(max_length=30, blank=True),
            blank=True, null=True
        )

    likes = ArrayField(
            models.IntegerField(blank=True),
            size=settings.PARSER_COUNTER, blank=True, null=True,
            default = list()
        )
    bookmarks = ArrayField(
            models.IntegerField(blank=True),
            size=settings.PARSER_COUNTER, blank=True, null=True,
            default = list()
        )
    views = ArrayField(
            models.IntegerField(blank=True),
            size=settings.PARSER_COUNTER, blank=True, null=True,
            default = list()
        )
    comments = ArrayField(
            models.IntegerField(blank=True),
            size=settings.PARSER_COUNTER, blank=True, null=True,
            default = list()
        )
    datetime = ArrayField(
            models.DateTimeField(),
            size=settings.PARSER_COUNTER, blank=True, null=True,
            default = list()
        )
    text = models.TextField()

    def __repr__(self):
        return f"{self.id}: {self.link}"
    
    def __str__(self):
        return f"{self.id}: {self.link}"