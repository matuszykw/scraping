# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags
import deepl
import os
import re

deepl_api_key = os.environ.get("DEEPL_API_KEY")
translator = deepl.Translator(deepl_api_key)

def genres(value):
    # if "Komedia" in value:
    #     value = "Komedia"
    # elif "Dramat" in value:
    #     value = "Dramat"
    # elif "Kryminał" in value:
    #     value = "Thriller"
    # elif "Akcja" in value:
    #     value = "Action"
    result = translator.translate_text(value, target_lang='EN-US', source_lang='PL')
    return result.text

def ranking(value):
    return value.replace("#", '')

def country(value):
    result = translator.translate_text(value, target_lang='EN-US', source_lang='PL')
    return result.text

def clean_price(value):
    return re.sub(r'\D', '', value)

def round_rating(value):
    rating = float(value)
    return round(rating, 2)


class FilmwebItem(scrapy.Item):
    global_ranking = scrapy.Field(
        input_processor = MapCompose(remove_tags, ranking),
        output_processor=TakeFirst()
    )
    title = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor=TakeFirst()
    )
    rating = scrapy.Field(
        input_processor = MapCompose(remove_tags, round_rating),
        output_processor=TakeFirst()
    )
    num_of_ratings = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor=TakeFirst()
    )
    genre = scrapy.Field(
        input_processor = MapCompose(remove_tags, genres),
        output_processor=TakeFirst()
    )
    country_of_origin = scrapy.Field(
        input_processor = MapCompose(remove_tags, country),
        output_processor=TakeFirst()
    )
    release_date = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor=TakeFirst()
    )
    us_gross = scrapy.Field(
        input_processor = MapCompose(remove_tags, clean_price),
        output_processor=TakeFirst()
    )
    worldwide_gross = scrapy.Field(
        input_processor = MapCompose(remove_tags, clean_price),
        output_processor=TakeFirst()
    )
    budget = scrapy.Field(
        input_processor = MapCompose(remove_tags, clean_price),
        output_processor=TakeFirst()
    )