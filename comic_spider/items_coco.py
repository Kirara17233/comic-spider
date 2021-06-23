import scrapy


class ComicItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    update = scrapy.Field()
    category_id = scrapy.Field()


class CategoryItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()


class ChapterItem(scrapy.Item):
    comic_id = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    size = scrapy.Field()
    code = scrapy.Field()
