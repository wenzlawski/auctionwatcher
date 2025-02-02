import scrapy
from auctionwatcher.items import Auction
from urllib.parse import urlparse
import os

auction_translator = {
    "Zuschlagstermin": "end_datetime",
    "Besichtigungstermin": "viewing_time",
    "Abholung": "collection_time",
    "Bezahlung": "payment",
    "Kontakt": "contact",
    "Versand": "shipping"
}

class AuctionSpider(scrapy.Spider):
    name = "auction"
    allowed_domains = ["luedtke-auktion-online.de"]
    start_url = "https://luedtke-auktion-online.de"

    def start_requests(self):
        # get the main page and extract auctions from it
        return [
            scrapy.Request(
                self.start_url,
                callback = self.get_auctions
            )
        ]

    def get_auctions(self, response):
        self.logger.info("Getting the auctions")
        auctions = response.css("#auktionen").css(".linkauktionen")
        for a in auctions:
            yield self.parse_auction(a)

    def parse_auction(self, element):
        url = element.xpath("@href").get()
        parsed = urlparse(url)
        content = element.css(".auction-content")
        title = content.css(".title-area").css(".title::text").getall()
        infos = self.clean_list(title)

        if len(infos) != 4:
            raise Exception("Not enough data from the title.")

        data = {}
        data["no"] = os.path.basename(parsed.path)
        data["location_name"] = infos[0]
        data["street"] = infos[1]
        data["city"] = infos[2].split()[1]
        data["postcode"] = infos[2].split()[0]
        data["title"] = infos[3]

        for el in content.css(".bid-area"):
            field_name = auction_translator[el.css("b::text").get().strip(" :")]
            data[field_name] = " ".join(self.clean_list(el.css("div::text").getall()))

        return Auction(**data)

    def clean_list(self, lst):
        return list(filter(bool, map(lambda x: x.strip(), lst)))

    def parse(self, response):
        self.logger.info("A response from %s just arrived" , response.url)
