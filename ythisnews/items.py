from scrapy import Item, Field


class YthisnewsItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    news = Field()

