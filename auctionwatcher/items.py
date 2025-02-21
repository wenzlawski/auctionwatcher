# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from dataclasses import dataclass

@dataclass
class Auction:
    title: str
    no: int
    location_name: str
    postcode: str
    street: str 
    city: str
    end_datetime: str
    collection_time: str = ''
    payment: str = ''
    contact: str = ''
    viewing_time: str = ''
    shipping: str = ''


# class AuctionwatcherItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass
