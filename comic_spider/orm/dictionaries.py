from comic_spider.source import coco
from comic_spider.orm import orm_coco

Comic = {
    coco: orm_coco.Comic
}

Category = {
    coco: orm_coco.Category
}

ComicCategory = {
    coco: orm_coco.ComicCategory
}

Chapter = {
    coco: orm_coco.Chapter
}
