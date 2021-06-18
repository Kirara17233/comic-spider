from comic_spider.orm.orm import get_categories, add_category

category_map = {}


def get_main_url(source):
    return source.protocol + '://' + source.third_level_domain + '.' + source.domain


def code_category(source, categories):
    if source not in category_map:
        category_map[source] = get_categories(source)
    result = chr(len(categories))
    for category in categories:
        if category not in category_map[source]:
            category_map[source][category] = add_category(source, category)
        result = chr(category_map[source][category]) + result
    return result
