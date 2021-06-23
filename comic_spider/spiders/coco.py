import scrapy
from comic_spider.spiders.coco_crypto import decrypt

from comic_spider.items import ComicItem, CategoryItem, ChapterItem
from comic_spider.source import coco
from comic_spider.spiders.functions import get_main_url
from comic_spider.orm.orm import get_source

source = get_source(coco)
main_url = get_main_url(source)


class CocoSpider(scrapy.Spider):
    name = source.code
    allowed_domains = [source.domain]
    start_url = main_url + '/show?orderBy=update'

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response):
        comic_list = response.xpath('//a[@class="fed-list-pics fed-lazy fed-part-2by3"]')
        for comic in comic_list:
            comic_url = main_url + comic.xpath('./@href').get()
            yield scrapy.Request(comic_url, callback=self.parse_comic)
        next_page = response.xpath('//a[@class="fed-btns-info fed-rims-info"]')
        if len(next_page) == 2 or next_page.xpath('./text()').get() == '下页':
            next_url = main_url + '/show?orderBy=update&page=' + next_page[-1].xpath('./@onclick').get()[11:-2]
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_comic(self, response):
        comic = ComicItem[self.name]()
        comic['id'] = int(response.xpath('//meta[@itemprop="url"]/@content').get()[27:-1])
        comic['name'] = response.xpath('//meta[@property="og:comic:book_name"]/@content').get()
        li_list = response.xpath('//li[@class="fed-col-xs12 fed-col-md6 fed-part-eone website-padding-right-1"]')
        for li in li_list:
            if li.xpath('./span/text()').get() == '作者':
                comic['author'] = li.xpath('./a/text()').get()
            if li.xpath('./span/text()').get() == '类别':
                comic['category_id'] = []
                for category in li.xpath('.//a'):
                    comic['category_id'].append(CategoryItem[self.name](id=int(category.xpath('./@href').get()[21:]), name=category.xpath('./text()').get()))
            if li.xpath('./span/text()').get() == '更新':
                comic['update'] = li.xpath('./a/text()').get()
                if comic['update'][:4] == '2564':
                    comic['update'] = '2021' + comic['update'][4:]
        yield comic
        chapters = response.xpath('//a[@class="fed-btns-info fed-rims-info fed-part-eone"]')
        for chapter in chapters:
            yield scrapy.Request(main_url + chapter.xpath('./@href').get(), callback=self.parse_chapter)

    def parse_chapter(self, response):
        chapter = ChapterItem[self.name]()
        for text in response.xpath('//script/text()').getall():
            if text[:12] == 'var C_DATA=\'':
                chapter['code'] = text[12:-2]
                break
        chapter['comic_id'], chapter['id'], chapter['name'], chapter['size'], chapter['code'] = decrypt(chapter['code'])
        yield chapter
