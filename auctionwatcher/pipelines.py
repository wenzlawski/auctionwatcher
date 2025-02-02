# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from auctionwatcher.items import Auction
from dataclasses import fields, astuple
from scrapy.mail import MailSender
import sqlite3
import jinja2
import humanize
import dateparser
import datetime as dt
import importlib.metadata
import os
import platformdirs

class AuctionwatcherPipeline:
    def init_db(self):
        self.con = sqlite3.connect(self.get_db_home())
        self.cur = self.con.cursor()
        self.new_auctions = []
        field_str = ", ".join([field.name for field in fields(Auction)])
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS auction({field_str})")
        self.con.commit()

    def open_spider(self, spider):
        self.init_db()

    def close_spider(self, spider):
        self.con.commit()
        self.con.close()
        if self.new_auctions:
            spider.logger.info(f"{len(self.new_auctions)} new auctions.")
            self.send_mail(spider.settings)
        else:
            spider.logger.info(f"No new auctions.")

    def new_auctions_mail(self):
        template_loader = jinja2.PackageLoader("auctionwatcher", "templates")
        template_env = jinja2.Environment(loader=template_loader,
                                          autoescape=jinja2.select_autoescape(['html']))
        template = template_env.get_template("mail.html")

        end_dates = [dateparser.parse(a.end_datetime,
                                      languages=['de'],
                                      date_formats=['%A %d.%m.%Y'])
                     for a in self.new_auctions]
        now = dt.datetime.now()
        human_dates = [humanize.precisedelta(now - d,
                                             minimum_unit="hours",
                                             format="%.0f")
                       for d in end_dates]

        html_output = template.render(auction_pairs=zip(self.new_auctions, human_dates))

        return html_output

    def send_mail(self, settings):
        mailer = MailSender.from_settings(settings)

        mailer.send("marcwenzlawski@posteo.com",
                    "New Auctions Registered",
                    body=self.new_auctions_mail(),
                    mimetype="text/html",
                    charset="utf-8")

    def get_db_home(self):
        datadir = platformdirs.user_data_dir("auctionwatcher", "mw")
        os.makedirs(datadir, exist_ok=True)
        return os.path.join(datadir, "database.sqlite")

    def process_item(self, item: Auction, spider):
        field_names = [field.name for field in fields(item)]
        placeholders = ", ".join(["?"] * len(field_names))
        columns = ", ".join(field_names)

        self.cur.execute("SELECT COUNT(*) FROM auction WHERE no = ?", (item.no, ))
        exists = self.cur.fetchone()[0]

        if not exists:
            self.cur.execute(f"INSERT INTO auction ({columns}) VALUES ({placeholders})",
                             astuple(item))
            self.new_auctions.append(item)

        return item
