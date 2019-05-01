# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from urllib import parse
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,Compose,Identity,TakeFirst,Join


class CtripSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CtripItermLoader(ItemLoader):
    default_output_processor = TakeFirst()


def img_url_prase(url_list):
    for i in range(len(url_list)):
        url = parse.urljoin("https:",url_list[i])
        url_list[i]=url
    return url_list


def convert_to_int(value):
    price = int(value)
    return price


def get_num(value):
    if len(value) > 0:
        return [int(value[len(value)-1])]


class CtripItem(scrapy.Item):

    url = scrapy.Field()
    num = scrapy.Field(
        input_processor=Compose(get_num)
    )
    title = scrapy.Field()
    price = scrapy.Field(
        input_processor=MapCompose(convert_to_int)
    )
    img_urls = scrapy.Field(
        input_processor=Compose(img_url_prase),
        output_processor=Identity()
    )
    trip_type = scrapy.Field()
    image_path = scrapy.Field(
        output_processor=Join(',')
    )
    destination = scrapy.Field()
    vendor = scrapy.Field()
    guarantee = scrapy.Field(
        input_processor=Identity(),
        output_processor=Join(',')
    )
    pass