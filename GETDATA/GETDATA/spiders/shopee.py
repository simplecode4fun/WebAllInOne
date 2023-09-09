import re
import scrapy
from scrapy_splash import SplashRequest
from ..items import ShopeeProduct
from scrapy.loader import ItemLoader

class ShopeeSpider(scrapy.Spider):
    name = 'shopee'
    allowed_domains = ['shopee.vn']

    page_number = 0  # trang mặc định page=0

    start_urls = ["https://shopee.vn/sp.btw2"]  # đây là 1 trang cửa hàng

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url,
                endpoint="render.html",
                args={
                    'wait': 5,
                },
                callback=self.parse,
                dont_filter=True
            )

    def parse(self, response):
        for data in response.css(".col-xs-2-4"):

            l = ItemLoader(item = ShopeeProduct(), selector = data)

            l.add_css('title', '.pcmall-shopmicrofe_2498rm', re='([^]]+$)')  # Xóa chuỗi [text]
            l.add_css('price', '.pcmall-shopmicrofe_1KcSLJ')
           
            yield l.load_item()


           # phân trang
            next_page = 'https://shopee.vn/sp.btw2?page='+ str(ShopeeSpider.page_number)

            if ShopeeSpider.page_number < 5:  # Giới hạn quét bao nhiêu trang
                ShopeeSpider.page_number += 1
                yield response.follow(next_page, callback=self.parse)