import scrapy


class ComicItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    update = scrapy.Field()
    latest = scrapy.Field()


class CategoryItem(scrapy.Item):
    comic_id = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()


class CategoriesItem(scrapy.Item):
    list = scrapy.Field()


class ChapterItem(scrapy.Item):
    comic_id = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    size = scrapy.Field()
    code = scrapy.Field()
