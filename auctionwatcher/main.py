from auctionwatcher.spiders.auction import AuctionSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Auctionwatcher arguments.')
    
    # Add arguments
    parser.add_argument('--mail_pass', type=str, required=True,
                        help='password for mail sending')
    
    # Parse the arguments
    args = parser.parse_args()
    return args


def execute():
    args = parse_args()

    settings = get_project_settings()
    settings.set("MAIL_PASS", args.mail_pass)
    print(f"{settings.get("MAIL_PASS") = }")
    print(f"{settings.get("MAIL_HOST") = }")
    print(f"{settings.get("MAIL_USER") = }")
    print(f"{settings.get("MAIL_PASS") = }")
    process = CrawlerProcess(settings)
    process.crawl(AuctionSpider)
    process.start()

if __name__=="__main__":
    execute()
