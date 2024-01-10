# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags

def clean_price(value):
    value = value.replace(',', '.')
    value = value.replace('\xa0zł', '')
    return float(value)


class WkdzikscraperItem(scrapy.Item):
    name = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    price = scrapy.Field(
        input_processor=MapCompose(remove_tags, clean_price),
        output_processor=TakeFirst(),
    )
