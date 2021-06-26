import scrapy
from comic_spider.spiders.coco_crypto import decrypt

from comic_spider.items import ComicItem, CategoryItem, ChapterItem
from comic_spider.source import coco
from comic_spider.spiders.functions import get_main_url
from comic_spider.spiders.constants import *
from comic_spider.orm.orm import get_source, has_chapter

source = get_source(coco)
main_url = get_main_url(source)


class CocoSpider(scrapy.Spider):
    name = source.code
    allowed_domains = [source.domain]
    start_url = main_url + '/show?orderBy=update'

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response):
        comic_list = response.xpath(comics_content)
        for comic in comic_list:
            comic_url = main_url + comic.xpath(href_attribute).get()
            yield scrapy.Request(comic_url, callback=self.parse_comic)
        next_page = response.xpath(page_content)
        if len(next_page) == 2 or next_page.xpath(text_content).get() == '下页':
            next_url = main_url + '/show?orderBy=update&page=' + next_page[-1].xpath(onclick_attribute).get()[11:-2]
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_comic(self, response):
        comic = ComicItem[self.name]()
        comic['id'] = int(response.xpath(comic_id_content).get()[27:-1])
        comic['name'] = response.xpath(comic_name_content).get()
        li_list = response.xpath(comic_info_content)
        for li in li_list:
            if li.xpath(span_content).get() == '作者':
                comic['author'] = li.xpath('./a/text()').get()
            if li.xpath(span_content).get() == '更新':
                comic['update'] = li.xpath(a_content).get()
                if comic['update'][:3] == '256':
                    comic['update'] = str(int(comic['update'][:4]) - 543) + comic['update'][4:]
        yield comic
        for li in li_list:
            if li.xpath(span_content).get() == '类别':
                for category in li.xpath('.//a'):
                    yield CategoryItem[self.name](comic_id=comic['id'],
                                                  id=int(category.xpath(href_attribute).get()[21:]),
                                                  name=category.xpath(text_content).get())
                break
        chapters = response.xpath(chapters_content)
        for chapter in chapters:
            if not has_chapter(self.name, comic['id'], chapter.xpath(href_attribute).get()[9:-5]):
                yield scrapy.Request(main_url + chapter.xpath(href_attribute).get(), callback=self.parse_chapter)

    def parse_chapter(self, response):
        chapter = ChapterItem[self.name]()
        for text in response.xpath(script_content).getall():
            beginning = 'var C_DATA=\''
            if text[:len(beginning)] == beginning:
                chapter['code'] = text[12:-len('\';')]
                break
        chapter['comic_id'], chapter['id'], chapter['name'], chapter['size'], chapter['code'] = decrypt(chapter['code'])
        yield chapter
