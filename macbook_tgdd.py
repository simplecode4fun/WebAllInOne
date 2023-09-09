import scrapy


class MacbookTgddSpider(scrapy.Spider):
    name = "macbook_tgdd"
    allowed_domains = ["https://shopee.vn"]
    start_urls = ["https://shopee.vn/product/172060422/8320492390"]

    def parse(self, response):
        data = response.xpath('//div[@class="s_44qnta"]//span').get()
        yield {'data': data}