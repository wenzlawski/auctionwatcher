from auctionwatcher.spiders.auction import AuctionSpider
from scrapy.crawler import CrawlerProcess

def execute():
    process = CrawlerProcess()
    process.crawl(AuctionSpider)
    process.start()

if __name__=="__main__":
    execute()
