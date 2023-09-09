# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# import scrapy


# class GetdataItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass


# items.py
import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags

""" Dùng với ItemLoader """
# Xóa dấu chấm (.) trong giá
def remove_dot(value):
    return value.replace('.', '')
# xóa khoảng trắng đầu và cuôi trong tiêu đề nếu có
def remove_space(value):
    return value.strip()

class ShopeeProduct(scrapy.Item):
    title = scrapy.Field(input_processor=MapCompose(remove_tags, remove_space), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=[remove_tags, remove_dot], output_processor=TakeFirst())
