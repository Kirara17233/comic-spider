import scrapy


class ComicItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    update = scrapy.Field()
    category = scrapy.Field()


class CategoryItem(scrapy.Item):
    name = scrapy.Field()
    id = scrapy.Field()


class ChapterItem(scrapy.Item):
    comic_id = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()


class MappingItem(scrapy.Item):
    name = scrapy.Field()
    code = scrapy.Field()
