def get_main_url(source):
    return source.protocol + '://' + source.third_level_domain + '.' + source.domain
