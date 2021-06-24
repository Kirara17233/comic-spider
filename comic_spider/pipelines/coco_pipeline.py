from comic_spider.source import coco
from comic_spider.items import ComicItem, CategoryItem, ChapterItem
from comic_spider.spiders.coco import CocoSpider
from comic_spider.orm.orm import save_comic, save_category, save_chapter


class CocoComicPipeline:
    def process_item(self, comic, spider):
        if type(comic) == ComicItem[CocoSpider.name]:
            save_comic(coco, comic)
        return comic


class CocoCategoryPipeline:
    def process_item(self, category, spider):
        if type(category) == CategoryItem[CocoSpider.name]:
            save_category(coco, category)
        return category


class CocoChapterPipeline:
    def process_item(self, chapter, spider):
        if type(chapter) == ChapterItem[CocoSpider.name]:
            save_chapter(coco, chapter)
        return chapter
