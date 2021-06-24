point = '.'
text = '/text()'
href = '/@href'
onclick = '/@onclick'
span = '/span'
a = '/a'
content = '/@content'
text_content = point + text
href_attribute = point + href
onclick_attribute = point + onclick
span_content = point + span + text
a_content = point + a + text

comics_content = '//a[@class="fed-list-pics fed-lazy fed-part-2by3"]'
chapter_name_content = './/span[@class="fed-list-remarks fed-font-xii fed-text-white fed-text-center"]' + text
page_content = '//a[@class="fed-btns-info fed-rims-info"]'
comic_id_content = '//meta[@itemprop="url"]' + content
comic_name_content = '//meta[@property="og:comic:book_name"]' + content
comic_info_content = '//li[@class="fed-col-xs12 fed-col-md6 fed-part-eone website-padding-right-1"]'
chapters_content = '//a[@class="fed-btns-info fed-rims-info fed-part-eone"]'
script_content = '//script' + text
