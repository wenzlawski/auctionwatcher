from auctionwatcher.spiders.auction import AuctionSpider

from scrapy.crawler import CrawlerProcess

import json
import scrapy

from collections import OrderedDict
from datetime import datetime
from operator import itemgetter
from pathlib import Path
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field


class SaveItemPipeline:
    """Append item to list in SpiderManager"""
    def process_item(self, item, spider):
        SpiderManager.spider_data.append(item)


class SpiderManager:
    spider_data = []
    
    def __init__(self):
        self.run_spider()
        self.compile_json_data()

    @staticmethod
    def write_json(data, filename="quote_data.json"):
        """Write data to JSON file"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def read_json(filename="quote_data.json"):
        """Get data from JSON file"""
        try:
            with open(filename) as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            data = OrderedDict()
        except ValueError:
            data = []
        return data

    @staticmethod
    def compile_json_data():
        """Read the data from the spider & created an OrderedDict"""
        spider_data = SpiderManager.spider_data

        SpiderManager.write_json(spider_data, filename="auctions.json")

    def run_spider(self):
        """Run the spider"""
        process = CrawlerProcess({
            "ITEM_PIPELINES": {SaveItemPipeline: 100},
                                  })
        process.crawl(AuctionSpider)
        process.start()

        
if __name__ == '__main__':
    SpiderManager()
