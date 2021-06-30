from comic_spider.source import coco
from comic_spider.items import ComicItem, CategoriesItem, ChapterItem
from comic_spider.spiders.coco import CocoSpider
from comic_spider.orm.orm import save_comic, save_category, save_chapter


class CocoComicPipeline:
    def process_item(self, comic, spider):
        if type(comic) == ComicItem[CocoSpider.name]:
            save_comic(coco, comic)
        return comic


class CocoCategoriesPipeline:
    def process_item(self, categories, spider):
        if type(categories) == CategoriesItem[CocoSpider.name]:
            save_category(coco, categories)
        return categories


class CocoChapterPipeline:
    def process_item(self, chapter, spider):
        if type(chapter) == ChapterItem[CocoSpider.name]:
            save_chapter(coco, chapter)
        return chapter
