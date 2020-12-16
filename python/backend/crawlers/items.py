from scrapy.item import Item, Field


class PostItem(Item):
    id = Field()
    title = Field()
    link = Field()
    likes = Field()
    bookmarks = Field()
    views = Field()
    comments = Field()
    datetime = Field()
    posted = Field()
    text = Field()
    tags = Field()